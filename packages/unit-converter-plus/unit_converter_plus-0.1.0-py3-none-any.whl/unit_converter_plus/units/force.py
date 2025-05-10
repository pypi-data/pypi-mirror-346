class ForceConverter:
    def __init__(self):
        self.units = {
            "newton": 1,
            "dyne": 1e-5,  
            "kilonewton": 1e3,  
            "pound_force": 4.44822,  
            "kilopound_force": 4.44822e3,  
            "gram_force": 9.80665e-3,  
            "ton_force": 9.80665e3,  
            "ounce_force": 0.2780139,  
            "kilogram_force": 9.80665,  
            "megaton_force": 9.80665e6, 
            "micronewton": 1e-6,  
            "poundal": 0.13825495,  
            "kilopoundal": 0.13825495e3,  
            "metric_ton_force": 9.80665e3,  
            "long_ton_force": 9.807e3,  
            "short_ton_force": 8.89644e3,  
        }

        self.aliases = {
            "newton": ["n", "newton", "نيوتن"],
            "dyne": ["dyne", "داين"],
            "kilonewton": ["kn", "kilonewton", "كيلو_نيوتن"],
            "pound_force": ["lbf", "pound_force", "رطل_قوة"],
            "kilopound_force": ["klbf", "kilopound_force", "كيلو_رطل_قوة"],
            "gram_force": ["gf", "gram_force", "جرام_قوة"],
            "ton_force": ["tf", "ton_force", "طن_قوة"],
            "ounce_force": ["ozf", "ounce_force", "أونصة_قوة"],
            "kilogram_force": ["kgf", "kilogram_force", "كيلو_جرام_قوة"],
            "megaton_force": ["mtf", "megaton_force", "ميغا_طن_قوة"],
            "micronewton": ["μn", "micronewton", "ميكرونيوتن"],
            "poundal": ["pdl", "poundal", "باوندال"],
            "kilopoundal": ["kpdl", "kilopoundal", "كيلو_باوندال"],
            "metric_ton_force": ["mtf", "metric_ton_force", "طن_متري_قوة"],
            "long_ton_force": ["ltf", "long_ton_force", "طن_طويل_قوة"],
            "short_ton_force": ["stf", "short_ton_force", "طن_قصير_قوة"],
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

        value_in_newton = value * self.units[from_unit]
        return value_in_newton / self.units[to_unit]
