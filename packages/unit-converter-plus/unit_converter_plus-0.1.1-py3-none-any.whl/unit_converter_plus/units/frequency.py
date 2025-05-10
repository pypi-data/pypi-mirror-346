class FrequencyConverter:
    def __init__(self):
        self.units = {
            "hertz": 1,  
            "kilohertz": 1e3,  
            "megahertz": 1e6,  
            "gigahertz": 1e9,  
            "terahertz": 1e12, 
            "millihertz": 1e-3,
            "microhertz": 1e-6,  
            "nanohertz": 1e-9,  
            "picohertz": 1e-12, 
            "kilocycles": 1e3,  
            "megacycles": 1e6,  
            "gigacycles": 1e9,  
            "teracycles": 1e12, 
        }

        self.aliases = {
            "hertz": ["hz", "hertz", "هرتز"],
            "kilohertz": ["khz", "kilohertz", "كيلوهرتز"],
            "megahertz": ["mhz", "megahertz", "ميغاهرتز"],
            "gigahertz": ["ghz", "gigahertz", "جيغاهرتز"],
            "terahertz": ["thz", "terahertz", "تيراهرتز"],
            "millihertz": ["mhz", "millihertz", "ميلي_هرتز"],
            "microhertz": ["μhz", "microhertz", "ميكرو_هرتز"],
            "nanohertz": ["nhz", "nanohertz", "نانو_هرتز"],
            "picohertz": ["phz", "picohertz", "بيكو_هرتز"],
            "kilocycles": ["kc", "kilocycles", "كيلو_سايكل"],
            "megacycles": ["mc", "megacycles", "ميغا_سايكل"],
            "gigacycles": ["gc", "gigacycles", "جيغا_سايكل"],
            "teracycles": ["tc", "teracycles", "تيرا_سايكل"],
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

        value_in_hertz = value * self.units[from_unit]
        return value_in_hertz / self.units[to_unit]
