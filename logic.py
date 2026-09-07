"""
Logic components for Pokemon Emerald Version (Flit's ver.)
"""
from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, List
from typing_extensions import override

from rule_builder.rules import (Rule, CanReachEntrance, Has, HasAll, HasAny, HasGroupUnique, HasFromListUnique, OptionFilter, True_, False_)

from .constants import GAME_NAME
from .options import NormanCount, NormanRequirement, HoennEliteFourRequirement, HoennEliteFourCount

if TYPE_CHECKING:
    from . import PokemonEmeraldFlitWorld


BADGE_REQUIREMENTS: Dict[str, str] = {
    "Cut": "Stone Badge",
    "Fly": "Feather Badge",
    "Surf": "Balance Badge",
    "Strength": "Heat Badge",
    "Flash": "Knuckle Badge",
    "Rock Smash": "Dynamo Badge",
    "Waterfall": "Rain Badge",
    "Dive": "Mind Badge",
}

GYMS: List[str] = [
    "Defeat ROXANNE",
    "Defeat BRAWLY",
    "Defeat WATTSON",
    "Defeat FLANNERY",
    "Defeat NORMAN",
    "Defeat WINONA",
    "Defeat TATE AND LIZA",
    "Defeat JUAN"
]

@dataclass
class CanGoal(Rule["PokemonEmeraldFlitWorld"], game=GAME_NAME):
    @override
    def _instantiate(self, world: "PokemonEmeraldFlitWorld") -> Rule.Resolved:
        return self.Resolved(world.options.goals, player=world.player)
    
    @override
    class Resolved(Rule.Resolved):
        goals: set

@dataclass
class HasNBadges(Rule["PokemonEmeraldFlitWorld"], game=GAME_NAME):
    count: int

    @override
    def _instantiate(self, world: "PokemonEmeraldFlitWorld") -> Rule.Resolved:
        return HasGroupUnique("Badges", self.count).resolve(world)

@dataclass
class HasNGyms(Rule["PokemonEmeraldFlitWorld"], game=GAME_NAME):
    count: int

    @override
    def _instantiate(self, world: "PokemonEmeraldFlitWorld") -> Rule.Resolved:
        return HasFromListUnique(*GYMS, count=self.count).resolve(world)

@dataclass
class HasBadgeRequirement(Rule["PokemonEmeraldFlitWorld"], game=GAME_NAME):
    hm: str

    @override
    def _instantiate(self, world: "PokemonEmeraldFlitWorld") -> Rule.Resolved:
        if self.hm in world.options.remove_badge_requirement.value:
            return True_().resolve(world)
        return Has(BADGE_REQUIREMENTS[self.hm]).resolve(world)

@dataclass
class CanCut(Rule["PokemonEmeraldFlitWorld"], game=GAME_NAME):
    @override
    def _instantiate(self, world: "PokemonEmeraldFlitWorld") -> Rule.Resolved:
        rule = Has("HM01 Cut")
        return (rule & HasBadgeRequirement("Cut")).resolve(world)

@dataclass
class CanFly(Rule["PokemonEmeraldFlitWorld"], game=GAME_NAME):
    @override
    def _instantiate(self, world: "PokemonEmeraldFlitWorld") -> Rule.Resolved:
        rule = Has("HM02 Fly")
        return (rule & HasBadgeRequirement("Fly")).resolve(world)

@dataclass
class CanSurf(Rule["PokemonEmeraldFlitWorld"], game=GAME_NAME):
    @override
    def _instantiate(self, world: "PokemonEmeraldFlitWorld") -> Rule.Resolved:
        rule = Has("HM03 Surf")
        return (rule & HasBadgeRequirement("Surf")).resolve(world)

@dataclass
class CanStrength(Rule["PokemonEmeraldFlitWorld"], game=GAME_NAME):
    @override
    def _instantiate(self, world: "PokemonEmeraldFlitWorld") -> Rule.Resolved:
        rule = Has("HM04 Strength")
        return (rule & HasBadgeRequirement("Strength")).resolve(world)

@dataclass
class CanFlash(Rule["PokemonEmeraldFlitWorld"], game=GAME_NAME):
    @override
    def _instantiate(self, world: "PokemonEmeraldFlitWorld") -> Rule.Resolved:
        rule = Has("HM05 Flash")
        return (rule & HasBadgeRequirement("Flash")).resolve(world)

@dataclass
class CanRockSmash(Rule["PokemonEmeraldFlitWorld"], game=GAME_NAME):
    @override
    def _instantiate(self, world: "PokemonEmeraldFlitWorld") -> Rule.Resolved:
        rule = Has("HM06 Rock Smash")
        return (rule & HasBadgeRequirement("Rock Smash")).resolve(world)

@dataclass
class CanWaterfall(Rule["PokemonEmeraldFlitWorld"], game=GAME_NAME):
    @override
    def _instantiate(self, world: "PokemonEmeraldFlitWorld") -> Rule.Resolved:
        rule = Has("HM07 Waterfall")
        return (rule & HasBadgeRequirement("Waterfall")).resolve(world)

@dataclass
class CanDive(Rule["PokemonEmeraldFlitWorld"], game=GAME_NAME):
    @override
    def _instantiate(self, world: "PokemonEmeraldFlitWorld") -> Rule.Resolved:
        rule = Has("HM08 Dive")
        return (rule & HasBadgeRequirement("Dive")).resolve(world)

@dataclass
class HasPetalburgGymRequirements(Rule["PokemonEmeraldFlitWorld"], game=GAME_NAME):
    @override
    def _instantiate(self, world: "PokemonEmeraldFlitWorld") -> Rule.Resolved:
        if world.options.norman_requirement == NormanRequirement.option_badges:
            return HasNBadges(world.options.norman_count.value).resolve(world)
        elif world.options.norman_requirement == NormanRequirement.option_gyms:
            return HasNGyms(world.options.norman_count.value).resolve(world)
        return False_().resolve(world)

@dataclass
class HasEliteFourRequirements(Rule["PokemonEmeraldFlitWorld"], game=GAME_NAME):
    @override
    def _instantiate(self, world: "PokemonEmeraldFlitWorld") -> Rule.Resolved:
        if world.options.e4_requirement == HoennEliteFourRequirement.option_badges:
            return HasNBadges(world.options.e4_count.value).resolve(world)
        elif world.options.e4_requirement == HoennEliteFourRequirement.option_gyms:
            return HasNGyms(world.options.e4_count.value).resolve(world)
        return False_().resolve(world)

@dataclass
class HasTerraMarineCaveRequirements(Rule["PokemonEmeraldFlitWorld"], game=GAME_NAME):
    event: str

    @override
    def _instantiate(self, world: "PokemonEmeraldFlitWorld") -> Rule.Resolved:
        rule = HasAll(
            "Enter HALL OF FAME",
            "Liberate WEATHER INSTITUTE",  # needed so that the scientist can reveal the cave locations
            event
        )
        # all possible Marine Cave locations are underwater
        if event.startswith("MARINE CAVE: "):
            rule = rule & HasDive()
        return rule.resolve(world)
