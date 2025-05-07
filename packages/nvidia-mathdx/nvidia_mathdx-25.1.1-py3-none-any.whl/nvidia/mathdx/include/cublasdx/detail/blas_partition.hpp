// Copyright (c) 2025, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
//
// NVIDIA CORPORATION and its licensors retain all intellectual property
// and proprietary rights in and to this software, related documentation
// and any modifications thereto.  Any use, reproduction, disclosure or
// distribution of this software and related documentation without an express
// license agreement from NVIDIA CORPORATION is strictly prohibited.

#ifndef CUBLASDX_DETAIL_BLAS_PARTITION_HPP
#define CUBLASDX_DETAIL_BLAS_PARTITION_HPP

#include "cublasdx/database/cute.hpp"

namespace cublasdx {
    namespace detail {
        template<class T>
        struct type_wrapper {
            using type = T;
        };

        template<class Index, class TiledMMA, class ShapeMN, class InputTypeC, class HasStaticBlockDim>
        struct blas_partitioner;

        template<class Index, class ... Args, class ShapeMN, class InputTypeC, class HasStaticBlockDim>
        struct blas_partitioner<Index, cute::TiledMMA<Args...>, ShapeMN, InputTypeC, HasStaticBlockDim> {
            private:

            static constexpr cute::TiledMMA<Args...> _tiled_mma = {};

            using thr_mma_t = decltype(_tiled_mma.get_thread_slice(Index{}));
            const thr_mma_t thr_mma;

            using coord_tensor_t = decltype(cute::make_identity_tensor(ShapeMN{}));
            using coord_slice_t = decltype(cute::declval<thr_mma_t>().partition_C(coord_tensor_t{}));
            const coord_slice_t thr_coord = thr_mma.partition_C(coord_tensor_t{});

            static constexpr auto is_partition_divisible =
                cute::evenly_divides(ShapeMN{}, cute::select<0, 1>(cute::tile_shape(_tiled_mma)));

            bool is_thr_active = false;

            HasStaticBlockDim has_static_block_dim;

            public:

            CUBLASDX_DEVICE
            blas_partitioner(Index thread_idx,
                            cute::TiledMMA<Args...> tiled_mma,
                            ShapeMN shape_mn,
                            type_wrapper<InputTypeC>,
                            HasStaticBlockDim has_static_block_dim)
                : thr_mma(tiled_mma.get_thread_slice(thread_idx)), is_thr_active(thread_idx < cute::size(tiled_mma)),
                  has_static_block_dim(has_static_block_dim) {};

            CUBLASDX_DEVICE
            constexpr auto is_predicated() const {
                return not is_partition_divisible;
            }

            CUBLASDX_DEVICE
            auto is_thread_active() const {
                return has_static_block_dim or is_thr_active;
            }

            template<class CTensor>
            CUBLASDX_DEVICE
            auto partition_like_C(CTensor && ctensor) const {
                return thr_mma.partition_C(ctensor);
            }

            CUBLASDX_DEVICE
            constexpr auto make_accumulator_fragment() const {
                return make_tensor<InputTypeC>(cute::partition_shape_C(cute::TiledMMA<Args...>{}, ShapeMN{}));
            }

            template<class ... Coords>
            CUBLASDX_DEVICE
            auto map_fragment_index(Coords&& ... coords) const {
                return thr_coord(static_cast<Coords&&>(coords)...);
            }

            template<class ... Coords>
            CUBLASDX_DEVICE
            bool is_index_in_bounds(Coords&& ... coords) const {
                return cute::elem_less(thr_coord(static_cast<Coords&&>(coords)...), ShapeMN{});
            }
        };

        // Deduction guide for the main constructor
        template<class Index, class ... Args, class ShapeMN, class InputTypeC, class HasStaticBlockDim>
        blas_partitioner(Index, cute::TiledMMA<Args...>, ShapeMN, type_wrapper<InputTypeC>, HasStaticBlockDim) -> blas_partitioner<Index, cute::TiledMMA<Args...>, ShapeMN, InputTypeC, HasStaticBlockDim>;
    }

    using cute::clear;
    using cute::transform;
    using cute::make_fragment_like;

    template<unsigned AlignmentInBytes,
             class TRC,
             class CFragLayout,
             class TC,
             class CLayout,
             class Partitioner>
    CUBLASDX_DEVICE
    COMMONDX_STL_NAMESPACE::enable_if_t<
         cute::is_rmem_v<TRC> and
        (cute::is_smem_v<TC> or cute::is_gmem_v<TC>)>
    copy_fragment(tensor<TRC, CFragLayout> const& tS,
                  tensor<TC, CLayout>           & tD,
                  Partitioner              const& p) {
        auto tPtD = p.partition_like_C(tD);

        using src_shape = decltype(tS.shape());
        using dst_shape = decltype(tPtD.shape());
        static_assert(cute::is_static_v<src_shape> and cute::is_static_v<dst_shape>,
            "cublasdx::copy requires static tensor layouts");

        auto predicated = p.is_predicated();

        if(p.is_thread_active()) {
            if constexpr(predicated) {
                cute::copy_if(cute::FunctionPredTensor([&](auto ... idx) { return p.is_index_in_bounds(idx ...); }), tS, tPtD);
            } else {
                cute::copy(cute::AutoVectorizingCopyWithAssumedAlignment<AlignmentInBytes * 8>{}, tS, tPtD);
            }
        }
    }


    template<unsigned AlignmentInBytes,
             class TRC,
             class CFragLayout,
             class TC,
             class CLayout,
             class Partitioner>
    CUBLASDX_DEVICE
    COMMONDX_STL_NAMESPACE::enable_if_t<
         cute::is_rmem_v<TRC> and
        (cute::is_smem_v<TC> or cute::is_gmem_v<TC>)>
    copy_fragment(tensor<TC, CLayout>      const& tS,
                  tensor<TRC, CFragLayout>      & tD,
                  Partitioner              const& p) {
        auto tPtS = p.partition_like_C(tS);

        using src_shape = decltype(tS.shape());
        using dst_shape = decltype(tPtS.shape());
        static_assert(cute::is_static_v<src_shape> and cute::is_static_v<dst_shape>,
            "cublasdx::copy requires static tensor layouts");

        auto predicated = p.is_predicated();

        if(p.is_thread_active()) {
            if constexpr(predicated) {
                cute::copy_if(cute::FunctionPredTensor([&](auto ... idx) { return p.is_index_in_bounds(idx ...); }), tPtS, tD);
            } else {
                cute::copy(cute::AutoVectorizingCopyWithAssumedAlignment<AlignmentInBytes * 8>{}, tPtS, tD);
            }
        }
    }

    namespace detail {
        template<class Beta>
        CUBLASDX_HOST_DEVICE constexpr
        bool is_zero(Beta beta) {
            if constexpr (cutlass::is_complex<Beta>::value) {
                using vt = typename Beta::value_type;
                const auto zero = static_cast<vt>(0.f);
                return beta.real() == zero && beta.imag() == zero;
            }
            else {
                const auto zero = static_cast<Beta>(0.f);
                return beta == zero;
            }
            CUTE_GCC_UNREACHABLE;
        }

        template<class Alpha,
                class XEngine, class XLayout,
                class Beta,
                class YEngine, class YLayout>
        CUBLASDX_HOST_DEVICE void
        axpby_impl(Alpha                          const& alpha,
                   cute::Tensor<XEngine, XLayout> const& x_tensor,
                   Beta                           const& beta,
                   cute::Tensor<YEngine, YLayout>      & y_tensor) {
            if(is_zero(beta)) {
                CUTE_UNROLL
                for(int i = 0; i < cute::size(y_tensor); ++i) {
                    y_tensor(i) = alpha * x_tensor(i);
                }
            } else {
                CUTE_UNROLL
                for(int i = 0; i < cute::size(y_tensor); ++i) {
                    y_tensor(i) = alpha * x_tensor(i) + beta * y_tensor(i);
                }
            }
        }

        // Accept mutable temporaries
        template<class Alpha,
                class XEngine, class XLayout,
                class Beta,
                class YEngine, class YLayout>
        CUBLASDX_HOST_DEVICE void
        axpby_impl(Alpha                          const&  alpha,
                   cute::Tensor<XEngine, XLayout> const&  x_tensor,
                   Beta                           const&  beta,
                   cute::Tensor<YEngine, YLayout>      && y_tensor) {
            axpby_impl(alpha, x_tensor, beta, y_tensor);
        }
    }

    template<class Alpha,
             class XEngine, class XLayout,
             class Beta,
             class YEngine, class YLayout>
    CUBLASDX_HOST_DEVICE void
    axpby(Alpha                          const& alpha,
          cute::Tensor<XEngine, XLayout> const& x_tensor,
          Beta                           const& beta,
          cute::Tensor<YEngine, YLayout>      & y_tensor) {

        using x_value_type = typename XEngine::value_type;
        using y_value_type = typename YEngine::value_type;

        static_assert(sizeof(Alpha) == sizeof(x_value_type) and alignof(Alpha) == alignof(x_value_type));
        static_assert(sizeof(Beta) == sizeof(y_value_type) and alignof(Beta) == alignof(y_value_type));

        detail::axpby_impl(
            reinterpret_cast<detail::convert_to_cutlass_type_t<x_value_type>const&>(alpha),
            cute::recast<detail::convert_to_cutlass_type_t<x_value_type>>(x_tensor),
            reinterpret_cast<detail::convert_to_cutlass_type_t<y_value_type>const&>(beta),
            cute::recast<detail::convert_to_cutlass_type_t<y_value_type>>(y_tensor)
        );
    }

    // Accept mutable temporaries
    template<class Alpha,
             class XEngine, class XLayout,
             class Beta,
             class YEngine, class YLayout>
    CUBLASDX_HOST_DEVICE void
    axpby(Alpha                          const&  alpha,
          cute::Tensor<XEngine, XLayout> const&  x_tensor,
          Beta                           const&  beta,
          cute::Tensor<YEngine, YLayout>      && y_tensor) {
        cublasdx::axpby(alpha, x_tensor, beta, y_tensor);
    }
} // namespace cublasdx

#endif // CUBLASDX_DETAIL_BLAS_PARTITION_HPP
