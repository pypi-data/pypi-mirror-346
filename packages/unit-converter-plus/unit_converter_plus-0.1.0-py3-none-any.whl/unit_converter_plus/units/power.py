class PowerConverter:
    def __init__(self):
        self.units = {
            "watt": 1,
            "kilowatt": 1000,
            "megawatt": 1e6,
            "gigawatt": 1e9,
            "microwatt": 1e-6,
            "horsepower": 745.7,
            "electric_horsepower": 746,
            "metric_horsepower": 735.5,
            "ton_refrigeration": 3516.85,
            "boiler_horsepower": 9809.5,
            "decibel_milliwatt": 0.0012589,
        }

        self.aliases = {
            "watt": ["w", "watt", "واط"],
            "kilowatt": ["kw", "kilowatt", "كيلوواط"],
            "megawatt": ["mw", "megawatt", "ميغاواط", "ميجاواط"],
            "gigawatt": ["gw", "gigawatt", "جيجاواط"],
            "microwatt": ["μw", "microwatt", "ميكروواط"],
            "horsepower": ["hp", "horsepower", "حصان", "حصان_ميكانيكي"],
            "electric_horsepower": ["ehp", "electric_horsepower", "حصان_كهربائي"],
            "metric_horsepower": ["mhp", "metric_horsepower", "حصان_متري"],
            "ton_refrigeration": ["tr", "ton_refrigeration", "طن_تبريد"],
            "boiler_horsepower": ["bhp", "boiler_horsepower", "حصان_بخاري"],
            "decibel_milliwatt": ["dbm", "decibel_milliwatt", "ديسيبل_ميليواط"],
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
        value_in_watts = value * self.units[from_unit]
        return value_in_watts / self.units[to_unit]
