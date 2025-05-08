#include <gtest/gtest.h>

#include <mechanism_configuration/v1/parser.hpp>

using namespace mechanism_configuration;

TEST(ParserBase, CanParseValidSpecies)
{
  v1::Parser parser;
  std::vector<std::string> extensions = { ".json", ".yaml" };
  for (auto& extension : extensions)
  {
    auto parsed = parser.Parse(std::string("v1_unit_configs/species/valid_species") + extension);
    EXPECT_TRUE(parsed);
    v1::types::Mechanism mechanism = *parsed;
    EXPECT_EQ(mechanism.species.size(), 3);

    EXPECT_EQ(mechanism.species[0].name, "A");
    EXPECT_EQ(mechanism.species[0].unknown_properties.size(), 2);
    EXPECT_EQ(mechanism.species[0].unknown_properties["__absolute tolerance"], "1.0e-30");
    EXPECT_EQ(mechanism.species[0].unknown_properties["__long name"], "ozone");
    EXPECT_EQ(mechanism.species[0].tracer_type.has_value(), true);
    EXPECT_EQ(mechanism.species[0].tracer_type.value(), "AEROSOL");

    EXPECT_EQ(mechanism.species[1].name, "H2O2");
    EXPECT_EQ(mechanism.species[1].henrys_law_constant_298.has_value(), true);
    EXPECT_EQ(mechanism.species[1].henrys_law_constant_298.value(), 1.011596348);
    EXPECT_EQ(mechanism.species[1].henrys_law_constant_exponential_factor.has_value(), true);
    EXPECT_EQ(mechanism.species[1].henrys_law_constant_exponential_factor.value(), 6340);
    EXPECT_EQ(mechanism.species[1].diffusion_coefficient.has_value(), true);
    EXPECT_EQ(mechanism.species[1].diffusion_coefficient.value(), 1.46e-05);
    EXPECT_EQ(mechanism.species[1].n_star.has_value(), true);
    EXPECT_EQ(mechanism.species[1].n_star.value(), 1.74);
    EXPECT_EQ(mechanism.species[1].molecular_weight.has_value(), true);
    EXPECT_EQ(mechanism.species[1].molecular_weight.value(), 0.0340147);
    EXPECT_EQ(mechanism.species[1].density.has_value(), true);
    EXPECT_EQ(mechanism.species[1].density.value(), 1000.0);
    EXPECT_EQ(mechanism.species[1].unknown_properties.size(), 1);
    EXPECT_EQ(mechanism.species[1].unknown_properties["__absolute tolerance"], "1.0e-10");

    EXPECT_EQ(mechanism.species[2].name, "aerosol stuff");
    EXPECT_EQ(mechanism.species[2].molecular_weight.has_value(), true);
    EXPECT_EQ(mechanism.species[2].molecular_weight.value(), 0.5);
    EXPECT_EQ(mechanism.species[2].density.has_value(), true);
    EXPECT_EQ(mechanism.species[2].density.value(), 1000.0);
    EXPECT_EQ(mechanism.species[2].unknown_properties.size(), 1);
    EXPECT_EQ(mechanism.species[2].unknown_properties["__absolute tolerance"], "1.0e-20");
  }
}

TEST(ParserBase, DetectsDuplicateSpecies)
{
  v1::Parser parser;
  std::vector<std::string> extensions = { ".json", ".yaml" };
  for (auto& extension : extensions)
  {
    std::string file = std::string("v1_unit_configs/species/duplicate_species") + extension;
    auto parsed = parser.Parse(file);
    EXPECT_FALSE(parsed);
    EXPECT_EQ(parsed.errors.size(), 1);
    EXPECT_EQ(parsed.errors[0].first, ConfigParseStatus::DuplicateSpeciesDetected);
    for (auto& error : parsed.errors)
    {
      std::cout << error.second << " " << configParseStatusToString(error.first) << std::endl;
    }
  }
}

TEST(ParserBase, DetectsMissingRequiredKeys)
{
  v1::Parser parser;
  std::vector<std::string> extensions = { ".json", ".yaml" };
  for (auto& extension : extensions)
  {
    std::string file = std::string("v1_unit_configs/species/missing_required_key") + extension;
    auto parsed = parser.Parse(file);
    EXPECT_FALSE(parsed);
    EXPECT_EQ(parsed.errors.size(), 2);
    EXPECT_EQ(parsed.errors[0].first, ConfigParseStatus::RequiredKeyNotFound);
    EXPECT_EQ(parsed.errors[1].first, ConfigParseStatus::InvalidKey);
    for (auto& error : parsed.errors)
    {
      std::cout << error.second << " " << configParseStatusToString(error.first) << std::endl;
    }
  }
}

TEST(ParserBase, DetectsInvalidKeys)
{
  v1::Parser parser;
  std::vector<std::string> extensions = { ".json", ".yaml" };
  for (auto& extension : extensions)
  {
    std::string file = std::string("v1_unit_configs/species/invalid_key") + extension;
    auto parsed = parser.Parse(file);
    EXPECT_FALSE(parsed);
    EXPECT_EQ(parsed.errors.size(), 1);
    EXPECT_EQ(parsed.errors[0].first, ConfigParseStatus::InvalidKey);
    for (auto& error : parsed.errors)
    {
      std::cout << error.second << " " << configParseStatusToString(error.first) << std::endl;
    }
  }
}
