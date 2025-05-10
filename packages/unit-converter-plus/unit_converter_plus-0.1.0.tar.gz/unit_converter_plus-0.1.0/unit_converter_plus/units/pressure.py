class PressureConverter:
    def __init__(self):
        self.units = {
            "pascal": 1,
            "bar": 1e5,
            "psi": 6894.76,
            "atm": 101325,
            "torr": 133.322,
            "mmhg": 133.322,
            "inhg": 3386.39,
            "kgf_per_cm2": 9.80665e4,
            "kgf_per_m2": 9.80665,
            "pascals_per_square_meter": 1,
        }

        self.aliases = {
            "pascal": ["pa", "pascal", "باسكال"],
            "bar": ["bar", "بار"],
            "psi": ["psi", "رطل_لكل_بوصة_مربعة", "رطل_لكل_بوصة"],
            "atm": ["atm", "جو", "الضغط_الجوي"],
            "torr": ["torr", "تور"],
            "mmhg": ["mmhg", "مليمتر_زئبقي"],
            "inhg": ["inhg", "بوصة_زئبقية"],
            "kgf_per_cm2": ["kgf/cm2", "kgf_per_cm2", "كيلو_جرام_لكل_سنتيمتر_مربع"],
            "kgf_per_m2": ["kgf/m2", "kgf_per_m2", "كيلو_جرام_لكل_متر_مربع"],
            "pascals_per_square_meter": ["pa/m2", "pascals_per_square_meter", "باسكال_لكل_متر_مربع"],
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

        value_in_pascal = value * self.units[from_unit]
        return value_in_pascal / self.units[to_unit]
