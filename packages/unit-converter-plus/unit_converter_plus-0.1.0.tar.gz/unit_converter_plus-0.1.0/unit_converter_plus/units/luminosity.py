class LuminosityConverter:
    def __init__(self):
        self.units = {
            "lumen": 1,  
            "lux": 1,  
            "candela": 1,  
            "foot_candle": 10.764,  
            "nit": 1,  
            "flame_lumen": 1,  
            "watt": 683,  
        }

        self.aliases = {
            "lumen": ["lm", "lumen", "لومن"],
            "lux": ["lx", "lux", "لوكس"],
            "candela": ["cd", "candela", "كانديلا"],
            "foot_candle": ["fc", "foot_candle", "فوت_كاندل"],
            "nit": ["nt", "nit", "نيت"],
            "flame_lumen": ["flm", "flame_lumen", "لومن_شعلة"],
            "watt": ["w", "watt", "واط"],
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

        value_in_lumen = value * self.units[from_unit]
        return value_in_lumen / self.units[to_unit]
