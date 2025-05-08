// Copyright (C) 2023-2024 National Center for Atmospheric Research, University of Illinois at Urbana-Champaign
//
// SPDX-License-Identifier: Apache-2.0

#pragma once

#include <array>
#include <map>
#include <mechanism_configuration/mechanism.hpp>
#include <optional>
#include <string>
#include <unordered_map>
#include <vector>

namespace mechanism_configuration
{
  namespace v0
  {
    namespace types
    {
      struct Species
      {
        std::string name;
        std::optional<double> molecular_weight;
        std::optional<double> diffusion_coefficient;
        std::optional<double> absolute_tolerance;
        std::optional<std::string> tracer_type;
        /// @brief Unknown properties, prefixed with two underscores (__)
        std::unordered_map<std::string, std::string> unknown_properties;
      };

      struct Phase
      {
        std::string name;
        std::vector<std::string> species;
        /// @brief Unknown properties, prefixed with two underscores (__)
        std::unordered_map<std::string, std::string> unknown_properties;
      };

      struct ReactionComponent
      {
        std::string species_name;
        double coefficient{ 1.0 };
        /// @brief Unknown properties, prefixed with two underscores (__)
        std::unordered_map<std::string, std::string> unknown_properties;
      };

      struct Arrhenius
      {
        /// @brief Pre-exponential factor [(mol m−3)^(−(𝑛−1)) s−1]
        double A{ 1 };
        /// @brief Unitless exponential factor
        double B{ 0 };
        /// @brief Activation threshold, expected to be the negative activation energy divided by the boltzman constant
        ///        [-E_a / k_b), K]
        double C{ 0 };
        /// @brief A factor that determines temperature dependence [K]
        double D{ 300 };
        /// @brief A factor that determines pressure dependence [Pa-1]
        double E{ 0 };
        /// @brief A list of reactants
        std::vector<ReactionComponent> reactants;
        /// @brief A list of products
        std::vector<ReactionComponent> products;
        /// @brief Unknown properties, prefixed with two underscores (__)
        std::unordered_map<std::string, std::string> unknown_properties;
      };

      struct Troe
      {
        /// @brief low-pressure pre-exponential factor
        double k0_A = 1.0;
        /// @brief low-pressure temperature-scaling parameter
        double k0_B = 0.0;
        /// @brief low-pressure exponential factor
        double k0_C = 0.0;
        /// @brief high-pressure pre-exponential factor
        double kinf_A = 1.0;
        /// @brief high-pressure temperature-scaling parameter
        double kinf_B = 0.0;
        /// @brief high-pressure exponential factor
        double kinf_C = 0.0;
        /// @brief Troe F_c parameter
        double Fc = 0.6;
        /// @brief Troe N parameter
        double N = 1.0;
        /// @brief A list of reactants
        std::vector<ReactionComponent> reactants;
        /// @brief A list of products
        std::vector<ReactionComponent> products;
        /// @brief Unknown properties, prefixed with two underscores (__)
        std::unordered_map<std::string, std::string> unknown_properties;
      };

      struct TernaryChemicalActivation
      {
        /// @brief low-pressure pre-exponential factor
        double k0_A = 1.0;
        /// @brief low-pressure temperature-scaling parameter
        double k0_B = 0.0;
        /// @brief low-pressure exponential factor
        double k0_C = 0.0;
        /// @brief high-pressure pre-exponential factor
        double kinf_A = 1.0;
        /// @brief high-pressure temperature-scaling parameter
        double kinf_B = 0.0;
        /// @brief high-pressure exponential factor
        double kinf_C = 0.0;
        /// @brief TernaryChemicalActivation F_c parameter
        double Fc = 0.6;
        /// @brief TernaryChemicalActivation N parameter
        double N = 1.0;
        std::vector<ReactionComponent> reactants;
        /// @brief A list of products
        std::vector<ReactionComponent> products;
        /// @brief Unknown properties, prefixed with two underscores (__)
        std::unordered_map<std::string, std::string> unknown_properties;
      };

      struct Branched
      {
        /// @brief pre-exponential factor
        double X;
        /// @brief exponential factor
        double Y;
        /// @brief branching factor
        double a0;
        /// @brief number of heavy atoms in the RO2 reacting species (excluding the peroxy moiety)
        int n;
        /// @brief A list of reactants
        std::vector<ReactionComponent> reactants;
        /// @brief A list of nitrate products
        std::vector<ReactionComponent> nitrate_products;
        /// @brief A list of alkoxy products
        std::vector<ReactionComponent> alkoxy_products;
        /// @brief Unknown properties, prefixed with two underscores (__)
        std::unordered_map<std::string, std::string> unknown_properties;
      };

      struct Tunneling
      {
        /// @brief Pre-exponential factor [(mol m−3)^(−(𝑛−1)) s−1]
        double A = 1.0;
        /// @brief Linear temperature-dependent parameter [K]
        double B = 0.0;
        /// @brief Cubed temperature-dependent parameter [K^3]
        double C = 0.0;
        /// @brief A list of reactants
        std::vector<ReactionComponent> reactants;
        /// @brief A list of products
        std::vector<ReactionComponent> products;
        /// @brief Unknown properties, prefixed with two underscores (__)
        std::unordered_map<std::string, std::string> unknown_properties;
      };

      struct Surface
      {
        /// @brief Reaction probability (0-1) [unitless]
        double reaction_probability{ 1.0 };
        /// @brief A list of reactants
        ReactionComponent gas_phase_species;
        /// @brief A list of products
        std::vector<ReactionComponent> gas_phase_products;
        /// @brief An identifier, optional, uniqueness not enforced
        std::string name;
        /// @brief Unknown properties, prefixed with two underscores (__)
        std::unordered_map<std::string, std::string> unknown_properties;
      };

      struct UserDefined
      {
        /// @brief Scaling factor to apply to user-provided rate constants
        double scaling_factor{ 1.0 };
        /// @brief A list of reactants
        std::vector<ReactionComponent> reactants;
        /// @brief A list of products
        std::vector<ReactionComponent> products;
        /// @brief An identifier, optional, uniqueness not enforced
        std::string name;
        /// @brief Unknown properties, prefixed with two underscores (__)
        std::unordered_map<std::string, std::string> unknown_properties;
      };

      struct Reactions
      {
        std::vector<Arrhenius> arrhenius;
        std::vector<Branched> branched;
        std::vector<UserDefined> user_defined;
        std::vector<Surface> surface;
        std::vector<Troe> troe;
        std::vector<TernaryChemicalActivation> ternary_chemical_activation;
        std::vector<Tunneling> tunneling;
      };

      struct Mechanism : public ::mechanism_configuration::Mechanism
      {
        /// @brief An identifier, optional
        std::string name;
        std::vector<Species> species;
        std::vector<Phase> phases;
        Reactions reactions;
        double relative_tolerance{ 1e-6 };
      };

    }  // namespace types
  }  // namespace v0
}  // namespace mechanism_configuration