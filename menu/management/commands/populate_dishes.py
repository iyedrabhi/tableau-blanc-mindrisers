from django.core.management.base import BaseCommand
from menu.models import Dish

class Command(BaseCommand):
    help = 'Populate database with 20 example dishes'

    def handle(self, *args, **options):
        dishes_data = [
            {
                'name': 'Margherita Pizza',
                'description': 'Classic Italian pizza with fresh mozzarella, basil, and tomato sauce',
                'price': 12.99,
                'cuisine_type': 'italian',
                'preference': 'chef_special',
                'spice_level': 'mild',
                'prep_time': 20,
                'is_available': True,
            },
            {
                'name': 'Spaghetti Carbonara',
                'description': 'Traditional Italian pasta with eggs, bacon, and parmesan cheese',
                'price': 13.99,
                'cuisine_type': 'italian',
                'preference': 'chef_special',
                'spice_level': 'mild',
                'prep_time': 18,
                'is_available': True,
            },
            {
                'name': 'Grilled Salmon',
                'description': 'Fresh Atlantic salmon fillet with lemon butter sauce',
                'price': 18.99,
                'cuisine_type': 'mediterranean',
                'preference': 'chef_special',
                'spice_level': 'mild',
                'prep_time': 25,
                'is_available': True,
            },
            {
                'name': 'Caesar Salad',
                'description': 'Crisp romaine lettuce with parmesan, croutons, and caesar dressing',
                'price': 9.99,
                'cuisine_type': 'american',
                'preference': 'vegetarian',
                'spice_level': 'mild',
                'prep_time': 10,
                'is_available': True,
            },
            {
                'name': 'Beef Burger',
                'description': 'Juicy beef patty with cheddar cheese, lettuce, tomato, and special sauce',
                'price': 11.99,
                'cuisine_type': 'american',
                'preference': 'chef_special',
                'spice_level': 'mild',
                'prep_time': 15,
                'is_available': True,
            },
            {
                'name': 'Chicken Tikka Masala',
                'description': 'Tender chicken in creamy tomato and spice sauce with rice',
                'price': 14.99,
                'cuisine_type': 'asian',
                'preference': 'chef_special',
                'spice_level': 'medium',
                'prep_time': 30,
                'is_available': True,
            },
            {
                'name': 'Pad Thai',
                'description': 'Stir-fried rice noodles with shrimp, peanuts, and lime',
                'price': 13.99,
                'cuisine_type': 'asian',
                'preference': 'chef_special',
                'spice_level': 'medium',
                'prep_time': 20,
                'is_available': True,
            },
            {
                'name': 'Tacos Al Pastor',
                'description': 'Three soft corn tortillas with marinated pork, pineapple, and onions',
                'price': 10.99,
                'cuisine_type': 'mexican',
                'preference': 'chef_special',
                'spice_level': 'medium',
                'prep_time': 15,
                'is_available': True,
            },
            {
                'name': 'Falafel Wrap',
                'description': 'Crispy falafel balls in pita wrap with tahini sauce and vegetables',
                'price': 9.99,
                'cuisine_type': 'mediterranean',
                'preference': 'vegetarian',
                'spice_level': 'mild',
                'prep_time': 12,
                'is_available': True,
            },
            {
                'name': 'Beef Steak',
                'description': '12oz prime rib eye steak with garlic mashed potatoes and asparagus',
                'price': 24.99,
                'cuisine_type': 'american',
                'preference': 'chef_special',
                'spice_level': 'mild',
                'prep_time': 35,
                'is_available': True,
            },
            {
                'name': 'Lobster Bisque',
                'description': 'Creamy soup with lobster meat, shallots, and a hint of brandy',
                'price': 8.99,
                'cuisine_type': 'mediterranean',
                'preference': 'chef_special',
                'spice_level': 'mild',
                'prep_time': 25,
                'is_available': True,
            },
            {
                'name': 'Vegetable Stir Fry',
                'description': 'Mixed vegetables with tofu in garlic and ginger sauce over rice',
                'price': 11.99,
                'cuisine_type': 'asian',
                'preference': 'vegetarian',
                'spice_level': 'medium',
                'prep_time': 18,
                'is_available': True,
            },
            {
                'name': 'Shrimp Scampi',
                'description': 'Fresh shrimp with garlic, white wine, and lemon butter sauce',
                'price': 16.99,
                'cuisine_type': 'mediterranean',
                'preference': 'chef_special',
                'spice_level': 'mild',
                'prep_time': 22,
                'is_available': True,
            },
            {
                'name': 'Mushroom Risotto',
                'description': 'Creamy arborio rice with wild mushrooms, truffle oil, and parmesan',
                'price': 13.99,
                'cuisine_type': 'italian',
                'preference': 'vegetarian',
                'spice_level': 'mild',
                'prep_time': 28,
                'is_available': True,
            },
            {
                'name': 'Duck Confit',
                'description': 'Slow-cooked duck leg with skin, served with potato and cherry gastrique',
                'price': 19.99,
                'cuisine_type': 'french',
                'preference': 'chef_special',
                'spice_level': 'mild',
                'prep_time': 45,
                'is_available': True,
            },
            {
                'name': 'Sushi Roll Platter',
                'description': 'Assorted sushi rolls including California, Spicy Tuna, and Vegetable',
                'price': 17.99,
                'cuisine_type': 'asian',
                'preference': 'chef_special',
                'spice_level': 'mild',
                'prep_time': 20,
                'is_available': True,
            },
            {
                'name': 'Lamb Kebab',
                'description': 'Grilled lamb skewers with yogurt marinade, served with pita and tzatziki',
                'price': 15.99,
                'cuisine_type': 'mediterranean',
                'preference': 'chef_special',
                'spice_level': 'medium',
                'prep_time': 25,
                'is_available': True,
            },
            {
                'name': 'Chocolate Lava Cake',
                'description': 'Warm chocolate cake with molten center, served with vanilla ice cream',
                'price': 7.99,
                'cuisine_type': 'fusion',
                'preference': 'dessert',
                'spice_level': 'mild',
                'prep_time': 12,
                'is_available': True,
            },
            {
                'name': 'Tiramisu',
                'description': 'Classic Italian dessert with mascarpone, coffee, and cocoa powder',
                'price': 6.99,
                'cuisine_type': 'italian',
                'preference': 'dessert',
                'spice_level': 'mild',
                'prep_time': 15,
                'is_available': True,
            },
            {
                'name': 'Cheesecake',
                'description': 'New York style cheesecake with strawberry compote and whipped cream',
                'price': 6.99,
                'cuisine_type': 'american',
                'preference': 'dessert',
                'spice_level': 'mild',
                'prep_time': 10,
                'is_available': True,
            },
        ]

        # Clear existing dishes
        Dish.objects.all().delete()
        self.stdout.write(self.style.WARNING('Cleared existing dishes'))

        # Create new dishes
        created_count = 0
        for dish_data in dishes_data:
            dish, created = Dish.objects.get_or_create(
                name=dish_data['name'],
                defaults=dish_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {dish.name} - ${dish.price}'))

        self.stdout.write(self.style.SUCCESS(f'\n✓ Successfully created {created_count} dishes!'))
