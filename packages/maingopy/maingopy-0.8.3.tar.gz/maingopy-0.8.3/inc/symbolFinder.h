/**********************************************************************************
 * Copyright (c) 2019 Process Systems Engineering (AVT.SVT), RWTH Aachen University
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License 2.0 which is available at
 * http://www.eclipse.org/legal/epl-2.0.
 *
 * SPDX-License-Identifier: EPL-2.0
 *
 * @file symbolFinder.h
 *
 * @brief File containing the SymbolFinder class that detects all symbols occurring
 *        in visited expression.
 *
 **********************************************************************************/

#pragma once

#include "symbol_table.hpp"

#include "expression.hpp"


namespace maingo {


using namespace ale;

/**
* @class SymbolFinder
* @brief Visitor for finding all symbols used in an expression
*/
class SymbolFinder {
  public:
    /**
	* @brief Constructor
	*
	* @param[in] symbols is the symbol_table for symbol lookup
	*/
    SymbolFinder(symbol_table& symbols):
        _symbols(symbols){};

    /**
	* @name Dispatch functions
	* @brief Functions dispatching to visit functions
	*/
    /**@{*/
    template <typename TType>
    void dispatch(expression<TType>& expr)
    {
        dispatch(expr.get());
    }


    template <typename TType>
    void dispatch(value_node<TType>* node)
    {
        std::visit(*this, node->get_variant());
    }


    template <typename TType>
    void dispatch(value_symbol<TType>* sym)
    {
        std::visit(*this, sym->get_value_variant());
    }
    /**@}*/

    /**
	* @name Visit specializations for terminal nodes and symbols
	* @brief Functions visiting specific terminal node and symbol types
	*/
    /**@{*/
    template <typename TType>
    void operator()(constant_node<TType>* node)
    {
    }


    template <typename TType>
    void operator()(parameter_node<TType>* node)
    {
        if (std::find(_scopeStack.begin(), _scopeStack.end(), node->name) != _scopeStack.end()) {
            mScopedSymbols.insert(node->name);
            return;
        }
        auto sym = _symbols.resolve<TType>(node->name);
        if (sym) {
            dispatch(sym);
            return;
        }
        mIlldefinedSymbols.insert(node->name);
    }


    template <typename TType>
    void operator()(parameter_symbol<TType>* sym)
    {
        mFixedSymbols.insert(sym->m_name);
    }


    template <typename TType>
    void operator()(variable_symbol<TType>* sym)
    {
        mDefinedSymbols.insert(sym->m_name);
    }

    template <typename TType>
    void operator()(expression_symbol<TType>* sym)
    {
        dispatch(sym->m_value.get());
    }
    /**@}*/

    /**
	* @name Traverse functions
	* @brief Functions for traversing non-terminal nodes
	*/
    /**@{*/
    template <typename TType>
    void traverse(unary_node<TType>* node)
    {
        dispatch(node->template get_child<0>());
    }


    template <typename TType, typename UType>
    void traverse(binary_node<TType, UType>* node)
    {
        dispatch(node->template get_child<0>());
        dispatch(node->template get_child<1>());
    }


    template <typename TType, typename UType, typename VType>
    void traverse(ternary_node<TType, UType, VType>* node)
    {
        dispatch(node->template get_child<0>());
        dispatch(node->template get_child<1>());
        dispatch(node->template get_child<2>());
    }


    template <typename TType, typename UType, typename VType, typename WType>
    void traverse(quaternary_node<TType, UType, VType, WType>* node)
    {
        dispatch(node->template get_child<0>());
        dispatch(node->template get_child<1>());
        dispatch(node->template get_child<2>());
        dispatch(node->template get_child<3>());
    }


    template <typename TType, typename UType, typename VType, typename WType, typename XType>
    void traverse(quinary_node<TType, UType, VType, WType, XType>* node)
    {
        dispatch(node->template get_child<0>());
        dispatch(node->template get_child<1>());
        dispatch(node->template get_child<2>());
        dispatch(node->template get_child<3>());
        dispatch(node->template get_child<4>());
    }


    template <typename TType, typename UType, typename VType, typename WType, typename XType, typename YType>
    void traverse(senary_node<TType, UType, VType, WType, XType, YType>* node)
    {
        dispatch(node->template get_child<0>());
        dispatch(node->template get_child<1>());
        dispatch(node->template get_child<2>());
        dispatch(node->template get_child<3>());
        dispatch(node->template get_child<4>());
        dispatch(node->template get_child<5>());
    }


    template <typename TType, typename UType, typename VType, typename WType, typename XType, typename YType, typename ZType>
    void traverse(septenary_node<TType, UType, VType, WType, XType, YType, ZType>* node)
    {
        dispatch(node->template get_child<0>());
        dispatch(node->template get_child<1>());
        dispatch(node->template get_child<2>());
        dispatch(node->template get_child<3>());
        dispatch(node->template get_child<4>());
        dispatch(node->template get_child<5>());
        dispatch(node->template get_child<6>());
    }


    template <typename TType, typename UType, typename VType, typename WType, typename XType, typename YType, typename ZType, typename AType>
    void traverse(octonary_node<TType, UType, VType, WType, XType, YType, ZType, AType>* node)
    {
        dispatch(node->template get_child<0>());
        dispatch(node->template get_child<1>());
        dispatch(node->template get_child<2>());
        dispatch(node->template get_child<3>());
        dispatch(node->template get_child<4>());
        dispatch(node->template get_child<5>());
        dispatch(node->template get_child<6>());
        dispatch(node->template get_child<7>());
    }


    template <typename TType, typename UType, typename VType, typename WType, typename XType, typename YType, typename ZType, typename AType, typename BType>
    void traverse(novenary_node<TType, UType, VType, WType, XType, YType, ZType, AType, BType>* node)
    {
        dispatch(node->template get_child<0>());
        dispatch(node->template get_child<1>());
        dispatch(node->template get_child<2>());
        dispatch(node->template get_child<3>());
        dispatch(node->template get_child<4>());
        dispatch(node->template get_child<5>());
        dispatch(node->template get_child<6>());
        dispatch(node->template get_child<7>());
        dispatch(node->template get_child<8>());
    }


    template <typename TType, typename UType, typename VType, typename WType, typename XType, typename YType, typename ZType, typename AType, typename BType, typename CType, typename DType>
    void traverse(undenary_node<TType, UType, VType, WType, XType, YType, ZType, AType, BType, CType, DType>* node)
    {
        dispatch(node->template get_child<0>());
        dispatch(node->template get_child<1>());
        dispatch(node->template get_child<2>());
        dispatch(node->template get_child<3>());
        dispatch(node->template get_child<4>());
        dispatch(node->template get_child<5>());
        dispatch(node->template get_child<6>());
        dispatch(node->template get_child<7>());
        dispatch(node->template get_child<8>());
        dispatch(node->template get_child<9>());
        dispatch(node->template get_child<10>());
    }


    template <typename TTypes>
    void traverse(nary_node<TTypes>* node)
    {
        for (auto it = node->children.begin(); it != node->children.end(); ++it) {
            dispatch(it->get());
        }
    }
    /**@}*/

    /**
	* @name Visit specializations for non-terminal nodes
	* @brief Functions visiting specific non-terminal node types
	*/
    /**@{*/
    template <typename TType>
    void operator()(entry_node<TType>* node)
    {
        traverse(node);
    }

    void operator()(minus_node* node) { traverse(node); }
    void operator()(inverse_node* node) { traverse(node); }

    void operator()(addition_node* node) { traverse(node); }
    void operator()(multiplication_node* node) { traverse(node); }
    void operator()(exponentiation_node* node) { traverse(node); }
    void operator()(min_node* node) { traverse(node); }
    void operator()(max_node* node) { traverse(node); }
    void operator()(sum_div_node* node) { traverse(node); };
    void operator()(xlog_sum_node* node) { traverse(node); };

    void operator()(exp_node* node) { traverse(node); }
    void operator()(log_node* node) { traverse(node); }
    void operator()(sqrt_node* node) { traverse(node); }
    void operator()(sin_node* node) { traverse(node); }
    void operator()(asin_node* node) { traverse(node); }
    void operator()(cos_node* node) { traverse(node); }
    void operator()(acos_node* node) { traverse(node); }
    void operator()(tan_node* node) { traverse(node); }
    void operator()(atan_node* node) { traverse(node); }

    void operator()(lmtd_node* node) { traverse(node); }
    void operator()(rlmtd_node* node) { traverse(node); }
    void operator()(xexpax_node* node) { traverse(node); }
    void operator()(arh_node* node) { traverse(node); }
    void operator()(lb_func_node* node) { traverse(node); }
    void operator()(ub_func_node* node) { traverse(node); }
    void operator()(bounding_func_node* node) { traverse(node); }
    void operator()(ale::squash_node* node) { traverse(node); }
    void operator()(ale::regnormal_node* node) { traverse(node); }

    void operator()(xlogx_node* node) { traverse(node); }
    void operator()(abs_node* node) { traverse(node); }
    void operator()(xabsx_node* node) { traverse(node); }
    void operator()(cosh_node* node) { traverse(node); }
    void operator()(sinh_node* node) { traverse(node); }
    void operator()(tanh_node* node) { traverse(node); }
    void operator()(coth_node* node) { traverse(node); }
    void operator()(acosh_node* node) { traverse(node); }
    void operator()(asinh_node* node) { traverse(node); }
    void operator()(atanh_node* node) { traverse(node); }
    void operator()(acoth_node* node) { traverse(node); }
    void operator()(erf_node* node) { traverse(node); }
    void operator()(erfc_node* node) { traverse(node); }
    void operator()(pos_node* node) { traverse(node); }
    void operator()(neg_node* node) { traverse(node); }
    void operator()(xexpy_node* node) { traverse(node); }
    void operator()(norm2_node* node) { traverse(node); }

    void operator()(schroeder_ethanol_p_node* node) { traverse(node); }
    void operator()(schroeder_ethanol_rhovap_node* node) { traverse(node); }
    void operator()(schroeder_ethanol_rholiq_node* node) { traverse(node); }

    void operator()(nrtl_dtau_node* node) { traverse(node); }
    void operator()(nrtl_tau_node* node) { traverse(node); }
    void operator()(nrtl_g_node* node) { traverse(node); }
    void operator()(nrtl_gtau_node* node) { traverse(node); }
    void operator()(nrtl_gdtau_node* node) { traverse(node); }
    void operator()(nrtl_dgtau_node* node) { traverse(node); }

    void operator()(ext_antoine_psat_node* node) { traverse(node); }
    void operator()(antoine_psat_node* node) { traverse(node); }
    void operator()(wagner_psat_node* node) { traverse(node); }
    void operator()(ik_cape_psat_node* node) { traverse(node); }

    void operator()(aspen_hig_node* node) { traverse(node); }
    void operator()(nasa9_hig_node* node) { traverse(node); }
    void operator()(dippr107_hig_node* node) { traverse(node); }
    void operator()(dippr127_hig_node* node) { traverse(node); }

    void operator()(antoine_tsat_node* node) { traverse(node); }

    void operator()(watson_dhvap_node* node) { traverse(node); }
    void operator()(dippr106_dhvap_node* node) { traverse(node); }

    void operator()(cost_turton_node* node) { traverse(node); }

    void operator()(covar_matern_1_node* node) { traverse(node); }
    void operator()(covar_matern_3_node* node) { traverse(node); }
    void operator()(covar_matern_5_node* node) { traverse(node); }
    void operator()(covar_sqrexp_node* node) { traverse(node); }

    void operator()(gpdf_node* node) { traverse(node); }

    template <typename TType>
    void operator()(sum_node<TType>* node)
    {
        _scopeStack.push_back(node->name);
        traverse(node);
        _scopeStack.pop_back();
    }


    template <typename TType>
    void operator()(set_min_node<TType>* node)
    {
        _scopeStack.push_back(node->name);
        traverse(node);
        _scopeStack.pop_back();
    }


    template <typename TType>
    void operator()(set_max_node<TType>* node)
    {
        _scopeStack.push_back(node->name);
        traverse(node);
        _scopeStack.pop_back();
    }

    void operator()(index_minus_node* node) { traverse(node); }

    void operator()(index_addition_node* node) { traverse(node); }
    void operator()(index_multiplication_node* node) { traverse(node); }

    void operator()(negation_node* node) { traverse(node); }

    template <typename TType>
    void operator()(equal_node<TType>* node)
    {
        traverse(node);
    }
    template <typename TType>
    void operator()(less_node<TType>* node)
    {
        traverse(node);
    }
    template <typename TType>
    void operator()(less_equal_node<TType>* node)
    {
        traverse(node);
    }
    template <typename TType>
    void operator()(greater_node<TType>* node)
    {
        traverse(node);
    }
    template <typename TType>
    void operator()(greater_equal_node<TType>* node)
    {
        traverse(node);
    }

    void operator()(disjunction_node* node) { traverse(node); }
    void operator()(conjunction_node* node) { traverse(node); }

    void operator()(element_node* node) { traverse(node); };

    template <typename TType>
    void operator()(forall_node<TType>* node)
    {
        _scopeStack.push_back(node->name);
        traverse(node);
        _scopeStack.pop_back();
    }


    template <typename TType>
    void operator()(indicator_set_node<TType>* node)
    {
        _scopeStack.push_back(node->name);
        traverse(node);
        _scopeStack.pop_back();
    }

    void operator()(mid_node* node) { traverse(node); }
    /**@}*/

    std::set<std::string> mDefinedSymbols;    /*!< Symbols that are properly defined */
    std::set<std::string> mIlldefinedSymbols; /*!< Symbols that are ill-defined */
    std::set<std::string> mFixedSymbols;      /*!< Symbols with fixed value */
    std::set<std::string> mScopedSymbols;     /*!< Symbols in local scopes */

  private:
    symbol_table& _symbols;              /*!< symbol_table for symbol lookup */
    std::deque<std::string> _scopeStack; /*!< Container for scope tracking */
};


}    // namespace maingo