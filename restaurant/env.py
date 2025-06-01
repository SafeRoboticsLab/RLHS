from prompt import get_all_prompts
from environment import BaseEnv


class Restaurant(BaseEnv):
    items = {
        "Italian": [
            ("Wood-fired Neapolitan pizza", "Pre-made frozen pizza", "Pizza style not specified"),
            ("House-made fresh pasta", "Store-bought dried pasta", "Pasta freshness not specified"),
            ("Authentic imported ingredients", "Generic low-grade ingredients", "Ingredient sourcing not specified"),
            ("Extensive sommelier-curated wine list", "Limited house wines only", "Wine list not specified"),
            ("Cozy rustic ambiance", "Loud cafeteria ambiance", "Ambiance not specified"),
            ("Attentive table service", "Slow or inattentive service", "Service quality not specified"),
            ("Vegetarian & gluten-free options available", "No vegetarian options", "Dietary options not specified"),
            ("Traditional tiramisu made in-house", "Pre-packaged desserts", "Dessert quality not specified"),
        ],
        "Japanese": [
            ("Freshly flown-in fish for sushi", "Frozen fish used for sushi", "Fish freshness not specified"),
            ("Authentic omakase experience", "Pre-set conveyor-belt plates", "Dining style not specified"),
            ("Hand-pulled udon noodles", "Instant udon noodles", "Noodle preparation not specified"),
            ("Quiet zen-like interior", "Crowded fast-food layout", "Interior atmosphere not specified"),
            ("Highly skilled itamae (sushi chef)", "Inexperienced chef", "Chef expertise not specified"),
            ("Wide sake selection", "No alcoholic beverages", "Beverage menu not specified"),
            ("Seasonal kaiseki menu", "No seasonal specials", "Seasonal menu not specified"),
            ("Green-tea ice cream house-made", "Desserts outsourced", "Dessert offering not specified"),
        ],
        "Mexican": [
            ("House-made corn tortillas", "Store-bought tortillas", "Tortilla source not specified"),
            ("Slow-cooked barbacoa", "Pre-cooked reheated meats", "Meat preparation not specified"),
            ("Fresh guacamole prepared tableside", "Pre-packaged guacamole", "Guacamole freshness not specified"),
            ("Live mariachi on weekends", "No live entertainment", "Entertainment not specified"),
            ("Extensive tequila & mezcal list", "Limited spirit selection", "Spirit menu not specified"),
            ("Colorful traditional décor", "Minimal generic décor", "Décor style not specified"),
            ("Vegan taco options", "No vegan options", "Vegan availability not specified"),
            ("Homemade churros", "Desserts bought from supplier", "Dessert freshness not specified"),
        ],
        "American": [
            ("Grass-fed beef burgers", "Frozen patties", "Beef sourcing not specified"),
            ("Hand-cut truffle fries", "Pre-cut frozen fries", "Fries quality not specified"),
            ("Craft beer on tap", "Only mass-market beer", "Beer selection not specified"),
            ("Live blues music nights", "No live music", "Music offering not specified"),
            ("Sustainable seafood options", "No sustainability focus", "Sustainability not specified"),
            ("Farm-to-table seasonal menu", "Static year-round menu", "Seasonality not specified"),
            ("House-made pies", "Store-bought desserts", "Dessert sourcing not specified"),
            ("Pet-friendly patio", "No outdoor seating", "Outdoor seating not specified"),
        ],
        "Indian": [
            ("Traditional tandoor oven", "No tandoor—griddle used instead", "Cooking method not specified"),
            ("Freshly baked naan", "Pre-made naan reheated", "Bread freshness not specified"),
            ("Rich variety of vegetarian dishes", "Very limited vegetarian choices", "Vegetarian range not specified"),
            ("Authentic spice blends roasted in-house", "Generic commercial spice mix", "Spice sourcing not specified"),
            ("Classical sitar background music", "Loud pop music", "Music atmosphere not specified"),
            ("Mango lassi prepared fresh", "Lassi from mix", "Lassi freshness not specified"),
            ("Allergy-friendly labeling", "No allergen info", "Allergy info not specified"),
            ("Gulab jamun made on site", "Desserts outsourced", "Dessert preparation not specified"),
        ],
        "Chinese": [
            ("Hand-pulled Lanzhou noodles", "Factory-made noodles", "Noodle origin not specified"),
            ("Dim sum prepared to order", "Premade dim sum reheated", "Dim sum freshness not specified"),
            ("Traditional tea service", "No specialty teas", "Tea selection not specified"),
            ("Decorated with regional art", "Plain undecorated walls", "Décor not specified"),
            ("Experienced dim sum cart staff", "Inattentive service", "Service attentiveness not specified"),
            ("Szechuan dishes use authentic peppercorns", "Uses generic chili flakes", "Peppercorn authenticity not specified"),
            ("Vegetarian mapo tofu option", "Only pork mapo tofu", "Vegetarian option not specified"),
            ("Fortune cookies house-made", "Mass-produced fortune cookies", "Dessert authenticity not specified"),
        ],
        "French": [
            ("Classic foie gras entrée", "No gourmet entrées", "Entrée selection not specified"),
            ("Freshly baked baguettes daily", "Bread delivered frozen", "Bread freshness not specified"),
            ("Table-side crêpe suzette", "Pre-made desserts", "Dessert preparation not specified"),
            ("Sommelier-led wine pairings", "No wine guidance", "Wine service not specified"),
            ("White-tablecloth fine-dining setting", "Café-style casual setting", "Dining setting not specified"),
            ("Cheese trolley with AOC varieties", "Limited cheese options", "Cheese selection not specified"),
            ("Escargot in garlic butter", "No traditional escargot", "Escargot availability not specified"),
            ("French-speaking waitstaff", "No French language ability", "Staff language not specified"),
        ],
        "Mediterranean": [
            ("Cold-pressed extra-virgin olive oil", "Generic cooking oil", "Oil quality not specified"),
            ("Freshly baked pita from stone oven", "Store-bought pita", "Pita freshness not specified"),
            ("Wide selection of mezze plates", "Limited appetizer choices", "Mezze variety not specified"),
            ("Locally-sourced organic produce", "Produce origin unknown", "Produce sourcing not specified"),
            ("Outdoor seating with sea-inspired décor", "No outdoor seating", "Outdoor option not specified"),
            ("House-made baklava", "Baklava from wholesale supplier", "Dessert origin not specified"),
            ("Gluten-free falafel option", "No gluten-free options", "Gluten-free availability not specified"),
            ("Live olive-oil tasting events", "No tasting events", "Special events not specified"),
        ],
        "Thai": [
            ("Curry paste made fresh in-house", "Uses factory pre-made curry paste", "Curry preparation not specified"),
            ("Fresh aromatic herbs (lemongrass, kaffir lime, galangal)", "Dried or artificial herbs only", "Herb freshness not specified"),
            ("Som tam (papaya salad) prepared tableside", "Pre-shredded som tam from fridge", "Som tam preparation not specified"),
            ("Wide range of regional Thai dishes", "Limited menu of generic Pad Thai only", "Menu variety not specified"),
            ("Décor inspired by Thai temples with traditional music", "Sparse, generic décor", "Ambiance not specified"),
            ("Spiciness level fully customizable", "Fixed mild spice level", "Spice customization not specified"),
            ("Thai iced tea brewed fresh", "Powder-mix Thai iced tea", "Beverage quality not specified"),
            ("Vegetarian tofu alternatives available", "No vegetarian substitutions", "Vegetarian option not specified"),
        ],

        "Korean": [
            ("Charcoal-grilled BBQ at the table", "Pre-cooked meat on gas griddle", "Grilling method not specified"),
            ("House-fermented kimchi made on site", "Store-bought kimchi", "Kimchi source not specified"),
            ("Generous banchan side dishes with free refills", "Limited banchan, no refills", "Banchan policy not specified"),
            ("Stone-pot bibimbap served sizzling", "Bibimbap served lukewarm", "Serving temperature not specified"),
            ("Unlimited self-grill BBQ option", "Meat ordered by the plate only", "Serving style not specified"),
            ("Extensive soju & makgeolli selection", "Limited beverage options", "Beverage selection not specified"),
            ("Servers in traditional hanbok attire", "Casual server attire", "Server attire not specified"),
            ("Late-night hours until 2 a.m.", "Closes early at 9 p.m.", "Opening hours not specified"),
        ],
        }

        # ---------- typical per-person price brackets (USD) ----------
        prices = {
            #          premium          mid-tier         budget
            "Italian":        [(60, 80), (35, 50), (18, 28)],
            "Japanese":       [(80,100), (45, 60), (20, 30)],
            "Mexican":        [(45, 60), (25, 35), (12, 20)],
            "American":       [(55, 75), (30, 45), (15, 25)],
            "Indian":         [(50, 65), (28, 40), (12, 22)],
            "Chinese":        [(55, 70), (30, 45), (15, 25)],
            "French":         [(90,120), (50, 70), (25, 35)],
            "Mediterranean":  [(60, 80), (35, 50), (18, 28)],
            "Thai":    [(50, 70), (30, 45), (15, 25)],  # premium, mid-tier, budget
            "Korean":  [(60, 80), (35, 50), (20, 30)],
        }
    all_prompts = get_all_prompts()