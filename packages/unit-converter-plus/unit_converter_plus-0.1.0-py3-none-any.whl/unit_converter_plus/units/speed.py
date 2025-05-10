class SpeedConverter:
    def __init__(self):
        self.units = {
            "mps": 1,                
            "kph": 1000 / 3600,      
            "mph": 1609.344 / 3600,  
            "fps": 0.3048,           
            "knots": 1852 / 3600,    
            "mach": 343,             
            "mps_hour": 1 * 3600,        
            "kmps": 1000,                
            "kmph": 1000 / 3600,         
            "inchps": 0.0254,            
            "inchesph": 0.0254 * 3600,   
            "ftps": 0.3048,              
            "ftph": 0.3048 * 3600,       
            "milesps": 1609.344,         
            "milesph": 1609.344 * 3600,  
        }

        self.aliases = {
            "mps": ["mps", "m/s", "متر_في_الثانية"],
            "kph": ["kph", "km/h", "كيلومتر_في_الساعة"],
            "mph": ["mph", "mile/h", "ميل_في_الساعة"],
            "fps": ["fps", "ft/s", "قدم_في_الثانية"],
            "knots": ["knots", "nmi/h", "عقدة_بحرية"],
            "mach": ["mach", "ماخ", "سرعة_الصوت"],
            "mps_hour": ["mps_hour", "m/s_hour", "متر_في_الساعة"],
            "kmps": ["kmps", "km/s", "كيلومتر_في_الثانية"],
            "kmph": ["kmph", "km/h", "كيلومتر_في_الساعة"],
            "inchps": ["inchps", "in/s", "بوصة_في_الثانية"],
            "inchesph": ["inchesph", "in/h", "بوصة_في_الساعة"],
            "ftps": ["ftps", "ft/s", "قدم_في_الثانية"],
            "ftph": ["ftph", "ft/h", "قدم_في_الساعة"],
            "milesps": ["milesps", "mi/s", "ميل_في_الثانية"],
            "milesph": ["milesph", "mi/h", "ميل_في_الساعة"],
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

        value_in_mps = value * self.units[from_unit]
        return value_in_mps / self.units[to_unit]
