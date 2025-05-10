import math

class AngleConverter:
    def __init__(self):
        self.units = {
            "radian": 1,
            "degree": math.pi / 180,
            "gradian": math.pi / 200,
            "turn": 2 * math.pi,
        }

        self.aliases = {
            "radian": ["rad", "radian", "راديان"],
            "degree": ["deg", "degree", "°", "درجة"],
            "gradian": ["gon", "grad", "gradian", "غراد", "جراد"],
            "turn": ["turn", "دورة", "لفة"],
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

        value_in_radians = value * self.units[from_unit]
        return value_in_radians / self.units[to_unit]
