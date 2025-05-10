class LengthConverter:
    def __init__(self):
        self.units = {
            "meter": 1,
            "kilometer": 1000,
            "centimeter": 0.01,
            "millimeter": 0.001,
            "micrometer": 1e-6,
            "nanometer": 1e-9,
            "mile": 1609.34,
            "yard": 0.9144,
            "foot": 0.3048,
            "inch": 0.0254,
            "nautical_mile": 1852,  
            "furlong": 201.168      
        }

        self.aliases = {
            "meter": ["m", "meter", "متر"],
            "kilometer": ["km", "kilometer", "كيلومتر"],
            "centimeter": ["cm", "centimeter", "سنتيمتر"],
            "millimeter": ["mm", "millimeter", "ملليمتر"],
            "micrometer": ["um", "micrometer", "ميكرومتر"],
            "nanometer": ["nm", "nanometer", "نانومتر"],
            "mile": ["mi", "mile", "ميل"],
            "yard": ["yd", "yard", "يارد"],
            "foot": ["ft", "foot", "قدم"],
            "inch": ["in", "inch", "بوصة"],
            "nautical_mile": ["nmi", "nautical_mile", "ميل_بحري", "ميل_ملاحي", "ميل_بحري_ملاحي"],
            "furlong": ["fur", "furlong", "مِلَّة", "مِلَّات"]
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

        value_in_meters = value * self.units[from_unit]
        return value_in_meters / self.units[to_unit]
