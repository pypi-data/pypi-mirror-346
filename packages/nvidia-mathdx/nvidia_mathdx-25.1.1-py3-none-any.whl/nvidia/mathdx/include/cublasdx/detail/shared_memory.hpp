// Copyright (c) 2025, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
//
// NVIDIA CORPORATION and its licensors retain all intellectual property
// and proprietary rights in and to this software, related documentation
// and any modifications thereto.  Any use, reproduction, disclosure or
// distribution of this software and related documentation without an express
// license agreement from NVIDIA CORPORATION is strictly prohibited.

#ifndef CUBLASDX_DETAIL_SHARED_MEMORY_HPP
#define CUBLASDX_DETAIL_SHARED_MEMORY_HPP

#include "cublasdx/detail/blas_execution.hpp"

namespace cublasdx {
    namespace detail {
        // Keep below functions external to allow for constexpr device
        // memory computation without code repetition
        template<class Layout>
        CUBLASDX_HOST_DEVICE constexpr
        COMMONDX_STL_NAMESPACE::enable_if_t<cublasdx::is_layout_v<Layout>, unsigned>
        add_aligned_shared_memory_extent(unsigned current, unsigned alignment, unsigned elem_size, const Layout& layout) {
            return (cutlass::round_up(current, alignment) + cublasdx::cosize(layout) * elem_size);
        }

        CUBLASDX_HOST_DEVICE constexpr
        unsigned add_aligned_shared_memory_extent(unsigned current, unsigned alignment, unsigned matrix_size_bytes) {
            return (cutlass::round_up(current, alignment) + matrix_size_bytes);
        }

        CUBLASDX_HOST_DEVICE constexpr
        unsigned add_aligned_shared_memory_extent(unsigned current, unsigned alignment, unsigned elem_size, unsigned num_elements) {
            return (cutlass::round_up(current, alignment) + num_elements * elem_size);
        }

        struct shared_storage_calc {
            private:
            unsigned current = 0;

            public:
            template<class ... Args>
            CUBLASDX_HOST_DEVICE shared_storage_calc&
            add(Args ... args) {
                current = add_aligned_shared_memory_extent(current, args...);
                return *this;
            }

            CUBLASDX_HOST_DEVICE unsigned get() {
                return current;
            }
        };

        CUBLASDX_HOST_DEVICE
        uintptr_t ptr_round_up(uintptr_t a, uintptr_t b) {
            return ((a + b - 1) / b) * b;
        }

        // Shared memory slicing helpers
        template<class T>
        struct pop_first_static;

        template<class T, class ... Ts>
        struct pop_first_static<cute::tuple<T, Ts...>> {
            using type = cute::tuple<Ts...>;
        };

        template<class T>
        using pop_first_static_t = typename pop_first_static<T>::type;


        template<class PointerTypeTuple, class Tuple, auto ... I>
        CUBLASDX_HOST_DEVICE
        auto offset_pointers(char* smem, Tuple const& offsets, cute::index_sequence<I...>) {
            return cute::make_tuple(reinterpret_cast<cute::tuple_element_t<I, PointerTypeTuple>*>(smem + cute::get<I>(offsets))...);
        }

        template<class PointerTypeTuple, class MD> // Memory Descriptor is: tuple<cosize, alignment>
        CUBLASDX_HOST_DEVICE
        constexpr auto align_offsets(uintptr_t smem, MD const& md) {
            static_assert(cute::tuple_size<PointerTypeTuple>::value == 1);
            using current_ptr_t = cute::tuple_element_t<0, PointerTypeTuple>;

            auto last_int_ptr = ptr_round_up(smem, cute::get<1>(md));

            return cute::make_tuple(last_int_ptr);
        }

        template<class PointerTypeTuple, class MD, class ... MDS> // Memory Descriptor is: tuple<cosize, alignment>
        CUBLASDX_HOST_DEVICE
        constexpr auto align_offsets(uintptr_t smem, MD const& md, MDS const& ... mds) {
            using current_ptr_t = cute::tuple_element_t<0, PointerTypeTuple>;
            constexpr auto elem_size = sizeof(current_ptr_t);

            const auto current_int_ptr = ptr_round_up(smem, cute::get<1>(md));
            using next_type_tuple = pop_first_static_t<PointerTypeTuple>;

            // next = current + tensor_cosize * elem_size
            const auto next_int_ptr = current_int_ptr + (cute::get<0>(md) * elem_size);
            return cute::prepend(align_offsets<next_type_tuple>(next_int_ptr, mds...), current_int_ptr);
        }
    }

    CUBLASDX_HOST_DEVICE
    detail::shared_storage_calc make_shared_storage_calc() {
        return detail::shared_storage_calc{};
    }

    template<class BLAS, class AValueType = typename BLAS::a_value_type,
                         class BValueType = typename BLAS::b_value_type,
                         class CValueType = typename BLAS::c_value_type,
                         class ALayout, class BLayout, class CLayout,
                         __CUTE_REQUIRES(cublasdx::is_layout_v<ALayout> and
                                         cublasdx::is_layout_v<BLayout> and
                                         cublasdx::is_layout_v<CLayout>)>
    CUBLASDX_HOST_DEVICE constexpr
    COMMONDX_STL_NAMESPACE::enable_if_t<is_blas_execution<BLAS>::value, unsigned>
    get_shared_storage_size(ALayout const& a_layout,
                            BLayout const& b_layout,
                            CLayout const& c_layout) {
        unsigned requirement = 0;
        requirement = detail::add_aligned_shared_memory_extent(requirement, alignment_of<BLAS>::a, sizeof(AValueType), a_layout);
        requirement = detail::add_aligned_shared_memory_extent(requirement, alignment_of<BLAS>::b, sizeof(BValueType), b_layout);
        requirement = detail::add_aligned_shared_memory_extent(requirement, alignment_of<BLAS>::c, sizeof(CValueType), c_layout);
        return requirement;
    }

    template<class BLAS, class AValueType = typename BLAS::a_value_type,
                         class BValueType = typename BLAS::b_value_type,
                         class CValueType = typename BLAS::c_value_type>
    CUBLASDX_HOST_DEVICE constexpr
    COMMONDX_STL_NAMESPACE::enable_if_t<is_blas_execution<BLAS>::value, unsigned>
    get_shared_storage_size(unsigned lda = leading_dimension_of<BLAS>::a,
                            unsigned ldb = leading_dimension_of<BLAS>::b,
                            unsigned ldc = leading_dimension_of<BLAS>::c) {
        return get_shared_storage_size<BLAS, AValueType, BValueType, CValueType>(
            BLAS::get_layout_smem_a(lda),
            BLAS::get_layout_smem_b(ldb),
            BLAS::get_layout_smem_c(ldc)
        );
    }

    template<class BLAS, class AValueType = typename BLAS::a_value_type,
                         class BValueType = typename BLAS::b_value_type,
                         class ALayout, class BLayout,
                         __CUTE_REQUIRES(cublasdx::is_layout_v<ALayout> and
                                         cublasdx::is_layout_v<BLayout>)>
    CUBLASDX_HOST_DEVICE constexpr
    COMMONDX_STL_NAMESPACE::enable_if_t<is_blas_execution<BLAS>::value, unsigned>
    get_shared_storage_size_ab(ALayout const& a_layout,
                               BLayout const& b_layout) {
        unsigned requirement = 0;
        requirement = detail::add_aligned_shared_memory_extent(requirement, alignment_of<BLAS>::a, sizeof(AValueType), a_layout);
        requirement = detail::add_aligned_shared_memory_extent(requirement, alignment_of<BLAS>::b, sizeof(BValueType), b_layout);
        return requirement;
    }

    template<class BLAS, class AValueType = typename BLAS::a_value_type,
                         class BValueType = typename BLAS::b_value_type>
    CUBLASDX_HOST_DEVICE constexpr
    COMMONDX_STL_NAMESPACE::enable_if_t<is_blas_execution<BLAS>::value, unsigned>
    get_shared_storage_size_ab(unsigned lda = leading_dimension_of<BLAS>::a,
                               unsigned ldb = leading_dimension_of<BLAS>::b) {
        return get_shared_storage_size_ab<BLAS, AValueType, BValueType>(
            BLAS::get_layout_smem_a(lda),
            BLAS::get_layout_smem_b(ldb)
        );
    }

    template<class ... PointerTypes, class ... Tuples>
    CUBLASDX_HOST_DEVICE auto
    slice_shared_memory_generic(void* smem, Tuples const& ... memory_descriptors) {
        static_assert(((cute::is_tuple_v<Tuples> and cute::tuple_size<Tuples>::value == 2) && ...),
                      "Can't slice shared memory, proper descriptor format is cute::tuple<uint, uint> (cosize, alignment)");

        static_assert(sizeof...(PointerTypes) == sizeof...(Tuples), "Number of pointer types must be the same as number of memory descriptors");

        using pointer_type_tuple = cute::tuple<PointerTypes...>;

        const auto slicing_offsets = detail::align_offsets<pointer_type_tuple>(0ull, memory_descriptors...);
        return detail::offset_pointers<pointer_type_tuple>(static_cast<char*>(smem), slicing_offsets, cute::make_index_sequence<cute::tuple_size<decltype(slicing_offsets)>::value>{});
    }

    template<class BLAS, class AValueType = typename BLAS::a_value_type,
                         class BValueType = typename BLAS::b_value_type,
                         class CValueType = typename BLAS::c_value_type,
                         class ALayout = decltype(BLAS::get_layout_smem_a().layout),
                         class BLayout = decltype(BLAS::get_layout_smem_b().layout),
                         class CLayout = decltype(BLAS::get_layout_smem_c().layout),
                         __CUTE_REQUIRES(cublasdx::is_layout_v<ALayout> and
                                         cublasdx::is_layout_v<BLayout> and
                                         cublasdx::is_layout_v<CLayout>)>
    CUBLASDX_HOST_DEVICE auto
    slice_shared_memory(void* smem,
                        ALayout const& a_layout = {},
                        BLayout const& b_layout = {},
                        CLayout const& c_layout = {}) {
        static_assert(is_complete_blas<BLAS>::value, "Can't slice shared memory, description is not complete");

        return slice_shared_memory_generic<AValueType, BValueType, CValueType>(
            smem,
            cute::make_tuple(cublasdx::cosize(a_layout), cute::C<alignment_of_v_a<BLAS>>{}),
            cute::make_tuple(cublasdx::cosize(b_layout), cute::C<alignment_of_v_b<BLAS>>{}),
            cute::make_tuple(cublasdx::cosize(c_layout), cute::C<alignment_of_v_c<BLAS>>{})
        );
    }

    template<class BLAS, class AValueType = typename BLAS::a_value_type,
                         class BValueType = typename BLAS::b_value_type,
                         class CValueType = typename BLAS::c_value_type>
    CUBLASDX_HOST_DEVICE auto
    slice_shared_memory(void* smem, unsigned lda, unsigned ldb, unsigned ldc) {
        return slice_shared_memory<BLAS, AValueType, BValueType, CValueType>
            (smem,
             BLAS::get_layout_smem_a(lda),
             BLAS::get_layout_smem_b(ldb),
             BLAS::get_layout_smem_c(ldc));
    }

    template<class BLAS, class AValueType = typename BLAS::a_value_type,
                         class BValueType = typename BLAS::b_value_type,
                         class ALayout = decltype(BLAS::get_layout_smem_a().layout),
                         class BLayout = decltype(BLAS::get_layout_smem_b().layout),
                         __CUTE_REQUIRES(cublasdx::is_layout_v<ALayout> and cublasdx::is_layout_v<BLayout>)>
    CUBLASDX_HOST_DEVICE auto
    slice_shared_memory_ab(void* smem,
                           ALayout const& a_layout = {},
                           BLayout const& b_layout = {}) {
        static_assert(is_complete_blas<BLAS>::value, "Can't slice shared memory, description is not complete");

        return slice_shared_memory_generic<AValueType, BValueType>(
            smem,
            cute::make_tuple(cublasdx::cosize(a_layout), cute::C<alignment_of_v_a<BLAS>>{}),
            cute::make_tuple(cublasdx::cosize(b_layout), cute::C<alignment_of_v_b<BLAS>>{})
        );
    }

    template<class BLAS, class AValueType = typename BLAS::a_value_type,
                         class BValueType = typename BLAS::b_value_type>
    CUBLASDX_HOST_DEVICE auto
    slice_shared_memory_ab(void* smem, unsigned lda, unsigned ldb) {
        return slice_shared_memory_ab<BLAS, AValueType, BValueType>
                                      (smem,
                                       BLAS::get_layout_smem_a(lda),
                                       BLAS::get_layout_smem_b(ldb));
    }
}

#endif // CUBLASDX_DETAIL_SHARED_MEMORY_HPP
