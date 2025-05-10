class EarthquakeConverter:
    def __init__(self):
        self.units = {
            "richter_scale": 1,
            "moment_magnitude": 1,  
            "acceleration": 9.81,  
            "g_force": 1,
            "seismic_moment": 1e20,
            "intensity": 1,
            "decibels": 1,
        }

        self.aliases = {
            "richter_scale": ["richter_scale", "richter", "magnitude", "مقياس_ريختر"],
            "moment_magnitude": ["moment_magnitude", "magnitude", "مقياس_العزم"],
            "acceleration": ["acceleration", "g", "تسارع", "تسارع_زلزالي"],
            "g_force": ["g_force", "g", "جاذبية", "قوة_جاذبية"],
            "seismic_moment": ["seismic_moment", "moment", "العزم_الزلزالي"],
            "intensity": ["intensity", "shidda", "شدة_الزلزال"],
            "decibels": ["decibels", "dB", "ديسيبل", "شدة_الصوت"],
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

        value_in_base_unit = value * self.units[from_unit]
        return value_in_base_unit / self.units[to_unit]