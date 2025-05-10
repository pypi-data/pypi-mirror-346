class VolumeConverter:
    def __init__(self):
        self.units = {
            "cubic_meter": 1,
            "liter": 1e-3,
            "milliliter": 1e-6,
            "cubic_centimeter": 1e-6,
            "cubic_millimeter": 1e-9,
            "gallon_us": 3.78541e-3,
            "gallon_uk": 4.54609e-3,  
            "quart_us": 9.4635e-3,
            "quart_uk": 1.13652e-2,
            "pint_us": 1.89271e-2,
            "pint_uk": 2.27304e-2,
            "cup": 2.36588e-2,
            "fluid_ounce": 3.78541e-2,
            "teaspoon": 5.91939e-2,
            "tablespoon": 1.77582e-2,
            "cubic_inch": 1.63871e-5,
            "cubic_foot": 0.0283168,
            "cubic_yard": 0.764555,
            "barrel_us": 0.158987,  
            "barrel_uk": 0.159,  
        }

        self.aliases = {
            "cubic_meter": ["m3", "cubic_meter", "متر_مكعب"],
            "liter": ["l", "liter", "لتر", "ل"],
            "milliliter": ["ml", "milliliter", "ملليلتر"],
            "cubic_centimeter": ["cm3", "cubic_centimeter", "سنتيمتر_مكعب"],
            "cubic_millimeter": ["mm3", "cubic_millimeter", "ملليمتر_مكعب"],
            "gallon_us": ["gal_us", "gallon_us", "جالون_أمريكي"],
            "gallon_uk": ["gal_uk", "gallon_uk", "جالون_بريطاني"],
            "quart_us": ["qt_us", "quart_us", "ربع_جالون_أمريكي"],
            "quart_uk": ["qt_uk", "quart_uk", "ربع_جالون_بريطاني"],
            "pint_us": ["pt_us", "pint_us", "باينت_أمريكي"],
            "pint_uk": ["pt_uk", "pint_uk", "باينت_بريطاني"],
            "cup": ["cup", "كوب"],
            "fluid_ounce": ["fl_oz", "fluid_ounce", "أونصة_سائلة"],
            "teaspoon": ["tsp", "teaspoon", "ملعقة_شاي"],
            "tablespoon": ["tbsp", "tablespoon", "ملعقة_طعام"],
            "cubic_inch": ["in3", "cubic_inch", "بوصة_مكعبة"],
            "cubic_foot": ["ft3", "cubic_foot", "قدم_مكعب"],
            "cubic_yard": ["yd3", "cubic_yard", "يارد_مكعب"],
            "barrel_us": ["bbl_us", "barrel_us", "برميل_أمريكي"],
            "barrel_uk": ["bbl_uk", "barrel_uk", "برميل_بريطاني"],
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

        value_in_cubic_meters = value * self.units[from_unit]
        return value_in_cubic_meters / self.units[to_unit]
