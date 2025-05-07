// Copyright (c) 2024, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
//
// NVIDIA CORPORATION and its licensors retain all intellectual property
// and proprietary rights in and to this software, related documentation
// and any modifications thereto.  Any use, reproduction, disclosure or
// distribution of this software and related documentation without an express
// license agreement from NVIDIA CORPORATION is strictly prohibited.

#ifndef CUSOLVERDX_DETAIL_CUSOLVERDX_DESCRIPTION_HPP
#define CUSOLVERDX_DETAIL_CUSOLVERDX_DESCRIPTION_HPP

#include "commondx/detail/stl/type_traits.hpp"
#include "commondx/traits/detail/get.hpp"
#include "commondx/detail/expressions.hpp"

#include "cusolverdx/operators.hpp"
#include "cusolverdx/traits/detail/description_traits.hpp"
#include "cusolverdx/detail/solver_is_supported.hpp"

namespace cusolverdx {
    namespace detail {
        template<size_t org_size, size_t alignment = 16>
        inline constexpr size_t aligned_size() {
            return ((org_size + alignment - 1) / alignment) * alignment;
        }
        template<size_t alignment = 16>
        inline constexpr size_t aligned_dynamic_size(const size_t org_size) {
            return ((org_size + alignment - 1) / alignment) * alignment;
        }

        template<class... Operators>
        class solver_operator_wrapper: public commondx::detail::description_expression {};

        template<class... Operators>
        class solver_description: public commondx::detail::description_expression {
            using description_type = solver_operator_wrapper<Operators...>;

        protected:
            /// ---- Traits

            // Size
            // * Default value: NONE
            // * If there is no size, then dummy size is (8, 8, 8). This is required value for M, N sized don't break.
            // * Values of has_size or is_complete should be checked before using this property.
            static constexpr bool has_size  = has_operator<operator_type::size, description_type>::value;
            using dummy_default_solver_size = Size<8, 8>;
            using this_solver_size          = get_or_default_t<operator_type::size, description_type, dummy_default_solver_size>;

            // Type (real, complex)
            // * Default value: real
            using this_solver_type                   = get_or_default_t<operator_type::type, description_type, default_type_operator>;
            static constexpr auto this_solver_type_v = this_solver_type::value;

            // Function
            // * Default value: NONE
            // * Dummy value: potrf
            static constexpr bool has_function           = has_operator<operator_type::function, description_type>::value;
            using this_solver_function                   = get_or_default_t<operator_type::function, description_type, default_function_operator>;
            static constexpr auto this_solver_function_v = this_solver_function::value;

            // Precision
            // * Default: A, X, B are all float
            using this_solver_precision = get_or_default_t<operator_type::precision, description_type, default_precision_operator>;

            // Arrangement
            // * Default value: col_major
            static constexpr bool has_arrangement = has_operator<operator_type::arrangement, description_type>::value;

            using this_solver_arrangement                   = get_or_default_t<operator_type::arrangement, description_type, default_arrangement_operator>;
            static constexpr auto this_solver_arrangement_a = this_solver_arrangement::a;
            static constexpr auto this_solver_arrangement_b = this_solver_arrangement::b;

            // Transpose
            // * default non_trans
            static constexpr bool has_transpose           = has_operator<operator_type::transpose, description_type>::value;
            using this_solver_transpose                   = get_or_default_t<operator_type::transpose, description_type, default_transpose_operator>;
            static constexpr auto this_solver_transpose_v = this_solver_transpose::value;

            // Leading Dimension
            static constexpr bool         has_ld      = has_operator<operator_type::leading_dimension, description_type>::value;
            static constexpr unsigned int default_lda = ((this_solver_arrangement_a == arrangement::col_major) ? this_solver_size::m : this_solver_size::n);
            static constexpr unsigned int default_ldb = ((this_solver_arrangement_b == arrangement::col_major) ? this_solver_size::n : this_solver_size::nrhs);
            // Minimum possible ld's for detecting invalid configurations
            static constexpr unsigned int min_lda = this_solver_size::m <= this_solver_size::n ? this_solver_size::m : this_solver_size::n;
            static constexpr unsigned int min_ldb = this_solver_size::n <= this_solver_size::nrhs ? this_solver_size::n : this_solver_size::nrhs;

            using dummy_default_ld                = LeadingDimension<1, 1>;
            static constexpr auto this_solver_lda = has_ld ? get_or_default_t<operator_type::leading_dimension, description_type, dummy_default_ld>::a : default_lda;
            static constexpr auto this_solver_ldb = has_ld ? get_or_default_t<operator_type::leading_dimension, description_type, dummy_default_ld>::b : default_ldb;

            // FillMode
            // * Default value: NONE
            static constexpr bool has_fill_mode           = has_operator<operator_type::fill_mode, description_type>::value;
            using this_solver_fill_mode                   = get_or_default_t<operator_type::fill_mode, description_type, default_fill_mode_operator>;
            static constexpr auto this_solver_fill_mode_v = this_solver_fill_mode::value;

            // SM
            // * Default value: NONE
            // * Dummy value: 700
            static constexpr bool has_sm    = has_operator<operator_type::sm, description_type>::value;
            using dummy_default_sm          = SM<700>;
            using this_sm                   = get_or_default_t<operator_type::sm, description_type, dummy_default_sm>;
            static constexpr auto this_sm_v = this_sm::value;

            // Block
            static constexpr bool has_block = has_operator_v<operator_type::block, description_type>;

            // BlockDim
            static constexpr bool has_block_dim = has_operator<operator_type::block_dim, description_type>::value;

            using dummy_default_block_dim          = BlockDim<256, 1, 1>;
            static constexpr auto this_block_dim_x = get_or_default_t<operator_type::block_dim, description_type, dummy_default_block_dim>::value.x;
            static constexpr auto this_block_dim_y = get_or_default_t<operator_type::block_dim, description_type, dummy_default_block_dim>::value.y;
            static constexpr auto this_block_dim_z = get_or_default_t<operator_type::block_dim, description_type, dummy_default_block_dim>::value.z;

            using this_block_dim                   = BlockDim<this_block_dim_x, this_block_dim_y, this_block_dim_z>;
            static constexpr auto this_block_dim_v = this_block_dim::value;

            // BatchesPerBlock
            // * Default value: 1
            using this_solver_batches_per_block                   = get_or_default_t<operator_type::batches_per_block, description_type, default_batches_per_block_operator>;
            static constexpr auto this_solver_batches_per_block_v = this_solver_batches_per_block::value;

            // True if description is complete description
            static constexpr bool is_complete_v = is_complete_description<description_type>::value;


            /// ---- Constraints

            // We can only have one of each option

            // Main operators
            static constexpr bool has_one_block_dim         = has_at_most_one_of_v<operator_type::block_dim, description_type>;
            static constexpr bool has_one_block             = has_at_most_one_of_v<operator_type::block, description_type>;
            static constexpr bool has_one_batches_per_block = has_at_most_one_of_v<operator_type::batches_per_block, description_type>;
            static constexpr bool has_one_size              = has_at_most_one_of_v<operator_type::size, description_type>;
            static constexpr bool has_one_precision         = has_at_most_one_of_v<operator_type::precision, description_type>;
            static constexpr bool has_one_type              = has_at_most_one_of_v<operator_type::type, description_type>;
            static constexpr bool has_one_function          = has_at_most_one_of_v<operator_type::function, description_type>;
            static constexpr bool has_one_fill_mode         = has_at_most_one_of_v<operator_type::fill_mode, description_type>;
            static constexpr bool has_one_arrangement       = has_at_most_one_of_v<operator_type::arrangement, description_type>;
            static constexpr bool has_one_sm                = has_at_most_one_of_v<operator_type::sm, description_type>;

            static_assert(has_one_block_dim, "Can't create cusolverdx function with two BlockDim<> expressions");
            static_assert(has_one_block, "Can't create cusolverdx function with two Block expressions");
            static_assert(has_one_batches_per_block, "Can't create cusolverdx function with two BatchesPerBlock expressions");
            static_assert(has_one_size, "Can't create cusolverdx function with two Size expressions");
            static_assert(has_one_precision, "Can't create cusolverdx function with two Precision expressions");
            static_assert(has_one_type, "Can't create cusolverdx function with two Type expressions");
            static_assert(has_one_function, "Can't create cusolverdx function with two Function expressions");
            static_assert(has_one_fill_mode, "Can't create cusolverdx function with two FillMode expressions");
            static_assert(has_one_arrangement, "Can't create cusolverdx function with two Arrangement expressions");
            static_assert(has_one_sm, "Can't create cusolverdx function with two SM expressions");

            // Additional static checks
            static constexpr bool valid_block_dim = this_block_dim::flat_size >= 32 && this_block_dim::flat_size <= 1024;
            static_assert(valid_block_dim,
                          "Provided block dimension is invalid, BlockDim<> must have at least 32 threads, and can't "
                          "have more than 1024 threads.");
            static constexpr bool valid_batches_per_block = (this_solver_batches_per_block_v >= 1);
            static_assert(valid_batches_per_block, "Provided number of batches per block is invalid, BatchesPerBlock<> must have at least 1 batch");

            // Leading dimension check
            // col-major: LDA >= M
            // row-major: LDA >= N
            // col-major: LDB >= N
            // row-major: LDB >= NRHS
            // When no Arrangement operator, can only do the smaller comparison since they user might still set it
            static constexpr bool valid_lda = !has_ld || !has_size || (!has_arrangement && this_solver_lda >= min_lda) || (this_solver_lda >= default_lda);
            static_assert(valid_lda, "Incorrect leading dimension for A matrix, LDA must be equal or greater than M for column major and N for row major");

            static constexpr bool valid_ldb = !has_ld || !has_size || (!has_arrangement && this_solver_ldb >= min_ldb) || (this_solver_ldb >= default_ldb);
            static_assert(valid_ldb, "Incorrect leading dimension for B matrix, LDB must be equal or greater than N for column major and NRHS for row major");

            // e.g. Check if input fits in shared memory
            static constexpr unsigned int this_solver_a_size = (this_solver_arrangement_a == arrangement::col_major) ? this_solver_lda * this_solver_size::n : this_solver_lda * this_solver_size::m;
            static constexpr unsigned int this_solver_b_size = (this_solver_arrangement_b == arrangement::col_major) ? this_solver_ldb * this_solver_size::nrhs : this_solver_ldb * this_solver_size::n;
            static constexpr bool         valid_shared_size  = is_supported_shared_size<this_solver_precision,
                                                                               this_solver_type_v,
                                                                               this_solver_a_size * this_solver_batches_per_block_v,
                                                                               (is_solver<this_solver_function_v>::value ? this_solver_b_size : 0), // B size in shared memory
                                                                               this_sm_v>::value;
            static_assert((not has_sm) or valid_shared_size,
                          "Provided combination of data type and sizes makes this problem not fit into shared memory "
                          "available on the specified architecture");

            static constexpr bool is_function_cholesky = is_cholesky<this_solver_function_v>::value;
            static constexpr bool is_function_lu       = is_lu<this_solver_function_v>::value;
            static constexpr bool is_function_solver   = is_solver<this_solver_function_v>::value;

            // Transpose is only supported for LU solvers and trsm, and currently only non_trans is supported
            static constexpr bool valid_transpose = (this_solver_transpose_v == non_trans);
            static_assert(valid_transpose, "Only non_trans mode is supported currently");

            // Only real data type is supported for LU in 0.1.0
            static_assert(!(this_solver_type_v == type::complex && is_function_lu), "cuSolverDx 0.1.0 only support LU with real data type");

            /// ---- End of Constraints


        public:
            __device__ __host__ static bool constexpr is_complete() { return is_complete_v; }
        };

        template<>
        class solver_description<>: public commondx::detail::description_expression {};

    } // namespace detail
} // namespace cusolverdx

#undef STRINGIFY
#undef XSTRINGIFY

#endif // CUSOLVERDX_DETAIL_CUSOLVERDX_DESCRIPTION_HPP
