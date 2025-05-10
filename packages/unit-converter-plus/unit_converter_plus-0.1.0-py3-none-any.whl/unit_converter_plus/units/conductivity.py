class ConductivityConverter:
    def __init__(self):
        self.units = {
            "siemens_per_meter": 1,
            "millisiemens_per_meter": 1e-3,
            "microsiemens_per_meter": 1e-6,
            "mho_per_meter": 1,
            "milli_mho_per_meter": 1e-3,
            "micromho_per_meter": 1e-6,
        }

        self.aliases = {
            "siemens_per_meter": ["s/m", "siemens_per_meter", "سيمنز_للمتر"],
            "millisiemens_per_meter": ["ms/m", "millisiemens_per_meter", "ميلي_سيمنز_للمتر"],
            "microsiemens_per_meter": ["μs/m", "microsiemens_per_meter", "ميكرو_سيمنز_للمتر"],
            "mho_per_meter": ["mho/m", "mho_per_meter", "موه_للمتر"],
            "milli_mho_per_meter": ["mmho/m", "milli_mho_per_meter", "ملي_موه_للمتر"],
            "micromho_per_meter": ["μmho/m", "micromho_per_meter", "ميكرو_موه_للمتر"],
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

        value_in_siemens_per_meter = value * self.units[from_unit]
        return value_in_siemens_per_meter / self.units[to_unit]
