import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant.settings')
django.setup()

from menu.models import Dish, Category, DietaryTag, Allergen

# Ensure categories exist
categories_config = {
    'appetizers': {'icon': '🥗', 'display_order': 1},
    'mains': {'icon': '🍽️', 'display_order': 2},
    'desserts': {'icon': '🍰', 'display_order': 3},
    'beverages': {'icon': '🍷', 'display_order': 4},
}

categories = {}
for cat_type, config in categories_config.items():
    cat, _ = Category.objects.get_or_create(
        name=cat_type,
        defaults={'icon': config['icon'], 'display_order': config['display_order']}
    )
    categories[cat_type] = cat

# Get or create dietary tags
dietary_tags_list = {
    'vegetarian': DietaryTag.objects.get_or_create(name='vegetarian')[0],
    'vegan': DietaryTag.objects.get_or_create(name='vegan')[0],
    'gluten_free': DietaryTag.objects.get_or_create(name='gluten_free')[0],
    'dairy_free': DietaryTag.objects.get_or_create(name='dairy_free')[0],
    'keto': DietaryTag.objects.get_or_create(name='keto')[0],
}

# Get or create allergens
allergens_list = {
    'nuts': Allergen.objects.get_or_create(name='nuts')[0],
    'dairy': Allergen.objects.get_or_create(name='dairy')[0],
    'eggs': Allergen.objects.get_or_create(name='eggs')[0],
    'shellfish': Allergen.objects.get_or_create(name='shellfish')[0],
    'soy': Allergen.objects.get_or_create(name='soy')[0],
    'wheat': Allergen.objects.get_or_create(name='wheat')[0],
}

dishes_data = [
    {
        'name': 'Margherita Pizza',
        'description': 'Classic Italian pizza with fresh mozzarella, basil, and tomato sauce',
        'price': 12.99,
        'category': categories['mains'],
        'cuisine_type': 'italian',
        'preference': 'chef_special',
        'preferred_sauce': 'Fresh tomato and basil',
        'prep_time': 20,
        'spice_level': 'mild',
        'ingredients': 'Tomato, mozzarella, basil, olive oil, pizza dough',
        'rating': 4.5,
        'is_available': True,
        'dietary_tags': ['vegetarian'],
        'allergens': ['dairy', 'wheat'],
    },
    {
        'name': 'Spaghetti Carbonara',
        'description': 'Traditional Italian pasta with eggs, bacon, and parmesan cheese',
        'price': 13.99,
        'category': categories['mains'],
        'cuisine_type': 'italian',
        'preference': 'chef_special',
        'preferred_sauce': 'Creamy egg and bacon sauce',
        'prep_time': 25,
        'spice_level': 'mild',
        'ingredients': 'Pasta, eggs, bacon, parmesan, black pepper, olive oil',
        'rating': 4.7,
        'is_available': True,
        'dietary_tags': [],
        'allergens': ['eggs', 'dairy', 'wheat'],
    },
    {
        'name': 'Grilled Salmon',
        'description': 'Fresh Atlantic salmon fillet with lemon butter sauce',
        'price': 18.99,
        'category': categories['mains'],
        'cuisine_type': 'mediterranean',
        'preference': 'chef_special',
        'preferred_sauce': 'Lemon butter sauce',
        'prep_time': 30,
        'spice_level': 'mild',
        'ingredients': 'Salmon fillet, lemon, butter, herbs, olive oil',
        'rating': 4.8,
        'is_available': True,
        'dietary_tags': [],
        'allergens': ['dairy'],
    },
    {
        'name': 'Caesar Salad',
        'description': 'Crisp romaine lettuce with parmesan, croutons, and caesar dressing',
        'price': 9.99,
        'category': categories['appetizers'],
        'cuisine_type': 'american',
        'preference': 'vegetarian',
        'preferred_sauce': 'Caesar dressing',
        'prep_time': 10,
        'spice_level': 'mild',
        'ingredients': 'Romaine lettuce, parmesan, croutons, caesar dressing',
        'rating': 4.3,
        'is_available': True,
        'dietary_tags': ['vegetarian'],
        'allergens': ['eggs', 'dairy', 'wheat'],
    },
    {
        'name': 'Beef Burger',
        'description': 'Juicy beef patty with cheddar cheese, lettuce, tomato, and special sauce',
        'price': 11.99,
        'category': categories['mains'],
        'cuisine_type': 'american',
        'preference': 'chef_special',
        'preferred_sauce': 'Special burger sauce',
        'prep_time': 15,
        'spice_level': 'mild',
        'ingredients': 'Beef patty, cheddar cheese, lettuce, tomato, onion, burger bun',
        'rating': 4.4,
        'is_available': True,
        'dietary_tags': [],
        'allergens': ['dairy', 'wheat'],
    },
    {
        'name': 'Chicken Tikka Masala',
        'description': 'Tender chicken in creamy tomato and spice sauce with rice',
        'price': 14.99,
        'category': categories['mains'],
        'cuisine_type': 'asian',
        'preference': 'spicy',
        'preferred_sauce': 'Tikka masala curry sauce',
        'prep_time': 35,
        'spice_level': 'medium',
        'ingredients': 'Chicken, yogurt, tomato, cream, spices, basmati rice',
        'rating': 4.6,
        'is_available': True,
        'dietary_tags': [],
        'allergens': ['dairy'],
    },
    {
        'name': 'Pad Thai',
        'description': 'Stir-fried rice noodles with shrimp, peanuts, and lime',
        'price': 13.99,
        'category': categories['mains'],
        'cuisine_type': 'asian',
        'preference': 'chef_special',
        'preferred_sauce': 'Tamarind and peanut sauce',
        'prep_time': 20,
        'spice_level': 'medium',
        'ingredients': 'Rice noodles, shrimp, peanuts, lime, eggs, bean sprouts',
        'rating': 4.5,
        'is_available': True,
        'dietary_tags': [],
        'allergens': ['shellfish', 'peanuts', 'eggs'],
    },
    {
        'name': 'Falafel Wrap',
        'description': 'Crispy falafel balls in pita wrap with tahini sauce and vegetables',
        'price': 9.99,
        'category': categories['mains'],
        'cuisine_type': 'mediterranean',
        'preference': 'vegetarian',
        'preferred_sauce': 'Tahini sauce',
        'prep_time': 15,
        'spice_level': 'medium',
        'ingredients': 'Chickpeas, falafel spices, pita bread, tahini, vegetables',
        'rating': 4.2,
        'is_available': True,
        'dietary_tags': ['vegan', 'vegetarian'],
        'allergens': ['wheat', 'soy'],
    },
    {
        'name': 'Beef Steak',
        'description': '12oz prime rib eye steak with garlic mashed potatoes and asparagus',
        'price': 24.99,
        'category': categories['mains'],
        'cuisine_type': 'american',
        'preference': 'chef_special',
        'preferred_sauce': 'Garlic herb butter',
        'prep_time': 40,
        'spice_level': 'mild',
        'ingredients': 'Prime rib eye steak, potatoes, asparagus, butter, garlic',
        'rating': 4.9,
        'is_available': True,
        'dietary_tags': [],
        'allergens': ['dairy'],
    },
    {
        'name': 'Vegetable Stir Fry',
        'description': 'Mixed vegetables with tofu in garlic and ginger sauce over rice',
        'price': 11.99,
        'category': categories['mains'],
        'cuisine_type': 'asian',
        'preference': 'vegetarian',
        'preferred_sauce': 'Garlic ginger sauce',
        'prep_time': 20,
        'spice_level': 'medium',
        'ingredients': 'Tofu, broccoli, bell peppers, carrots, garlic, ginger, soy sauce, rice',
        'rating': 4.3,
        'is_available': True,
        'dietary_tags': ['vegan', 'vegetarian'],
        'allergens': ['soy'],
    },
    {
        'name': 'Shrimp Scampi',
        'description': 'Fresh shrimp with garlic, white wine, and lemon butter sauce',
        'price': 16.99,
        'category': categories['mains'],
        'cuisine_type': 'italian',
        'preference': 'chef_special',
        'preferred_sauce': 'White wine lemon butter',
        'prep_time': 25,
        'spice_level': 'mild',
        'ingredients': 'Shrimp, garlic, white wine, butter, lemon, pasta',
        'rating': 4.7,
        'is_available': True,
        'dietary_tags': [],
        'allergens': ['shellfish', 'dairy', 'wheat'],
    },
    {
        'name': 'Mushroom Risotto',
        'description': 'Creamy arborio rice with wild mushrooms, truffle oil, and parmesan',
        'price': 13.99,
        'category': categories['mains'],
        'cuisine_type': 'italian',
        'preference': 'vegetarian',
        'preferred_sauce': 'Truffle oil and parmesan',
        'prep_time': 30,
        'spice_level': 'mild',
        'ingredients': 'Arborio rice, mushrooms, white wine, parmesan, truffle oil, broth',
        'rating': 4.6,
        'is_available': True,
        'dietary_tags': ['vegetarian'],
        'allergens': ['dairy'],
    },
    {
        'name': 'Chocolate Lava Cake',
        'description': 'Warm chocolate cake with molten center, served with vanilla ice cream',
        'price': 7.99,
        'category': categories['desserts'],
        'cuisine_type': 'fusion',
        'preference': 'dessert',
        'preferred_sauce': 'Chocolate ganache',
        'prep_time': 15,
        'spice_level': 'mild',
        'ingredients': 'Dark chocolate, butter, eggs, flour, sugar, vanilla ice cream',
        'rating': 4.8,
        'is_available': True,
        'dietary_tags': ['vegetarian'],
        'allergens': ['eggs', 'dairy', 'wheat'],
    },
    {
        'name': 'Tiramisu',
        'description': 'Classic Italian dessert with mascarpone, coffee, and cocoa powder',
        'price': 6.99,
        'category': categories['desserts'],
        'cuisine_type': 'italian',
        'preference': 'dessert',
        'preferred_sauce': 'Coffee mascarpone',
        'prep_time': 10,
        'spice_level': 'mild',
        'ingredients': 'Mascarpone, coffee, cocoa powder, ladyfingers, eggs, sugar',
        'rating': 4.7,
        'is_available': True,
        'dietary_tags': ['vegetarian'],
        'allergens': ['eggs', 'dairy', 'wheat'],
    },
    {
        'name': 'Cheesecake',
        'description': 'New York style cheesecake with strawberry compote and whipped cream',
        'price': 6.99,
        'category': categories['desserts'],
        'cuisine_type': 'american',
        'preference': 'dessert',
        'preferred_sauce': 'Strawberry compote',
        'prep_time': 10,
        'spice_level': 'mild',
        'ingredients': 'Cream cheese, graham cracker crust, strawberries, whipped cream',
        'rating': 4.6,
        'is_available': True,
        'dietary_tags': ['vegetarian'],
        'allergens': ['eggs', 'dairy', 'wheat'],
    },
]

# Clear existing dishes
print("Clearing existing dishes...")
Dish.objects.all().delete()

# Create new dishes
created_count = 0
for dish_data in dishes_data:
    # Extract dietary tags and allergens for M2M relationships
    dietary_tags_names = dish_data.pop('dietary_tags', [])
    allergens_names = dish_data.pop('allergens', [])
    
    # Create the dish
    dish = Dish.objects.create(**dish_data)
    
    # Add dietary tags
    for tag_name in dietary_tags_names:
        if tag_name in dietary_tags_list:
            dish.dietary_tags.add(dietary_tags_list[tag_name])
    
    # Add allergens
    for allergen_name in allergens_names:
        if allergen_name in allergens_list:
            dish.allergens.add(allergens_list[allergen_name])
    
    created_count += 1
    print(f"✓ Created: {dish.name} - ${dish.price} ({dish.get_cuisine_type_display()})")

print(f"\n✓ Successfully created {created_count} dishes with all attributes!")
