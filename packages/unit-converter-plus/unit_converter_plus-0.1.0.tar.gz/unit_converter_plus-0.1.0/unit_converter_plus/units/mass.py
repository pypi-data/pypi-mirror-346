class MassConverter:
    def __init__(self):
        self.units = {
            "kilogram": 1,
            "gram": 1e-3,
            "milligram": 1e-6,
            "microgram": 1e-9,
            "ton": 1000,
            "pound": 0.453592,
            "ounce": 0.0283495,
            "stone": 6.35029,
            "us_ton": 907.18474,  
            "uk_ton": 1016.0469,  
        }

        self.aliases = {
            "kilogram": ["kg", "kilogram", "كيلوغرام", "كغم"],
            "gram": ["g", "gram", "غرام"],
            "milligram": ["mg", "milligram", "مليغرام"],
            "microgram": ["μg", "microgram", "ميكروغرام"],
            "ton": ["ton", "طن", "طن متري"],
            "pound": ["lb", "pound", "رطل"],
            "ounce": ["oz", "ounce", "أوقية"],
            "stone": ["st", "stone", "ستون"],
            "us_ton": ["us_ton", "طن أمريكي", "طن_قصير"],
            "uk_ton": ["uk_ton", "طن إنجليزي", "طن_طويل"],
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

        value_in_kg = value * self.units[from_unit]
        return value_in_kg / self.units[to_unit]
