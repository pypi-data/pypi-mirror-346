from __future__ import annotations
import enum
from difflib import get_close_matches
from env.src.entities import *


class ResourceName(enum.Enum):
    Coal = "coal"
    IronOre = "iron-ore"
    CopperOre = "copper-ore"
    Stone = "stone"
    Water = "water"
    CrudeOil = "crude-oil"
    UraniumOre = "uranium-ore"

class PrototypeMetaclass(enum.EnumMeta):
    def __getattr__(cls, name):
        try:
            attr =  super().__getattr__(name)
            return attr
        except AttributeError:
            # Get all valid prototype names
            valid_names = [member.name for member in cls]

            # Find closest matches
            matches = get_close_matches(name, valid_names, n=3, cutoff=0.6)

            suggestion_msg = ""
            if matches:
                suggestion_msg = f". Did you mean: {', '.join(matches)}?"

            raise AttributeError(f"'{cls.__name__}' has no attribute '{name}'{suggestion_msg}")

class RecipeName(enum.Enum):
    """
    Recipe names that can be used in the game for fluids
    """
    NuclearFuelReprocessing = "nuclear-fuel-reprocessing"
    UraniumProcessing = "uranium-processing"
    SulfuricAcid = "sulfuric-acid" # Recipe for producing sulfuric acid with a chemical plant
    BasicOilProcessing = "basic-oil-processing" # Recipe for producing petroleum gas with a oil refinery
    AdvancedOilProcessing = "advanced-oil-processing" # Recipe for producing petroleum gas, heavy oil and light oil with a oil refinery
    CoalLiquefaction = "coal-liquefaction" # Recipe for producing petroleum gas in a oil refinery
    HeavyOilCracking = "heavy-oil-cracking" # Recipe for producing light oil in a chemical plant
    LightOilCracking = "light-oil-cracking" # Recipe for producing petroleum gas in a chemical plant

    SolidFuelFromHeavyOil = "solid-fuel-from-heavy-oil" # Recipe for producing solid fuel in a chemical plant
    SolidFuelFromLightOil = "solid-fuel-from-light-oil" # Recipe for producing solid fuel in a chemical plant
    SolidFuelFromPetroleumGas = "solid-fuel-from-petroleum-gas" # Recipe for producing solid fuel in a chemical plant

    FillCrudeOilBarrel = "fill-crude-oil-barrel"
    FillHeavyOilBarrel = "fill-heavy-oil-barrel"
    FillLightOilBarrel = "fill-light-oil-barrel"
    FillLubricantBarrel = "fill-lubricant-barrel"
    FillPetroleumGasBarrel = "fill-petroleum-gas-barrel"
    FillSulfuricAcidBarrel = "fill-sulfuric-acid-barrel"
    FillWaterBarrel = "fill-water-barrel"

    EmptyCrudeOilBarrel = "empty-crude-oil-barrel"
    EmptyHeavyOilBarrel = "empty-heavy-oil-barrel"
    EmptyLightOilBarrel = "empty-light-oil-barrel"
    EmptyLubricantBarrel = "empty-lubricant-barrel"
    EmptyPetroleumGasBarrel = "empty-petroleum-gas-barrel"
    EmptySulfuricAcidBarrel = "empty-sulfuric-acid-barrel"
    EmptyWaterBarrel = "empty-water-barrel"


class Prototype(enum.Enum, metaclass=PrototypeMetaclass):

    AssemblingMachine1 = "assembling-machine-1", AssemblingMachine
    AssemblingMachine2 = "assembling-machine-2", AdvancedAssemblingMachine
    AssemblingMachine3 = "assembling-machine-3", AdvancedAssemblingMachine
    Centrifuge = "centrifuge", AssemblingMachine

    BurnerInserter = "burner-inserter", BurnerInserter
    FastInserter = "fast-inserter", Inserter
    ExpressInserter = "express-inserter", Inserter

    LongHandedInserter = "long-handed-inserter", Inserter
    StackInserter = "stack-inserter", Inserter
    StackFilterInserter = "stack-filter-inserter", FilterInserter
    FilterInserter = "filter-inserter", FilterInserter

    Inserter = "inserter", Inserter


    BurnerMiningDrill = "burner-mining-drill", BurnerMiningDrill
    ElectricMiningDrill = "electric-mining-drill", ElectricMiningDrill

    StoneFurnace = "stone-furnace", Furnace
    SteelFurnace = "steel-furnace", Furnace
    ElectricFurnace = "electric-furnace", ElectricFurnace

    Splitter = "splitter", Splitter
    FastSplitter = "fast-splitter", Splitter
    ExpressSplitter = "express-splitter", Splitter

    Rail = "rail", Rail

    TransportBelt = "transport-belt", TransportBelt
    FastTransportBelt = "fast-transport-belt", TransportBelt
    ExpressTransportBelt = "express-transport-belt", TransportBelt
    ExpressUndergroundBelt = "express-underground-belt", UndergroundBelt
    FastUndergroundBelt = "fast-underground-belt", UndergroundBelt
    UndergroundBelt = "underground-belt", UndergroundBelt
    OffshorePump = "offshore-pump", OffshorePump
    PumpJack = "pumpjack", PumpJack
    Pump = "pump", Pump
    Boiler = "boiler", Boiler
    OilRefinery = "oil-refinery", OilRefinery
    ChemicalPlant = "chemical-plant", ChemicalPlant

    SteamEngine = "steam-engine", Generator
    SolarPanel = "solar-panel", SolarPanel

    UndergroundPipe = "pipe-to-ground", Pipe
    HeatPipe = 'heat-pipe', Pipe
    Pipe = "pipe", Pipe

    SteelChest = "steel-chest", Chest
    IronChest = "iron-chest", Chest
    WoodenChest = "wooden-chest", Chest
    IronGearWheel = "iron-gear-wheel", Entity
    StorageTank = "storage-tank", StorageTank

    SmallElectricPole = "small-electric-pole", ElectricityPole
    MediumElectricPole = "medium-electric-pole", ElectricityPole
    BigElectricPole = "big-electric-pole", ElectricityPole

    Coal = "coal", None
    Wood = "wood", None
    Sulfur = "sulfur", None
    IronOre = "iron-ore", None
    CopperOre = "copper-ore", None
    Stone = "stone", None
    Concrete = "concrete", None
    UraniumOre = "uranium-ore", None

    IronPlate = "iron-plate", None  # Crafting requires smelting 1 iron ore
    IronStick = "iron-stick", None
    SteelPlate = "steel-plate", None  # Crafting requires smelting 5 iron plates
    CopperPlate = "copper-plate", None  # Crafting requires smelting 1 copper ore
    StoneBrick = "stone-brick", None # Crafting requires smelting 2 stone
    CopperCable = "copper-cable", None
    PlasticBar = "plastic-bar", None
    EmptyBarrel = "empty-barrel", None
    Battery = "battery", None
    SulfuricAcid = "sulfuric-acid", None
    Uranium235 = "uranium-235", None
    Uranium238 = "uranium-238", None

    Lubricant = "lubricant", None
    PetroleumGas = "petroleum-gas", None
    AdvancedOilProcessing = "advanced-oil-processing", None # These are recipes, not prototypes.
    CoalLiquifaction = "coal-liquifaction", None # These are recipes, not prototypes.
    SolidFuel = "solid-fuel", None # These are recipes, not prototypes.
    LightOil = "light-oil", None
    HeavyOil = "heavy-oil", None

    ElectronicCircuit = "electronic-circuit", None
    AdvancedCircuit = "advanced-circuit", None
    ProcessingUnit = "processing-unit", None
    EngineUnit = "engine-unit", None
    ElectricEngineUnit = "electric-engine-unit", None

    Lab = "lab", Lab
    Accumulator = "accumulator", Accumulator
    GunTurret = "gun-turret", GunTurret

    PiercingRoundsMagazine = "piercing-rounds-magazine", Ammo
    FirearmMagazine = "firearm-magazine", Ammo
    Grenade = "grenade", None

    Radar = "radar", Entity
    StoneWall = "stone-wall", Entity
    Gate = "gate", Entity
    SmallLamp = "small-lamp", Entity

    NuclearReactor = "nuclear-reactor", Reactor
    UraniumFuelCell = "uranium-fuel-cell", None
    HeatExchanger = 'heat-exchanger', HeatExchanger

    AutomationSciencePack = "automation-science-pack", None
    MilitarySciencePack = "military-science-pack", None
    LogisticsSciencePack = "logistic-science-pack", None
    ProductionSciencePack = "production-science-pack", None
    UtilitySciencePack = "utility-science-pack", None
    ChemicalSciencePack = "chemical-science-pack", None
    
    ProductivityModule = "productivity-module", None
    ProductivityModule2 = "productivity-module-2", None
    ProductivityModule3 = "productivity-module-3", None

    FlyingRobotFrame = "flying-robot-frame", None

    RocketSilo = "rocket-silo", RocketSilo
    Rocket = "rocket", Rocket
    Satellite = "satellite", None
    RocketPart = "rocket-part", None
    RocketControlUnit = "rocket-control-unit", None
    LowDensityStructure = "low-density-structure", None
    RocketFuel = "rocket-fuel", None
    SpaceSciencePack = "space-science-pack", None

    BeltGroup = "belt-group", BeltGroup
    PipeGroup = "pipe-group", PipeGroup
    ElectricityGroup = "electricity-group", ElectricityGroup

    def __init__(self, prototype_name, entity_class_name):
        self.prototype_name = prototype_name
        self.entity_class = entity_class_name

    @property
    def WIDTH(self):
        return self.entity_class._width.default  # Access the class attribute directly
    
    @property
    def HEIGHT(self):
        return self.entity_class._height.default

prototype_by_name = {prototype.value[0]: prototype for prototype in Prototype}
prototype_by_title = {str(prototype): prototype for prototype in Prototype}

import enum


class Technology(enum.Enum):
    # Basic automation technologies
    Automation = "automation"  # Unlocks assembling machine 1
    Automation2 = "automation-2"  # Unlocks assembling machine 2
    Automation3 = "automation-3"  # Unlocks assembling machine 3

    # Logistics technologies
    Logistics = "logistics"  # Unlocks basic belts and inserters
    Logistics2 = "logistics-2"  # Unlocks fast belts and inserters
    Logistics3 = "logistics-3"  # Unlocks express belts and inserters

    # Circuit technologies
    # CircuitNetwork = "circuit-network"
    AdvancedElectronics = "advanced-electronics"
    AdvancedElectronics2 = "advanced-electronics-2"

    # Power technologies
    Electronics = "electronics"
    ElectricEnergy = "electric-energy-distribution-1"
    ElectricEnergy2 = "electric-energy-distribution-2"
    SolarEnergy = "solar-energy"
    ElectricEngineering = "electric-engine"
    BatteryTechnology = "battery"
    # AdvancedBattery = "battery-mk2-equipment"
    NuclearPower = "nuclear-power"

    # Mining technologies
    SteelProcessing = "steel-processing"
    AdvancedMaterialProcessing = "advanced-material-processing"
    AdvancedMaterialProcessing2 = "advanced-material-processing-2"

    # Military technologies
    MilitaryScience = "military"
    # MilitaryScience2 = "military-2"
    # MilitaryScience3 = "military-3"
    # MilitaryScience4 = "military-4"
    # Artillery = "artillery"
    # Flamethrower = "flamethrower"
    # LandMines = "land-mines"
    # Turrets = "turrets"
    # LaserTurrets = "laser-turrets"
    # RocketSilo = "rocket-silo"

    # Armor and equipment
    ModularArmor = "modular-armor"
    PowerArmor = "power-armor"
    PowerArmor2 = "power-armor-mk2"
    NightVision = "night-vision-equipment"
    EnergyShield = "energy-shields"
    EnergyShield2 = "energy-shields-mk2-equipment"

    # Train technologies
    RailwayTransportation = "railway"
    # AutomatedRailTransportation = "automated-rail-transportation"
    # RailSignals = "rail-signals"

    # Oil processing
    OilProcessing = "oil-processing"
    AdvancedOilProcessing = "advanced-oil-processing"
    SulfurProcessing = "sulfur-processing"
    Plastics = "plastics"
    Lubricant = "lubricant"

    # Modules
    # Modules = "modules"
    # SpeedModule = "speed-module"
    # SpeedModule2 = "speed-module-2"
    # SpeedModule3 = "speed-module-3"
    ProductivityModule = "productivity-module"
    ProductivityModule2 = "productivity-module-2"
    ProductivityModule3 = "productivity-module-3"
    # EfficiencyModule = "efficiency-module"
    # EfficiencyModule2 = "efficiency-module-2"
    # EfficiencyModule3 = "efficiency-module-3"

    # Robot technologies
    Robotics = "robotics"
    # ConstructionRobotics = "construction-robotics"
    # LogisticRobotics = "logistic-robotics"
    # LogisticSystem = "logistic-system"
    # CharacterLogisticSlots = "character-logistic-slots"
    # CharacterLogisticSlots2 = "character-logistic-slots-2"

    # Science technologies
    LogisticsSciencePack = "logistic-science-pack"
    MilitarySciencePack = "military-science-pack"
    ChemicalSciencePack = "chemical-science-pack"
    ProductionSciencePack = "production-science-pack"
    # UtilitySciencePack = "utility-science-pack"
    #SpaceSciencePack = "space-science-pack"

    # Inserter technologies
    FastInserter = "fast-inserter"
    StackInserter = "stack-inserter"
    StackInserterCapacity1 = "stack-inserter-capacity-bonus-1"
    StackInserterCapacity2 = "stack-inserter-capacity-bonus-2"

    # Storage technologies
    StorageTanks = "fluid-handling"
    BarrelFilling = "barrel-filling"
    # Warehouses = "warehousing"

    # Vehicle technologies
    # Automobiles = "automobilism"
    # TankTechnology = "tank"
    # SpiderVehicle = "spidertron"

    # Weapon technologies
    Grenades = "grenades"
    # ClusterGrenades = "cluster-grenades"
    # RocketLauncher = "rocketry"
    # ExplosiveRocketry = "explosive-rocketry"
    # AtomicBomb = "atomic-bomb"
    # CombatRobotics = "combat-robotics"
    # CombatRobotics2 = "combat-robotics-2"
    # CombatRobotics3 = "combat-robotics-3"

    # Misc technologies
    Landfill = "landfill"
    CharacterInventorySlots = "character-inventory-slots"
    ResearchSpeed = "research-speed"
    # Toolbelt = "toolbelt"
    # BrakinPower = "braking-force"

    # # Endgame technologies
    SpaceScience = "space-science-pack"
    RocketFuel = "rocket-fuel"
    RocketControl = "rocket-control-unit"
    LowDensityStructure = "low-density-structure"
    RocketSiloTechnology = "rocket-silo"


# Helper dictionary to look up technology by name string
technology_by_name = {tech.value: tech for tech in Technology}

class Resource:
    Coal = "coal", ResourcePatch
    IronOre = "iron-ore", ResourcePatch
    CopperOre = "copper-ore", ResourcePatch
    Stone = "stone", ResourcePatch
    Water = "water", ResourcePatch
    CrudeOil = "crude-oil", ResourcePatch
    UraniumOre = "uranium-ore", ResourcePatch
    Wood = "wood", ResourcePatch