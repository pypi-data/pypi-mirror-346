from .units.angle import AngleConverter
from .units.area import AreaConverter
from .units.conductivity import ConductivityConverter
from .units.data import DataConverter
from .units.earthquake import EarthquakeConverter
from .units.energy import EnergyConverter
from .units.force import ForceConverter
from .units.frequency import FrequencyConverter
from .units.length import LengthConverter
from .units.luminosity import LuminosityConverter
from .units.mass import MassConverter
from .units.power import PowerConverter
from .units.pressure import PressureConverter
from .units.speed import SpeedConverter
from .units.temperature import TemperatureConverter
from .units.Time import TimeConverter
from .units.volume import VolumeConverter

class UnitConverter:
    def __init__(self):
        """
        Initializes the UnitConverter class by setting up the categories of units.
        Each category is associated with a corresponding unit converter.
        """
        self.categories = {
            "angle": AngleConverter(),
            "area": AreaConverter(),
            "conductivity": ConductivityConverter(),
            "data": DataConverter(),
            "earthquake": EarthquakeConverter(),
            "energy": EnergyConverter(),
            "force": ForceConverter(),
            "frequency": FrequencyConverter(),
            "length": LengthConverter(),
            "luminosity": LuminosityConverter(),
            "mass": MassConverter(),
            "power": PowerConverter(),
            "pressure": PressureConverter(),
            "speed": SpeedConverter(),
            "temperature": TemperatureConverter(),
            "time": TimeConverter(),
            "volume": VolumeConverter()
        }

    def convert(self, category: str, value: float, from_unit: str, to_unit: str) -> float:
        """
        Converts a value from one unit to another within the same category.

        Args:
            category (str): The category of units (e.g., 'length').
            value (float): The value to be converted.
            from_unit (str): The unit to convert from.
            to_unit (str): The unit to convert to.

        Returns:
            float: The converted value.

        Raises:
            ValueError: If the category is not registered or the conversion is not supported.
        """
        if category not in self.categories:
            raise ValueError(f"Category '{category}' not registered.")

        converter = self.categories[category]
        return converter.convert(value, from_unit, to_unit)

    def list_categories(self):
        """
        Returns a list of all the registered categories.

        Returns:
            list: A list of category names (e.g., ['angle', 'length', 'data']).
        """
        return list(self.categories.keys())

    def list_units(self, category: str) -> list:
        """
        Returns a list of the basic units in a specific category.

        Args:
            category (str): The category of units (e.g., 'data').

        Returns:
            list: A list of basic units in the category.

        Raises:
            ValueError: If the category is not registered or the converter does not support listing units.
        """
        category = category.lower()
        if category not in self.categories:
            raise ValueError(f"Category '{category}' not registered.")
        
        converter = self.categories[category]
        
        # Return only the basic units (i.e., keys from the `units` dictionary)
        if hasattr(converter, "units"):
            return list(converter.units.keys())
        else:
            raise ValueError(f"The converter for category '{category}' does not support listing units.")

    def list_unit_aliases(self, category: str, unit: str) -> list:
        """
        Returns a list of aliases (alternative names) for a specific unit within a category.

        Args:
            category (str): The category of units (e.g., 'data').
            unit (str): The unit name (e.g., 'gib').

        Returns:
            list: A list of aliases for the unit.

        Raises:
            ValueError: If the category or unit is not registered, or aliases are not supported.
        """
        category = category.lower()
        unit = unit.lower()

        if category not in self.categories:
            raise ValueError(f"Category '{category}' not registered.")
        
        converter = self.categories[category]

        # Check if aliases are supported for this category
        if hasattr(converter, "aliases"):
            for standard_name, aliases in converter.aliases.items():
                if unit in aliases:
                    return aliases
            raise ValueError(f"Unit '{unit}' not found in category '{category}'.")
        else:
            raise ValueError(f"The converter for category '{category}' does not support aliases.")
