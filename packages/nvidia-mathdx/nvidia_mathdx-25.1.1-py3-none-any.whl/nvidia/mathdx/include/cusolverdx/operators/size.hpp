// Copyright (c) 2024, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
//
// NVIDIA CORPORATION and its licensors retain all intellectual property
// and proprietary rights in and to this software, related documentation
// and any modifications thereto.  Any use, reproduction, disclosure or
// distribution of this software and related documentation without an express
// license agreement from NVIDIA CORPORATION is strictly prohibited.

#ifndef CUSOLVERDX_OPERATORS_SIZE_HPP
#define CUSOLVERDX_OPERATORS_SIZE_HPP

#include "commondx/operators/size3d.hpp"
#include "commondx/traits/detail/is_operator_fd.hpp"
#include "commondx/traits/detail/get_operator_fd.hpp"

#include "cusolverdx/operators/operator_type.hpp"

namespace cusolverdx {
    template<unsigned int M, unsigned int N = M, unsigned int NRHS = 1>
    struct Size: public commondx::Size3D<M, N, NRHS> {
        static_assert(M > 0, "First dimension must be greater than 0");
        static_assert(N > 0, "Second dimension size must be greater than 0");
        static_assert(NRHS > 0, "Third dimension size must be greater than 0");

        static constexpr unsigned int m = M;
        static constexpr unsigned int n = N;
        static constexpr unsigned int nrhs = NRHS;
    };
} // namespace cusolverdx


namespace commondx::detail {
    template<unsigned int M, unsigned int N, unsigned int NRHS>
    struct is_operator<cusolverdx::operator_type, cusolverdx::operator_type::size, cusolverdx::Size<M, N, NRHS>>:
        COMMONDX_STL_NAMESPACE::true_type {};

    template<unsigned int M, unsigned int N, unsigned int NRHS>
    struct get_operator_type<cusolverdx::Size<M, N, NRHS>> {
        static constexpr cusolverdx::operator_type value = cusolverdx::operator_type::size;
    };
} // namespace commondx::detail

#endif // CUSOLVERDX_OPERATORS_SIZE_HPP
