import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant.settings')
django.setup()

from menu.models import Dish

dishes_data = [
    {
        'name': 'Margherita Pizza',
        'description': 'Classic Italian pizza with fresh mozzarella, basil, and tomato sauce',
        'price': 12.99,
        'category': 'Pizza',
        'image': 'pizza_margherita.jpg',
        'is_available': True,
    },
    {
        'name': 'Spaghetti Carbonara',
        'description': 'Traditional Italian pasta with eggs, bacon, and parmesan cheese',
        'price': 13.99,
        'category': 'Pasta',
        'image': 'pasta_carbonara.jpg',
        'is_available': True,
    },
    {
        'name': 'Grilled Salmon',
        'description': 'Fresh Atlantic salmon fillet with lemon butter sauce',
        'price': 18.99,
        'category': 'Seafood',
        'image': 'salmon_grilled.jpg',
        'is_available': True,
    },
    {
        'name': 'Caesar Salad',
        'description': 'Crisp romaine lettuce with parmesan, croutons, and caesar dressing',
        'price': 9.99,
        'category': 'Salad',
        'image': 'salad_caesar.jpg',
        'is_available': True,
    },
    {
        'name': 'Beef Burger',
        'description': 'Juicy beef patty with cheddar cheese, lettuce, tomato, and special sauce',
        'price': 11.99,
        'category': 'Burger',
        'image': 'burger_beef.jpg',
        'is_available': True,
    },
    {
        'name': 'Chicken Tikka Masala',
        'description': 'Tender chicken in creamy tomato and spice sauce with rice',
        'price': 14.99,
        'category': 'Indian',
        'image': 'curry_chicken_tikka.jpg',
        'is_available': True,
    },
    {
        'name': 'Pad Thai',
        'description': 'Stir-fried rice noodles with shrimp, peanuts, and lime',
        'price': 13.99,
        'category': 'Thai',
        'image': 'pad_thai.jpg',
        'is_available': True,
    },
    {
        'name': 'Tacos Al Pastor',
        'description': 'Three soft corn tortillas with marinated pork, pineapple, and onions',
        'price': 10.99,
        'category': 'Mexican',
        'image': 'tacos_al_pastor.jpg',
        'is_available': True,
    },
    {
        'name': 'Falafel Wrap',
        'description': 'Crispy falafel balls in pita wrap with tahini sauce and vegetables',
        'price': 9.99,
        'category': 'Vegetarian',
        'image': 'wrap_falafel.jpg',
        'is_available': True,
    },
    {
        'name': 'Beef Steak',
        'description': '12oz prime rib eye steak with garlic mashed potatoes and asparagus',
        'price': 24.99,
        'category': 'Steak',
        'image': 'steak_ribeye.jpg',
        'is_available': True,
    },
    {
        'name': 'Lobster Bisque',
        'description': 'Creamy soup with lobster meat, shallots, and a hint of brandy',
        'price': 8.99,
        'category': 'Soup',
        'image': 'bisque_lobster.jpg',
        'is_available': True,
    },
    {
        'name': 'Vegetable Stir Fry',
        'description': 'Mixed vegetables with tofu in garlic and ginger sauce over rice',
        'price': 11.99,
        'category': 'Vegetarian',
        'image': 'stirfry_veg.jpg',
        'is_available': True,
    },
    {
        'name': 'Shrimp Scampi',
        'description': 'Fresh shrimp with garlic, white wine, and lemon butter sauce',
        'price': 16.99,
        'category': 'Seafood',
        'image': 'shrimp_scampi.jpg',
        'is_available': True,
    },
    {
        'name': 'Mushroom Risotto',
        'description': 'Creamy arborio rice with wild mushrooms, truffle oil, and parmesan',
        'price': 13.99,
        'category': 'Vegetarian',
        'image': 'risotto_mushroom.jpg',
        'is_available': True,
    },
    {
        'name': 'Duck Confit',
        'description': 'Slow-cooked duck leg with skin, served with potato and cherry gastrique',
        'price': 19.99,
        'category': 'Poultry',
        'image': 'duck_confit.jpg',
        'is_available': True,
    },
    {
        'name': 'Sushi Roll Platter',
        'description': 'Assorted sushi rolls including California, Spicy Tuna, and Vegetable',
        'price': 17.99,
        'category': 'Japanese',
        'image': 'sushi_platter.jpg',
        'is_available': True,
    },
    {
        'name': 'Lamb Kebab',
        'description': 'Grilled lamb skewers with yogurt marinade, served with pita and tzatziki',
        'price': 15.99,
        'category': 'Mediterranean',
        'image': 'kebab_lamb.jpg',
        'is_available': True,
    },
    {
        'name': 'Chocolate Lava Cake',
        'description': 'Warm chocolate cake with molten center, served with vanilla ice cream',
        'price': 7.99,
        'category': 'Dessert',
        'image': 'cake_chocolate_lava.jpg',
        'is_available': True,
    },
    {
        'name': 'Tiramisu',
        'description': 'Classic Italian dessert with mascarpone, coffee, and cocoa powder',
        'price': 6.99,
        'category': 'Dessert',
        'image': 'tiramisu.jpg',
        'is_available': True,
    },
    {
        'name': 'Cheesecake',
        'description': 'New York style cheesecake with strawberry compote and whipped cream',
        'price': 6.99,
        'category': 'Dessert',
        'image': 'cheesecake.jpg',
        'is_available': True,
    },
]

# Clear existing dishes
Dish.objects.all().delete()

# Create new dishes
created_count = 0
for dish_data in dishes_data:
    dish, created = Dish.objects.get_or_create(
        name=dish_data['name'],
        defaults=dish_data
    )
    if created:
        created_count += 1
        print(f"✓ Created: {dish.name} - ${dish.price}")

print(f"\n✓ Successfully created {created_count} dishes!")
