from django.core.management.base import BaseCommand
from menu.models import Category, DietaryTag, Dish, Allergen


class Command(BaseCommand):
    help = 'Populate the database with sample categories and dietary tags'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data population...'))

        # Create Categories
        categories_data = [
            {
                'name': 'appetizers',
                'description': 'Light starters to begin your meal',
                'icon': '🥗',
                'display_order': 1,
            },
            {
                'name': 'mains',
                'description': 'Main course dishes',
                'icon': '🍽️',
                'display_order': 2,
            },
            {
                'name': 'desserts',
                'description': 'Sweet treats to end your meal',
                'icon': '🍰',
                'display_order': 3,
            },
            {
                'name': 'beverages',
                'description': 'Drinks and beverages',
                'icon': '🥤',
                'display_order': 4,
            },
        ]

        for category_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=category_data['name'],
                defaults={
                    'description': category_data['description'],
                    'icon': category_data['icon'],
                    'display_order': category_data['display_order'],
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created category: {category.get_name_display()}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'✓ Category already exists: {category.get_name_display()}')
                )

        # Create Dietary Tags
        tags_data = [
            {
                'name': 'vegetarian',
                'description': 'No meat',
                'icon': '🌿',
                'color': '#28a745',
            },
            {
                'name': 'vegan',
                'description': 'No animal products',
                'icon': '🌱',
                'color': '#20c997',
            },
            {
                'name': 'gluten_free',
                'description': 'Gluten-free option',
                'icon': '🌾',
                'color': '#ffc107',
            },
            {
                'name': 'dairy_free',
                'description': 'No dairy products',
                'icon': '🥛',
                'color': '#17a2b8',
            },
            {
                'name': 'keto',
                'description': 'Low carb, high fat',
                'icon': '🥩',
                'color': '#e83e8c',
            },
        ]

        for tag_data in tags_data:
            tag, created = DietaryTag.objects.get_or_create(
                name=tag_data['name'],
                defaults={
                    'description': tag_data['description'],
                    'icon': tag_data['icon'],
                    'color': tag_data['color'],
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created dietary tag: {tag.get_name_display()}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'✓ Dietary tag already exists: {tag.get_name_display()}')
                )

        # Update existing dishes with categories and tags
        mains_category = Category.objects.get(name='mains')
        vegetarian_tag = DietaryTag.objects.get(name='vegetarian')

        # Update all existing dishes to have a default category and some tags
        for dish in Dish.objects.all():
            if not dish.category:
                dish.category = mains_category
                dish.save()
                self.stdout.write(f'✓ Updated dish: {dish.name} (assigned to Mains)')

            # Add vegetarian tag to dishes with vegetarian preference
            if dish.preference in ['vegetarian', 'vegan'] and not dish.dietary_tags.filter(name='vegetarian').exists():
                dish.dietary_tags.add(vegetarian_tag)
                self.stdout.write(f'✓ Added dietary tag to: {dish.name}')

            # Create Allergen entries
            allergens_data = [
                {'name': 'nuts', 'description': 'Contains tree nuts or peanuts'},
                {'name': 'dairy', 'description': 'Contains milk or dairy products'},
                {'name': 'eggs', 'description': 'Contains eggs'},
                {'name': 'shellfish', 'description': 'Contains shellfish'},
                {'name': 'soy', 'description': 'Contains soy'},
                {'name': 'wheat', 'description': 'Contains wheat/gluten'},
            ]

            for a in allergens_data:
                allergen, created = Allergen.objects.get_or_create(name=a['name'], defaults={'description': a['description']})
                if created:
                    self.stdout.write(self.style.SUCCESS(f'✓ Created allergen: {allergen.get_name_display()}'))
                else:
                    self.stdout.write(self.style.WARNING(f'✓ Allergen already exists: {allergen.get_name_display()}'))

        self.stdout.write(
            self.style.SUCCESS('\n✓ Data population completed successfully!')
        )
