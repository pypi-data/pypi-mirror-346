class EnergyConverter:
    def __init__(self):
        self.units = {
            "joule": 1,
            "kilojoule": 1e3,
            "calorie": 4.184,
            "kilocalorie": 4184,
            "watt_hour": 3600,
            "kilowatt_hour": 3.6e6,
            "electronvolt": 1.60218e-19,
            "btu": 1055.06,
            "therm": 1.055e8,
            "ton_tnt": 4.184e9,
            "erg": 1e-7,
            "foot_pound": 1.35582,
        }

        self.aliases = {
            "joule": ["j", "joule", "جول"],
            "kilojoule": ["kj", "kilojoule", "كيلوجول"],
            "calorie": ["cal", "calorie", "سعر", "سعر_صغير"],
            "kilocalorie": ["kcal", "kilocalorie", "سعر_كبير", "كيلو_سعر", "سعرة_حرارية"],
            "watt_hour": ["wh", "watt_hour", "واط_ساعة"],
            "kilowatt_hour": ["kwh", "kilowatt_hour", "كيلوواط_ساعة"],
            "electronvolt": ["ev", "electronvolt", "إلكترون_فولت"],
            "btu": ["btu", "british_thermal_unit", "وحدة_حرارية_بريطانية"],
            "therm": ["therm", "ثيرم", "وحدة_غاز"],
            "ton_tnt": ["tnt", "ton_tnt", "طن_tnt", "طن_تي_ان_تي"],
            "erg": ["erg", "إرج"],
            "foot_pound": ["ft_lb", "foot_pound", "قدم_باوند", "قدم_رطل"],
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
        value_in_joules = value * self.units[from_unit]
        return value_in_joules / self.units[to_unit]
