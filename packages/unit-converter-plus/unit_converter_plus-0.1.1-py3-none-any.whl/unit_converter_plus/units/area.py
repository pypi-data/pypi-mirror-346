class AreaConverter:
    def __init__(self):
        self.units = {
            "square_meter": 1,
            "square_kilometer": 1e6,
            "square_centimeter": 1e-4,
            "square_millimeter": 1e-6,
            "square_inch": 0.00064516,
            "square_foot": 0.092903,
            "square_yard": 0.836127,
            "acre": 4046.85642,
            "hectare": 10000,
            "square_mile": 2589988.11,
            "square_nautical_mile": 3.4299e6,
            "rod": 25.2929,
            "are": 100,
            "decare": 1000,
        }

        self.aliases = {
            "square_meter": ["m2", "square_meter", "متر_مربع"],
            "square_kilometer": ["km2", "square_kilometer", "كيلومتر_مربع"],
            "square_centimeter": ["cm2", "square_centimeter", "سنتيمتر_مربع"],
            "square_millimeter": ["mm2", "square_millimeter", "ملليمتر_مربع"],
            "square_inch": ["in2", "square_inch", "بوصة_مربعة"],
            "square_foot": ["ft2", "square_foot", "قدم_مربع"],
            "square_yard": ["yd2", "square_yard", "يارد_مربع"],
            "acre": ["acre", "فدان"],
            "hectare": ["ha", "hectare", "هكتار"],
            "square_mile": ["mi2", "square_mile", "ميل_مربع"],
            "square_nautical_mile": ["nmi2", "square_nautical_mile", "ميل_بحري_مربع"],
            "rod": ["rod", "رود", "متر_رود"],
            "are": ["are", "آر", "أر"],
            "decare": ["decare", "ديكار", "عشر_آرات", "عشر_أر"],
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

        value_in_square_meters = value * self.units[from_unit]
        return value_in_square_meters / self.units[to_unit]
