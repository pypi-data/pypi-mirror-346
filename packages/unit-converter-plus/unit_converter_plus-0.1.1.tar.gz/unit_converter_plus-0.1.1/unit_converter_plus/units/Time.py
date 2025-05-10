class TimeConverter:
    def __init__(self):
        self.units = {
            "second": 1,
            "minute": 60,
            "hour": 3600,
            "day": 86400,
            "week": 604800,
            "month": 2629746,     
            "year": 31556952  
        }

        self.aliases = {
            "second": ["s", "sec", "second", "ث", "ثانية", "ثواني"],
            "minute": ["m", "min", "minute", "د", "دقيقة", "دقائق"],
            "hour": ["h", "hr", "hour", "س", "ساعة", "ساعات"],
            "day": ["d", "day", "ي", "يوم", "أيام"],
            "week": ["w", "wk", "week", "أسبوع", "أسابيع"],
            "month": ["mo", "month", "ش", "شهر", "شهور", "أشهر"],
            "year": ["y", "yr", "year", "سنة", "سنوات", "أعوام"]
        }

        self.normalized_names = {}
        for key, names in self.aliases.items():
            for name in names:
                self.normalized_names[name.lower()] = key

    def normalize_unit(self, name: str) -> str:
        name = name.lower()
        if name in self.normalized_names:
            return self.normalized_names[name]
        raise ValueError(f"الوحدة '{name}' غير معروفة.")

    def convert(self, value: float, from_unit: str, to_unit: str) -> float:
        from_unit = self.normalize_unit(from_unit)
        to_unit = self.normalize_unit(to_unit)

        value_in_seconds = value * self.units[from_unit]
        return value_in_seconds / self.units[to_unit]
