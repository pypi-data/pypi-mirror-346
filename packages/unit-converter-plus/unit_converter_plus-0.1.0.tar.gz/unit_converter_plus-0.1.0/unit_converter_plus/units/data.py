class DataConverter:
    def __init__(self):
        self.units = {
            "bit": 1 / 8,  
            "byte": 1,
            "kb": 1000,
            "mb": 1000**2,
            "gb": 1000**3,
            "tb": 1000**4,
            "pb": 1000**5,
            "kib": 1024,
            "mib": 1024**2,
            "gib": 1024**3,
            "tib": 1024**4,
            "pib": 1024**5,
        }

        self.aliases = {
            "bit": ["bit", "بت", "بِت"],
            "byte": ["byte", "بايت", "octet"],
            "kb": ["kb", "kilobyte", "كيلوبايت", "ك.بايت"],
            "mb": ["mb", "megabyte", "ميغابايت", "م.بايت"],
            "gb": ["gb", "gigabyte", "غيغابايت", "جيجابايت", "ج.بايت"],
            "tb": ["tb", "terabyte", "تيرابايت", "ت.بايت"],
            "pb": ["pb", "petabyte", "بيتابايت", "ب.بايت"],
            "kib": ["kib", "kibibit", "كبي", "كيلو_ثنائي"],
            "mib": ["mib", "mebibit", "ميبي", "ميغا_ثنائي"],
            "gib": ["gib", "gibibit", "جيبي", "غ.ثنائي", "غيغا_ثنائي", "جيجابِت_ثنائية", "غيغابِت_ثنائية"],
            "tib": ["tib", "tebibit", "تيبي", "ت.ثنائي", "تيرا_ثنائي"],
            "pib": ["pib", "pebibit", "بيبي", "ب.ثنائي", "بيتا_ثنائية"],
        }
        
        self.normalized_names = {}
        for standard_name, alias_list in self.aliases.items():
            for alias in alias_list:
                self.normalized_names[alias.lower()] = standard_name

    def normalize_unit(self, name: str) -> str:
        name = name.lower()
        if name in self.normalized_names:
            return self.normalized_names[name]
        raise ValueError(f"الوحدة '{name}' غير معروفة.")

    def convert(self, value: float, from_unit: str, to_unit: str) -> float:
        from_unit = self.normalize_unit(from_unit)
        to_unit = self.normalize_unit(to_unit)

        value_in_bytes = value * self.units[from_unit]
        return value_in_bytes / self.units[to_unit]
