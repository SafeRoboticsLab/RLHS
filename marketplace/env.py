from prompt import get_all_prompts
from environment import BaseEnv


class Marketplace(BaseEnv):
    items = {
            "TV": [
                ("3D movie playbacks", "No 3D movie playback", "3D movie capability not specified"),
                ("8K Resolution", "4K Resolution", "Resolution not specified"),
                ("HDR", "No HDR", "HDR capability not specified"),
                ("240Hz Refresh Rate", "60Hz Refresh Rate", "Refresh rate not specified"),
                ("Has Smart TV Features", "No Smart TV Features", "Smart features not specified"),
                ("OLED", "LED", "Panel type not specified"),
                ("Built-in Wi-Fi", "Only Ethernet", "Network connectivity not specified"),
                ("Large screen (65 inches or more)", "Small screen (less than 32 inches)", "Screen size not specified"),
            ],
            "Laptop": [
                ("High resolution (4K)", "Standard resolution (1080p)", "Resolution not specified"),
                ("Latest generation processor", "Older generation processor", "Processor generation not specified"),
                ("16GB or more RAM", "8GB or less RAM", "RAM not specified"),
                ("SSD storage", "HDD storage", "Storage type not specified"),
                ("Long battery life (10+ hours)", "Short battery life (less than 5 hours)", "Battery life not specified"),
                ("Lightweight (less than 2 kg)", "Heavy (more than 3 kg)", "Weight not specified"),
                ("Multiple USB-C ports", "Few or no USB-C ports", "USB-C ports not specified"),
                ("Fast charging capability", "No fast charging", "Charging speed not specified")
            ],
            "Smartphone": [
                ("High-resolution camera (108MP)", "Standard camera (12MP)", "Camera resolution not specified"),
                ("Large battery capacity (5000mAh)", "Small battery capacity (3000mAh)", "Battery capacity not specified"),
                ("OLED display", "LCD display", "Display type not specified"),
                ("Large storage (256GB+)", "Small storage (64GB)", "Storage capacity not specified"),
                ("8GB or more RAM", "4GB or less RAM", "RAM not specified"),
                ("Supports 5G", "Does not support 5G", "5G capability not specified"),
                ("Has biometric security (e.g., fingerprint, face recognition)", "No biometric security", "Biometric security not specified"),
                ("Fast charging capability", "No fast charging", "Charging speed not specified")
            ],
            "Refrigerator": [
                ("Large capacity (500+ liters)", "Small capacity (200 liters)", "Capacity not specified"),
                ("Energy-efficient (Energy Star certified)", "Not energy-efficient", "Energy efficiency not specified"),
                ("Frost-free", "Manual defrost", "Defrost type not specified"),
                ("Digital temperature control", "Manual temperature control", "Temperature control not specified"),
                ("Has water dispenser", "No water dispenser", "Water dispenser not specified"),
                ("Built-in ice maker", "No ice maker", "Ice maker not specified"),
                ("Quiet operation", "Noisy operation", "Noise level not specified"),
                ("Adjustable shelves", "Fixed shelves", "Shelving not specified")
            ],
            "Washing Machine": [
                ("Front-loading", "Top-loading", "Loading type not specified"),
                ("Large capacity (10kg+)", "Small capacity (5kg or less)", "Capacity not specified"),
                ("Energy-efficient (Energy Star certified)", "Not energy-efficient", "Energy efficiency not specified"),
                ("Quick wash feature", "No quick wash feature", "Wash feature not specified"),
                ("Built-in dryer", "No built-in dryer", "Dryer inclusion not specified"),
                ("Silent operation", "Noisy operation", "Noise level not specified"),
                ("Smart features (e.g., Wi-Fi, app control)", "No smart features", "Smart features not specified"),
                ("Multiple wash programs", "Limited wash programs", "Wash programs not specified")
            ],
            "Microwave Oven": [
                ("High wattage (1000W+)", "Low wattage (700W or less)", "Wattage not specified"),
                ("Convection feature", "No convection feature", "Convection feature not specified"),
                ("Inverter technology", "No inverter technology", "Inverter technology not specified"),
                ("Sensor cooking", "No sensor cooking", "Sensor technology not specified"),
                ("Large capacity (1.5 cubic feet+)", "Small capacity (0.7 cubic feet or less)", "Capacity not specified"),
                ("Child lock feature", "No child lock feature", "Child lock not specified"),
                ("Quick-start button", "No quick-start button", "Quick-start feature not specified"),
                ("Touch control panel", "Dial control panel", "Control panel not specified")
            ],
            "Dishwasher": [
                ("Built-in", "Portable", "Installation type not specified"),
                ("Energy-efficient (Energy Star certified)", "Not energy-efficient", "Energy efficiency not specified"),
                ("Quiet operation", "Noisy operation", "Noise level not specified"),
                ("Third rack for utensils", "No third rack", "Third rack not specified"),
                ("Adjustable racks", "Non-adjustable racks", "Rack adjustability not specified"),
                ("Multiple wash cycles", "Limited wash cycles", "Wash cycles not specified"),
                ("Delay start feature", "No delay start feature", "Start feature not specified"),
                ("Soil sensor", "No soil sensor", "Soil sensor not specified")
            ],
            "Air Conditioner": [
                ("High BTU (12,000+)", "Low BTU (5,000 or less)", "BTU rating not specified"),
                ("Energy-efficient (Energy Star certified)", "Not energy-efficient", "Energy efficiency not specified"),
                ("Inverter technology", "No inverter technology", "Inverter technology not specified"),
                ("Smart features (e.g., Wi-Fi, app control)", "No smart features", "Smart features not specified"),
                ("Quiet operation", "Noisy operation", "Noise level not specified"),
                ("Programmable timer", "No programmable timer", "Timer not specified"),
                ("Remote control", "No remote control", "Remote control not specified"),
                ("Washable filter", "Disposable filter", "Filter type not specified")
            ],
            "Vacuum Cleaner": [
                ("Cordless", "Corded", "Power type not specified"),
                ("Bagless", "Bagged", "Bag type not specified"),
                ("HEPA filter", "No HEPA filter", "Filter type not specified"),
                ("Lightweight (less than 3kg)", "Heavy (more than 5kg)", "Weight not specified"),
                ("Long battery life (60+ minutes)", "Short battery life (20 minutes or less)", "Battery life not specified"),
                ("Quiet operation", "Noisy operation", "Noise level not specified"),
                ("Smart features (e.g., Wi-Fi, app control)", "No smart features", "Smart features not specified"),
                ("Large dustbin capacity", "Small dustbin capacity", "Dustbin capacity not specified")
            ],
            "Coffee Maker": [
                ("Programmable settings", "Manual settings", "Programmability not specified"),
                ("Built-in grinder", "No built-in grinder", "Grinder inclusion not specified"),
                ("Multiple brew strengths", "Single brew strength", "Brew strength not specified"),
                ("Thermal carafe", "Glass carafe", "Carafe type not specified"),
                ("Large capacity (12 cups+)", "Small capacity (1-4 cups)", "Capacity not specified"),
                ("Energy-efficient", "Not energy-efficient", "Energy efficiency not specified"),
                ("Water filtration system", "No water filtration system", "Water filtration not specified"),
                ("Compact design", "Bulky design", "Design size not specified")
            ]
        }
    prices = {
            "TV": [(1800, 1900), (1400, 1600), (900, 1100)],
            "Laptop": [(1500, 1600), (1200, 1400), (800, 1000)],
            "Smartphone": [(1000, 1100), (800, 900), (600, 700)],
            "Refrigerator": [(2200, 2400), (1800, 2000), (1400, 1600)],
            "Washing Machine": [(1500, 1600), (1200, 1400), (900, 1100)],
            "Microwave Oven": [(550, 600), (450, 500), (350, 400)],
            "Dishwasher": [(900, 1000), (700, 800), (500, 600)],
            "Air Conditioner": [(2100, 2200), (1800, 2000), (1500, 1700)],
            "Vacuum Cleaner": [(350, 400), (300, 350), (250, 300)],
            "Coffee Maker": [(350, 400), (300, 350), (250, 300)]
        }
    all_prompts = get_all_prompts()