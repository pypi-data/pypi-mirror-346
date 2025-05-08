#pragma once

#include <mechanism_configuration/errors.hpp>
#include <mechanism_configuration/mechanism.hpp>
#include <memory>
#include <string>
#include <utility>
#include <vector>

namespace mechanism_configuration
{

  template<typename MechanismType = GlobalMechanism>
  struct ParserResult
  {
    std::unique_ptr<MechanismType> mechanism = nullptr;
    Errors errors;

    bool has_errors() const
    {
      return !errors.empty();
    }

    operator bool() const
    {
      return mechanism != nullptr && errors.empty();
    }

    MechanismType& operator*()
    {
      return *mechanism;
    }
  };
}  // namespace mechanism_configuration
