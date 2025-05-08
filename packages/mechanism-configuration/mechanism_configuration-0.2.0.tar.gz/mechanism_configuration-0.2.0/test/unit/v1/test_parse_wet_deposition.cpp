#include <gtest/gtest.h>

#include <mechanism_configuration/v1/parser.hpp>

using namespace mechanism_configuration;

TEST(ParserBase, CanParseValidWetDepositionReaction)
{
  v1::Parser parser;
  std::vector<std::string> extensions = { ".json", ".yaml" };
  for (auto& extension : extensions)
  {
    auto parsed = parser.Parse(std::string("v1_unit_configs/reactions/wet_deposition/valid") + extension);
    EXPECT_TRUE(parsed);
    v1::types::Mechanism mechanism = *parsed;

    EXPECT_EQ(mechanism.reactions.wet_deposition.size(), 2);

    EXPECT_EQ(mechanism.reactions.wet_deposition[0].name, "rxn cloud");
    EXPECT_EQ(mechanism.reactions.wet_deposition[0].aerosol_phase, "cloud");
    EXPECT_EQ(mechanism.reactions.wet_deposition[0].scaling_factor, 12.3);
    EXPECT_EQ(mechanism.reactions.wet_deposition[0].unknown_properties.size(), 1);
    EXPECT_EQ(mechanism.reactions.wet_deposition[0].unknown_properties["__comment"], "Tuxedo cats are the best");

    EXPECT_EQ(mechanism.reactions.wet_deposition[1].name, "rxn cloud2");
    EXPECT_EQ(mechanism.reactions.wet_deposition[1].aerosol_phase, "cloud");
    EXPECT_EQ(mechanism.reactions.wet_deposition[1].scaling_factor, 1);
  }
}

TEST(ParserBase, WetDepositionDetectsUnknownPhase)
{
  v1::Parser parser;
  std::vector<std::string> extensions = { ".json", ".yaml" };
  for (auto& extension : extensions)
  {
    std::string file = std::string("v1_unit_configs/reactions/wet_deposition/missing_phase") + extension;
    auto parsed = parser.Parse(file);
    EXPECT_FALSE(parsed);
    EXPECT_EQ(parsed.errors.size(), 1);
    EXPECT_EQ(parsed.errors[0].first, ConfigParseStatus::UnknownPhase);
    for (auto& error : parsed.errors)
    {
      std::cout << error.second << " " << configParseStatusToString(error.first) << std::endl;
    }
  }
}