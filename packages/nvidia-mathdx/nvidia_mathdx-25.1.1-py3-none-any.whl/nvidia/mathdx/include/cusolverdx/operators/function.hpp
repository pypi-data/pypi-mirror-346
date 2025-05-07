// Copyright (c) 2024, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
//
// NVIDIA CORPORATION and its licensors retain all intellectual property
// and proprietary rights in and to this software, related documentation
// and any modifications thereto.  Any use, reproduction, disclosure or
// distribution of this software and related documentation without an express
// license agreement from NVIDIA CORPORATION is strictly prohibited.

#ifndef CUSOLVERDX_OPERATORS_FUNCTION_HPP
#define CUSOLVERDX_OPERATORS_FUNCTION_HPP

#include "commondx/detail/expressions.hpp"
#include "commondx/traits/detail/is_operator_fd.hpp"
#include "commondx/traits/detail/get_operator_fd.hpp"

#include "cusolverdx/operators/operator_type.hpp"

namespace cusolverdx {
    enum class function
    {
        potrf,               // Cholesky Factorization
        potrs,               // Cholesky Solve
        posv,                // Cholesky Factor and Solve
        getrf_no_pivot,      // LU Factorization
        getrs_no_pivot,      // LU Solve
        gesv_no_pivot,       // LU Factor and Solve

        trsm, // Temporarily exported until provided by cuBLASDx
    };

    inline constexpr auto potrf               = function::potrf;
    inline constexpr auto potrs               = function::potrs;
    inline constexpr auto posv                = function::posv;
    inline constexpr auto getrf_no_pivot      = function::getrf_no_pivot;
    inline constexpr auto getrs_no_pivot      = function::getrs_no_pivot;
    inline constexpr auto gesv_no_pivot       = function::gesv_no_pivot;
    inline constexpr auto trsm                = function::trsm;

    template<function Value>
    struct Function: commondx::detail::operator_expression {
        static_assert((Value == potrf) || (Value == potrs) || (Value == posv) || (Value == getrf_no_pivot) || (Value == getrs_no_pivot) || (Value == gesv_no_pivot) || (Value == trsm), "Supported functions are potrf, getrf");

        static constexpr function value = Value;
    };

    namespace detail {
        using default_function_operator = Function<potrf>;

        template<function Value>
        struct is_cholesky: COMMONDX_STL_NAMESPACE::integral_constant<bool, (Value == potrf || Value == potrs || Value == posv)> {};

        template<function Value>
        struct is_lu: COMMONDX_STL_NAMESPACE::integral_constant<bool, (Value == getrf_no_pivot || Value == getrs_no_pivot || Value == gesv_no_pivot)> {};

        template<function Value>
        struct is_solver: COMMONDX_STL_NAMESPACE::integral_constant<bool, (Value == potrs || Value == posv || Value == gesv_no_pivot || Value == getrs_no_pivot)> {};


    } // namespace detail
} // namespace cusolverdx

namespace commondx::detail {
    template<cusolverdx::function Value>
    struct is_operator<cusolverdx::operator_type, cusolverdx::operator_type::function, cusolverdx::Function<Value>>: COMMONDX_STL_NAMESPACE::true_type {};

    template<cusolverdx::function Value>
    struct get_operator_type<cusolverdx::Function<Value>> {
        static constexpr cusolverdx::operator_type value = cusolverdx::operator_type::function;
    };
} // namespace commondx::detail

#endif // CUSOLVERDX_OPERATORS_FUNCTION_HPP
