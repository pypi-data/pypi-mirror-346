// Copyright (c) 2024, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
//
// NVIDIA CORPORATION and its licensors retain all intellectual property
// and proprietary rights in and to this software, related documentation
// and any modifications thereto.  Any use, reproduction, disclosure or
// distribution of this software and related documentation without an express
// license agreement from NVIDIA CORPORATION is strictly prohibited.

#ifndef CUSOLVERDX_DETAIL_EXECUTION_HPP
#define CUSOLVERDX_DETAIL_EXECUTION_HPP

#include "commondx/detail/stl/type_traits.hpp"
#include "commondx/detail/stl/tuple.hpp"

#include "cusolverdx/detail/solver_description.hpp"
#include "cusolverdx/database/cholesky.cuh"
#include "cusolverdx/database/lu_np.cuh"
#include "cusolverdx/database/trs.cuh"


namespace cusolverdx {
    namespace detail {

        inline static constexpr unsigned smem_align(const unsigned size, const unsigned alignment = 16) {
            return (size + alignment - 1) / alignment * alignment; }

        template<class... Operators>
        class solver_execution: public solver_description<Operators...>, public commondx::detail::execution_description_expression {
            using base_type = solver_description<Operators...>;
            using this_type = solver_execution<Operators...>;

        protected:
            // Precision type
            using typename base_type::this_solver_precision;

            // Value type
            using this_solver_data_type = map_value_type<base_type::this_solver_type_v, this_solver_precision>;

            /// ---- Constraints
            // None

        public:
            using a_data_type = typename this_solver_data_type::a_type;
            using x_data_type = typename this_solver_data_type::x_type;
            using b_data_type = typename this_solver_data_type::b_type;

            static constexpr auto m_size = base_type::this_solver_size::m;
            static constexpr auto n_size = base_type::this_solver_size::n;
            static constexpr auto nrhs   = base_type::this_solver_size::nrhs;
            static constexpr auto lda    = base_type::this_solver_lda;
            static constexpr auto ldb    = base_type::this_solver_ldb;

            static constexpr auto a_size = base_type::this_solver_a_size;
            static constexpr auto b_size = base_type::this_solver_b_size;

            static constexpr bool is_function_cholesky = base_type::is_function_cholesky;
            static constexpr bool is_function_lu       = base_type::is_function_lu;
            static constexpr bool is_function_solver   = base_type::is_function_solver;
        };


        //=============================
        // Block execution
        //=============================
        template<class... Operators>
        class block_execution: public solver_execution<Operators...> {
            using this_type = block_execution<Operators...>;
            using base_type = solver_execution<Operators...>;

            // Import precision type from base class
            using typename base_type::this_solver_precision;

            /// ---- Constraints
            static_assert(base_type::has_block, "Can't create block cusolverdx block execution  without block execution operators");

        public:
            static constexpr auto m_size = base_type::m_size;
            static constexpr auto n_size = base_type::n_size;
            static constexpr auto nrhs   = base_type::nrhs;
            static constexpr auto lda    = base_type::lda;
            static constexpr auto ldb    = base_type::ldb;

            static constexpr unsigned int batches_per_block = base_type::this_solver_batches_per_block_v;

        private:
            __host__ __device__ __forceinline__ static constexpr unsigned int get_suggested_batches_per_block() {
                static_assert(base_type::is_complete_v, "Can't provide suggested batches per block, description is not complete");
                if constexpr (base_type::this_solver_function_v == function::potrf || base_type::this_solver_function_v == function::posv) {
                    return cholesky_suggested_batches<a_cuda_data_type, base_type::m_size, base_type::this_sm_v>();
                } else if constexpr (base_type::this_solver_function_v == function::getrf_no_pivot || base_type::this_solver_function_v == function::gesv_no_pivot) {
                    return lu_np_suggested_batches<a_cuda_data_type, base_type::m_size, base_type::n_size, base_type::this_sm_v>();
                } else {
                    return 1;
                }
            }

            __host__ __device__ __forceinline__ static constexpr dim3 get_suggested_block_dim() {
                static_assert(base_type::is_complete_v, "Can't provide suggested block dimensions, description is not complete");
                if constexpr (base_type::this_solver_function_v == function::potrf || base_type::this_solver_function_v == function::potrs || base_type::this_solver_function_v == function::posv) {
                    return cholesky_suggested_block_dim<a_cuda_data_type, base_type::m_size, batches_per_block, base_type::this_sm_v>();
                } else if constexpr (base_type::this_solver_function_v == function::getrf_no_pivot || base_type::this_solver_function_v == function::getrs_no_pivot ||
                                     base_type::this_solver_function_v == function::gesv_no_pivot) {
                    return lu_np_suggested_block_dim<a_cuda_data_type, base_type::m_size, base_type::n_size, batches_per_block, base_type::this_sm_v>();
                } else {
                    return 256;
                }
            }

            __host__ __device__ __forceinline__ static constexpr dim3 get_block_dim() {
                static_assert(base_type::is_complete_v, "Can't provide block dimensions, description is not complete");
                if constexpr (base_type::has_block_dim) {
                    return base_type::this_block_dim_v;
                }
                return get_suggested_block_dim();
            }

            __device__ __forceinline__ unsigned get_thread_id() {
                auto dim = get_block_dim();
                __builtin_assume(threadIdx.x < dim.x);
                __builtin_assume(threadIdx.y < dim.y);
                __builtin_assume(threadIdx.z < dim.z);

                return threadIdx.x + dim.x * (threadIdx.y + dim.y * threadIdx.z);
            }

        public:
            inline static constexpr unsigned int get_shared_memory_size() { return get_shared_memory_size(lda, ldb); }

            // support both compile-time and run-time leading dimensions
            inline static constexpr unsigned int get_shared_memory_size(const unsigned int runtime_lda, const unsigned int runtime_ldb = ldb) {
                static_assert(base_type::is_complete_v, "Can't calculate shared memory, description is not complete");

                const unsigned int size_a    = smem_align(sizeof(a_data_type) * runtime_lda * ((base_type::this_solver_arrangement_a == arrangement::col_major) ? n_size : m_size));
                const unsigned int size_b    = smem_align(sizeof(b_data_type) * runtime_ldb * ((base_type::this_solver_arrangement_b == arrangement::col_major) ? nrhs : n_size));
                const unsigned int size_ipiv = sizeof(int) * (m_size >= n_size ? n_size : m_size);

                switch (base_type::this_solver_function_v) {
                    case function::potrf:
                    case function::getrf_no_pivot:
                        return batches_per_block * size_a;

                    case function::potrs:
                    case function::posv:
                    case function::getrs_no_pivot:
                    case function::gesv_no_pivot:
                        return batches_per_block * (size_a + size_b);

                    default:
                        // Unknown routine
                        return 0;
                }
            }

            // Import value types from base class
            using typename base_type::a_data_type;
            using typename base_type::b_data_type;
            using typename base_type::x_data_type;

            using a_cuda_data_type = typename convert_to_cuda_type<a_data_type>::type;
            using b_cuda_data_type = typename convert_to_cuda_type<b_data_type>::type;
            using x_cuda_data_type = typename convert_to_cuda_type<x_data_type>::type;

            using status_type = int;

            // trsm
            template<class Solver = this_type>
            inline __device__ auto execute(a_data_type* A, const unsigned int runtime_lda, b_data_type* B, const unsigned int runtime_ldb = ldb) -> COMMONDX_STL_NAMESPACE::enable_if_t<function_of_v<Solver> == function::trsm, void> {

                // Hard coded for side left and non-unit diagonal
                trsm_dispatch<a_cuda_data_type, m_size, nrhs, true, false, base_type::this_solver_transpose_v, base_type::this_solver_fill_mode_v, base_type::this_solver_arrangement_a, base_type::this_solver_arrangement_b, max_threads_per_block, batches_per_block>(
                    (a_cuda_data_type*)A, runtime_lda, (a_cuda_data_type*)B, runtime_ldb, get_thread_id());
            }

            // potrf
            template<class Solver = this_type>
            inline __device__ auto execute(a_data_type* A, const unsigned int runtime_lda, status_type* status) -> COMMONDX_STL_NAMESPACE::enable_if_t<function_of_v<Solver> == function::potrf, void> {

                cholesky_dispatch<a_cuda_data_type, m_size, base_type::this_solver_fill_mode_v, base_type::this_solver_arrangement_a, max_threads_per_block, batches_per_block, base_type::this_sm_v>(
                    (a_cuda_data_type*)A, runtime_lda, status, get_thread_id());
            }

            // potrs
            template<class Solver = this_type>
            inline __device__ auto execute(a_data_type* A, const unsigned int runtime_lda, b_data_type* B, const unsigned int runtime_ldb = ldb) -> COMMONDX_STL_NAMESPACE::enable_if_t<function_of_v<Solver> == function::potrs, void> {

                potrs_dispatch<a_cuda_data_type, m_size, nrhs, base_type::this_solver_fill_mode_v, base_type::this_solver_arrangement_a, base_type::this_solver_arrangement_b, max_threads_per_block, batches_per_block>(
                    (a_cuda_data_type*)A, runtime_lda, (a_cuda_data_type*)B, runtime_ldb, get_thread_id());
            }

            // posv
            template<class Solver = this_type>
            inline __device__ auto execute(a_data_type* A, const unsigned int runtime_lda, b_data_type* B, const unsigned int runtime_ldb, status_type* status)
                -> COMMONDX_STL_NAMESPACE::enable_if_t<function_of_v<Solver> == function::posv, void> {

                cholesky_dispatch<a_cuda_data_type, m_size, base_type::this_solver_fill_mode_v, base_type::this_solver_arrangement_a, max_threads_per_block, batches_per_block, base_type::this_sm_v>(
                    (a_cuda_data_type*)A, runtime_lda, status, get_thread_id());
                potrs_dispatch<a_cuda_data_type, m_size, nrhs, base_type::this_solver_fill_mode_v, base_type::this_solver_arrangement_a, base_type::this_solver_arrangement_b, max_threads_per_block, batches_per_block>(
                    (a_cuda_data_type*)A, runtime_lda, (a_cuda_data_type*)B, runtime_ldb, get_thread_id());
            }

            // getrf_no_pivot
            template<class Solver = this_type>
            inline __device__ auto execute(a_data_type* A, const unsigned int runtime_lda, status_type* status)
                -> COMMONDX_STL_NAMESPACE::enable_if_t<function_of_v<Solver> == function::getrf_no_pivot, void> {

                lu_np_dispatch<a_cuda_data_type, base_type::m_size, base_type::n_size, base_type::this_solver_arrangement_a, max_threads_per_block, batches_per_block, base_type::this_sm_v>(
                    (a_cuda_data_type*)A, runtime_lda, status, get_thread_id());
            }

            // getrs_no_pivot
            template<class Solver = this_type>
            inline __device__ auto execute(a_data_type* A, const unsigned int runtime_lda, b_data_type* B, const unsigned int runtime_ldb = ldb)
                -> COMMONDX_STL_NAMESPACE::enable_if_t<function_of_v<Solver> == function::getrs_no_pivot, void> {

                static_assert(m_size == n_size, "getrs requires M=N");

                getrs_no_pivot_dispatch<a_cuda_data_type, m_size, nrhs, base_type::this_solver_arrangement_a, base_type::this_solver_arrangement_b, base_type::this_solver_transpose_v, max_threads_per_block, batches_per_block>(
                    (a_cuda_data_type*)A, runtime_lda, (a_cuda_data_type*)B, runtime_ldb, get_thread_id());
            }

            // gesv_no_pivot
            template<class Solver = this_type>
            inline __device__ auto execute(a_data_type* A, const unsigned int runtime_lda, b_data_type* B, const unsigned int runtime_ldb, status_type* status)
                -> COMMONDX_STL_NAMESPACE::enable_if_t<function_of_v<Solver> == function::gesv_no_pivot, void> {

                static_assert(m_size == n_size, "gesv requires M=N");

                lu_np_dispatch<a_cuda_data_type, base_type::m_size, base_type::n_size, base_type::this_solver_arrangement_a, max_threads_per_block, batches_per_block, base_type::this_sm_v>(
                    (a_cuda_data_type*)A, runtime_lda, status, get_thread_id());

                getrs_no_pivot_dispatch<a_cuda_data_type, m_size, nrhs, base_type::this_solver_arrangement_a, base_type::this_solver_arrangement_b, base_type::this_solver_transpose_v, max_threads_per_block, batches_per_block>(
                    (a_cuda_data_type*)A, runtime_lda, (a_cuda_data_type*)B, runtime_ldb, get_thread_id());
            }


            // Helpers for adding lda from operator
            // potrf, getrf_no_pivot
            template<class Solver = this_type>
            inline __device__ void execute(a_data_type* A, status_type* status) {
                execute(A, lda, status);
            }

            // trsm, potrs, getrs_no_pivot
            template<class Solver = this_type>
            inline __device__ void execute(a_data_type* A, b_data_type* B, unsigned int runtime_ldb=ldb) {
                execute(A, lda, B, runtime_ldb);
            }

            // posv, gesv_no_pivot
            template<class Solver = this_type>
            inline __device__ void execute(a_data_type* A, b_data_type* B, status_type* status) {
                execute(A, lda, B, ldb, status);
            }
            template<class Solver = this_type>
            inline __device__ void execute(a_data_type* A, b_data_type* B, const unsigned int runtime_ldb, status_type* status) {
                execute(A, lda, B, runtime_ldb, status);
            }
            template<class Solver = this_type>
            inline __device__ void execute(a_data_type* A, const unsigned int runtime_lda, b_data_type* B, status_type* status) {
                execute(A, runtime_lda, B, ldb, status);
            }

            static constexpr unsigned int suggested_batches_per_block = get_suggested_batches_per_block();

            static constexpr dim3 suggested_block_dim = get_suggested_block_dim();
            static constexpr dim3 block_dim           = get_block_dim();

            static constexpr unsigned int shared_memory_size = get_shared_memory_size();

            static constexpr unsigned int max_threads_per_block         = block_dim.x * block_dim.y * block_dim.z;
            static constexpr unsigned int min_blocks_per_multiprocessor = 1;

            static constexpr auto type        = base_type::this_solver_type_v;
            static constexpr auto a_arrangement = base_type::this_solver_arrangement_a;
            static constexpr auto b_arrangement = base_type::this_solver_arrangement_b;
            //static constexpr auto transpose   = base_type::this_solver_transpose_v; // only non_trans is support for POTR
            static constexpr auto fill_mode   = base_type::this_solver_fill_mode_v;
            static constexpr auto sm          = base_type::this_sm_v;

            using a_precision = typename base_type::this_solver_precision::a_type;
            using b_precision = typename base_type::this_solver_precision::b_type;
            using x_precision = typename base_type::this_solver_precision::x_type;
        };
    } // namespace detail
} // namespace cusolverdx

#endif // CUSOLVERDX_DETAIL_EXECUTION_HPP
