class TemperatureConverter:
    def __init__(self):
        self.units = {
            "celsius": "c",
            "fahrenheit": "f",
            "kelvin": "k"
        }

        self.aliases = {
            "c": ["c", "celsius", "سيلسيوس", "سيليسيوس", "مئوية"],
            "f": ["f", "fahrenheit", "فهرنهايت"],
            "k": ["k", "kelvin", "كلفن", "كلفين"]
        }

        self.normalized_names = {}
        for standard, names in self.aliases.items():
            for name in names:
                self.normalized_names[name.lower()] = standard

    def normalize_unit(self, name: str) -> str:
        name = name.lower()
        if name in self.normalized_names:
            return self.normalized_names[name]
        raise ValueError(f"الوحدة '{name}' غير معروفة.")

    def convert(self, value: float, from_unit: str, to_unit: str) -> float:
        from_unit = self.normalize_unit(from_unit)
        to_unit = self.normalize_unit(to_unit)

        kelvin = self._to_kelvin(value, from_unit)
        return self._from_kelvin(kelvin, to_unit)

    def _to_kelvin(self, value: float, unit: str) -> float:
        if unit == "c":
            return value + 273.15
        elif unit == "f":
            return (value - 32) * 5/9 + 273.15
        elif unit == "k":
            return value
        else:
            raise ValueError(f"الوحدة '{unit}' غير مدعومة.")

    def _from_kelvin(self, kelvin: float, unit: str) -> float:
        if unit == "c":
            return kelvin - 273.15
        elif unit == "f":
            return (kelvin - 273.15) * 9/5 + 32
        elif unit == "k":
            return kelvin
        else:
            raise ValueError(f"الوحدة '{unit}' غير مدعومة.")
