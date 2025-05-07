// Copyright (c) 2023-2024, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
//
// NVIDIA CORPORATION and its licensors retain all intellectual property
// and proprietary rights in and to this software, related documentation
// and any modifications thereto.  Any use, reproduction, disclosure or
// distribution of this software and related documentation without an express
// license agreement from NVIDIA CORPORATION is strictly prohibited.

#ifndef CUBLASDX_DATABASE_CUTE_HPP
#define CUBLASDX_DATABASE_CUTE_HPP

#include "cublasdx/database/cute_tensor.hpp"
#include "cublasdx/database/cute_db.hpp"
#include "cublasdx/database/cute_utils.hpp"
#include "cublasdx/database/suggested_layouts.hpp"
#include "cublasdx/detail/blas_partition.hpp"

namespace cublasdx::detail {

    template<class TileOperator, typename = void>
    struct get_tiled_mma;

    template<class TileOperator>
    struct get_tiled_mma<TileOperator, cute::enable_if_t<cute::is_void_v<typename TileOperator::mma>>> {
        using type = void;
    };

    template<class TileOperator>
    struct get_tiled_mma<TileOperator, cute::enable_if_t<not cute::is_void_v<typename TileOperator::mma>>> {
        using type =
            cute::TiledMMA<cute::MMA_Atom<typename TileOperator::mma>,
                           cute::Layout<cute::Shape<cute::Int<TileOperator::tile_x>,
                                                    cute::Int<TileOperator::tile_y>,
                                                    cute::_1> >,
                           typename TileOperator::permute>;
    };

    template<class BlockSize>
    CUBLASDX_DEVICE static constexpr unsigned get_threads() {
        unsigned ret = 128;
        if constexpr(not cute::is_void_v<BlockSize>) {
            ret = BlockSize::flat_size;
        }
        return ret;
    }

    template<class TiledMMA>
    CUBLASDX_DEVICE static constexpr unsigned get_mma_threads() {
        unsigned ret = 0;
        if constexpr(not cute::is_void_v<TiledMMA>) {
            ret = cute::size(TiledMMA{});
        }
        return ret;
    }

    template<class BlockSize>
    CUBLASDX_DEVICE static constexpr unsigned get_block_rank() {
        unsigned ret = 1;
        if constexpr(not cute::is_void_v<BlockSize>) {
            ret = BlockSize::rank;
        }
        return ret;
    }

    template<int BlockRank>
    CUBLASDX_DEVICE static unsigned int get_thread_idx() {
        constexpr int block_rank = BlockRank;
        if constexpr (block_rank == 3) {
            return threadIdx.x + threadIdx.y * blockDim.x + threadIdx.z * blockDim.x * blockDim.y;
        } else if constexpr (block_rank == 2) {
            return threadIdx.x + threadIdx.y * blockDim.x;
        } else {
            return threadIdx.x;
        }
    }

    template<class BlockSize>
    CUBLASDX_DEVICE static unsigned int get_thread_idx() {
        constexpr int block_rank = get_block_rank<BlockSize>();
        return get_thread_idx<block_rank>();
    }

    namespace cute_backend {
        template<typename TypeA,
                 typename TypeB,
                 typename TypeC,
                 typename InputA,
                 typename InputB,
                 typename InputC,
                 typename Alignment,
                 int SizeM,
                 int SizeN,
                 int SizeK,
                 typename Arrangement,
                 typename TransposeMode,
                 typename SM,
                 class HasStaticBlockDim,
                 typename BlockSize, // void if empty
                 typename OverloadedTileOperator>
        struct execution {
            private:
            using overloaded_config = typename get_tiled_mma<OverloadedTileOperator>::type;
            static constexpr bool is_tile_overloaded = not cute::is_void_v<overloaded_config>;

            static_assert(cute::is_void_v<BlockSize> or cute::is_void_v<overloaded_config> or
                          get_mma_threads<overloaded_config>() == get_threads<BlockSize>());

            // Necessary only for pointer API
            using blas_transpose_mode = TransposeMode;
            static constexpr auto tr_mode_a = blas_transpose_mode::a_transpose_mode;
            static constexpr auto tr_mode_b = blas_transpose_mode::b_transpose_mode;
            static constexpr auto tr_mode_c = transpose_mode::non_transposed;

            using blas_blockdim = BlockSize;

            // Necessary only for pointer API
            using blas_arrangement = Arrangement;
            static constexpr auto arr_a = blas_arrangement::a;
            static constexpr auto arr_b = blas_arrangement::b;
            static constexpr auto arr_c = blas_arrangement::c;

            using blas_alignment = Alignment;
            static constexpr auto align_a = blas_alignment::a;
            static constexpr auto align_b = blas_alignment::b;
            static constexpr auto align_c = blas_alignment::c;
            using default_a_copy_op = cute::AutoVectorizingCopyWithAssumedAlignment<align_a * 8>;
            using default_b_copy_op = cute::AutoVectorizingCopyWithAssumedAlignment<align_b * 8>;
            using default_c_copy_op = cute::AutoVectorizingCopyWithAssumedAlignment<align_c * 8>;

            // Necessary for both APIs
            static constexpr unsigned int m = SizeM;
            static constexpr unsigned int n = SizeN;
            static constexpr unsigned int k = SizeK;

            static constexpr auto has_static_block_dim = HasStaticBlockDim{};

            static constexpr int block_size = get_threads<BlockSize>();
            using swizzled_meta_info = cublasdx::detail::layout_database::optimal_config<
                block_size, SM::value,
                TypeA, arr_a == arrangement::col_major, align_a,
                TypeB, arr_b == arrangement::col_major, align_b,
                TypeC, arr_c == arrangement::col_major, align_c,
                m, n, k>;

            using swizzled_config    = typename swizzled_meta_info::TiledMma;
            using swizzled_a_layout  = typename swizzled_meta_info::a_layout;
            using swizzled_b_layout  = typename swizzled_meta_info::b_layout;
            using swizzled_c_layout  = typename swizzled_meta_info::c_layout;
            using swizzled_a_copy_op = typename swizzled_meta_info::a_copy_op;
            using swizzled_b_copy_op = typename swizzled_meta_info::b_copy_op;
            using swizzled_c_copy_op = typename swizzled_meta_info::c_copy_op;

            static constexpr bool is_swizzled_config_viable = not is_tile_overloaded and swizzled_meta_info::optimal;

            // This is necessary for a case where swizzled config is available but the user
            // does not utilize suggested layout and db_entry has higher number of threads
            // than 128
            using db_config = decltype(get_database_config<TypeA, TypeB, TypeC, m, n, k, arr_a, arr_b, align_a, align_b, SM, BlockSize>());

            using default_config = cute::conditional_t<is_tile_overloaded, overloaded_config, db_config>;

            using suggested_threads_config = cute::conditional_t<is_swizzled_config_viable, swizzled_config, default_config>;


            public:
            // Helper traits for knowing fragment type upfront
            using c_frag_t = decltype(cute::partition_fragment_C(default_config{}, cute::Shape<Int<SizeM>, Int<SizeN>>{}));
            using c_frag_suggested_t = decltype(cute::partition_fragment_C(suggested_threads_config{}, cute::Shape<Int<SizeM>, Int<SizeN>>{}));

            // If blocksize is not specified, this one will be used
            // it should be the most performant block size for this problem
            static constexpr unsigned int suggested_threads = cute::size(suggested_threads_config{});

            // Partitioner getters
            CUBLASDX_DEVICE static auto get_partitioner() {
                const auto thread_idx = cublasdx::detail::get_thread_idx<BlockSize>();
                auto tiled_mma = default_config{};
                auto shape_mn = cute::Shape<cute::Int<SizeM>, cute::Int<SizeN>>{};
                auto c_copy_op = default_c_copy_op{};
                return blas_partitioner(thread_idx, tiled_mma, shape_mn, type_wrapper<InputC>{}, has_static_block_dim);
            }

            CUBLASDX_DEVICE static auto suggest_partitioner() {
                const auto thread_idx = cublasdx::detail::get_thread_idx<BlockSize>();
                if constexpr(is_swizzled_config_viable) {
                    auto tiled_mma = swizzled_config{};
                    auto shape_mn = cute::Shape<cute::Int<SizeM>, cute::Int<SizeN>>{};
                    auto c_copy_op = swizzled_c_copy_op{};
                    return blas_partitioner(thread_idx, tiled_mma, shape_mn, type_wrapper<InputC>{}, has_static_block_dim);
                } else {
                    return get_partitioner();
                }
            }

            template<typename ALayout, typename BLayout>
            CUBLASDX_DEVICE static auto get_partitioner(ALayout, BLayout) {
                constexpr bool is_suggested_mma =
                    is_swizzled_config_viable and
                    cute::is_same_v<ALayout, swizzled_a_layout> and
                    cute::is_same_v<BLayout, swizzled_b_layout>;

                if constexpr(is_suggested_mma) {
                    return suggest_partitioner();
                } else {
                    return get_partitioner();
                }

                CUTE_GCC_UNREACHABLE;
            }


            // C in registers API
            template<typename TSA,
                    typename ALayout,
                    typename TSB,
                    typename BLayout,
                    typename TRC,
                    typename CLayout,
                    typename ALoadOp = identity,
                    typename BLoadOp = identity,
                    __CUTE_REQUIRES(cute::is_smem_v<TSA> and cute::is_smem_v<TSB> and cute::is_rmem_v<TRC>)>
            CUBLASDX_DEVICE static void tensor_gemm(cute::Tensor<TSA, ALayout> const& smem_tensor_a,
                                                    cute::Tensor<TSB, BLayout> const& smem_tensor_b,
                                                    cute::Tensor<TRC, CLayout>      & rmem_tensor_c,
                                                    const ALoadOp&                    a_load_op = identity {},
                                                    const BLoadOp&                    b_load_op = identity {}) {
                const auto thread_idx = cublasdx::detail::get_thread_idx<BlockSize>();

                static_assert(cute::is_same_v<CLayout, decltype(c_frag_suggested_t().layout())> or
                              cute::is_same_v<CLayout, decltype(c_frag_t().layout())>,
                              "Incompatible C fragment type used");

                constexpr bool is_suggested_mma =
                    is_swizzled_config_viable and
                    cute::is_same_v<CLayout, decltype(c_frag_suggested_t().layout())>;

                constexpr bool is_suggested_copy =
                    is_suggested_mma and
                    cute::is_same_v<ALayout, swizzled_a_layout> and
                    cute::is_same_v<BLayout, swizzled_b_layout> and
                    ((sizeof(typename TSA::value_type) == sizeof(TypeA) and alignof(typename TSA::value_type) == alignof(TypeA)) and
                     (sizeof(typename TSB::value_type) == sizeof(TypeB) and alignof(typename TSB::value_type) == alignof(TypeB)));

                auto tiled_mma = cute::conditional_t<is_suggested_mma, swizzled_config, default_config>{};
                auto a_copy_op = cute::conditional_t<is_suggested_copy, swizzled_a_copy_op, default_a_copy_op>{};
                auto b_copy_op = cute::conditional_t<is_suggested_copy, swizzled_b_copy_op, default_b_copy_op>{};

                if (has_static_block_dim or thread_idx < cute::size(tiled_mma)) {
                    cute::cooperative_gemm(thread_idx,
                                           tiled_mma,
                                           smem_tensor_a,
                                           swap_tensor_modes(smem_tensor_b),
                                           rmem_tensor_c,
                                           a_load_op,
                                           b_load_op,
                                           a_copy_op,
                                           b_copy_op);
                }
            }

            // Accept mutable temporaries
            template<typename TSA,
                    typename ALayout,
                    typename TSB,
                    typename BLayout,
                    typename TRC,
                    typename CLayout,
                    typename ALoadOp = identity,
                    typename BLoadOp = identity,
                    __CUTE_REQUIRES(cute::is_smem_v<TSA> and cute::is_smem_v<TSB> and cute::is_rmem_v<TRC>)>
            CUBLASDX_DEVICE static void tensor_gemm(cute::Tensor<TSA, ALayout> const& smem_tensor_a,
                                                               cute::Tensor<TSB, BLayout> const& smem_tensor_b,
                                                               cute::Tensor<TRC, CLayout>     && rmem_tensor_c,
                                                               const ALoadOp&                    a_load_op = identity {},
                                                               const BLoadOp&                    b_load_op = identity {}) {
                tensor_gemm(smem_tensor_a, smem_tensor_b, rmem_tensor_c, a_load_op, b_load_op);
            }

            // This operates on assumption (checked in BLAS.execute()) that tensor sizes agree with operator sizes
            template<typename TA,
                     typename ALayout,
                     typename TB,
                     typename BLayout,
                     typename TC,
                     typename CLayout,
                     typename Alpha,
                     typename Beta,
                     typename ALoadOp = identity,
                     typename BLoadOp = identity,
                     typename CLoadOp = identity,
                     typename CStoreOp = identity,
                     __CUTE_REQUIRES(cute::is_smem_v<TA> and cute::is_smem_v<TB> and cute::is_smem_v<TC>)>
            CUBLASDX_DEVICE static void tensor_gemm(cute::Tensor<TA, ALayout> const& smem_tensor_a,
                                                               cute::Tensor<TB, BLayout> const& smem_tensor_b,
                                                               cute::Tensor<TC, CLayout>      & smem_tensor_c,
                                                               Alpha                            alpha,
                                                               Beta                             beta,
                                                               const ALoadOp&                   a_load_op  = identity {},
                                                               const BLoadOp&                   b_load_op  = identity {},
                                                               const CLoadOp&                   c_load_op  = identity {},
                                                               const CStoreOp&                  c_store_op = identity {}) {
                const auto thread_idx = cublasdx::detail::get_thread_idx<BlockSize>();

                constexpr bool is_suggested_mma =
                    is_swizzled_config_viable and
                    cute::is_same_v<ALayout, swizzled_a_layout> and
                    cute::is_same_v<BLayout, swizzled_b_layout> and
                    cute::is_same_v<CLayout, swizzled_c_layout>;

                constexpr bool is_suggested_copy =
                    is_suggested_mma and
                    ((sizeof(typename TA::value_type) == sizeof(TypeA) and alignof(typename TA::value_type) == alignof(TypeA)) and
                     (sizeof(typename TB::value_type) == sizeof(TypeB) and alignof(typename TB::value_type) == alignof(TypeB)) and
                     (sizeof(typename TC::value_type) == sizeof(TypeC) and alignof(typename TC::value_type) == alignof(TypeC)));

                auto tiled_mma = cute::conditional_t<is_suggested_mma, swizzled_config, default_config>{};
                auto a_copy_op = cute::conditional_t<is_suggested_copy, swizzled_a_copy_op, default_a_copy_op>{};
                auto b_copy_op = cute::conditional_t<is_suggested_copy, swizzled_b_copy_op, default_b_copy_op>{};
                auto c_copy_op = cute::conditional_t<is_suggested_copy, swizzled_c_copy_op, default_c_copy_op>{};

                if (has_static_block_dim or thread_idx < cute::size(tiled_mma)) {
                    cute::cooperative_gemm(thread_idx,
                                           tiled_mma,
                                           alpha,
                                           smem_tensor_a,
                                           swap_tensor_modes(smem_tensor_b),
                                           beta,
                                           smem_tensor_c,
                                           a_load_op,
                                           b_load_op,
                                           c_load_op,
                                           c_store_op,
                                           a_copy_op,
                                           b_copy_op,
                                           c_copy_op);
                }
            }

            // Accept mutable temporaries
            template<typename TA,
                     typename ALayout,
                     typename TB,
                     typename BLayout,
                     typename TC,
                     typename CLayout,
                     typename Alpha,
                     typename Beta,
                     typename ALoadOp = identity,
                     typename BLoadOp = identity,
                     typename CLoadOp = identity,
                     typename CStoreOp = identity,
                     __CUTE_REQUIRES(cute::is_smem_v<TA> and cute::is_smem_v<TB> and cute::is_smem_v<TC>)>
            CUBLASDX_DEVICE static void tensor_gemm(cute::Tensor<TA, ALayout> const& smem_tensor_a,
                                                               cute::Tensor<TB, BLayout> const& smem_tensor_b,
                                                               cute::Tensor<TC, CLayout>     && smem_tensor_c,
                                                               Alpha                            alpha,
                                                               Beta                             beta,
                                                               const ALoadOp&                   a_load_op  = identity {},
                                                               const BLoadOp&                   b_load_op  = identity {},
                                                               const CLoadOp&                   c_load_op  = identity {},
                                                               const CStoreOp&                  c_store_op = identity {}) {
                tensor_gemm(smem_tensor_a, smem_tensor_b, smem_tensor_c, alpha, beta, a_load_op, b_load_op, c_load_op, c_store_op);
            }
        };
    } // namespace cute_backend
} // namespace cublasdx::detail

#endif // CUBLASDX_DATABASE_CUTE_HPP
