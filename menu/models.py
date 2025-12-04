from django.db import models


class Category(models.Model):
    """Restaurant menu categories."""

    class CategoryType(models.TextChoices):
        APPETIZERS = "appetizers", "Appetizers"
        MAINS = "mains", "Mains"
        DESSERTS = "desserts", "Desserts"
        BEVERAGES = "beverages", "Beverages"

    name = models.CharField(max_length=50, choices=CategoryType.choices, unique=True)
    description = models.CharField(max_length=200, blank=True)
    icon = models.CharField(max_length=50, default="🍽️", help_text="Emoji icon for the category")
    display_order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["display_order", "name"]

    def __str__(self) -> str:
        return f"{self.icon} {self.get_name_display()}"


class DietaryTag(models.Model):
    """Dietary restrictions and preferences."""

    class TagType(models.TextChoices):
        VEGETARIAN = "vegetarian", "Vegetarian"
        VEGAN = "vegan", "Vegan"
        GLUTEN_FREE = "gluten_free", "Gluten-free"
        DAIRY_FREE = "dairy_free", "Dairy-free"
        KETO = "keto", "Keto"

    name = models.CharField(max_length=50, choices=TagType.choices, unique=True)
    description = models.CharField(max_length=200, blank=True)
    icon = models.CharField(max_length=50, default="✓", help_text="Emoji icon for the tag")
    color = models.CharField(max_length=7, default="#28a745", help_text="Hex color for badge")

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.icon} {self.get_name_display()}"


class Allergen(models.Model):
    """Common allergens to exclude/filter."""

    class AllergenType(models.TextChoices):
        NUTS = "nuts", "Nuts"
        DAIRY = "dairy", "Dairy"
        EGGS = "eggs", "Eggs"
        SHELLFISH = "shellfish", "Shellfish"
        SOY = "soy", "Soy"
        WHEAT = "wheat", "Wheat/Gluten"

    name = models.CharField(max_length=50, choices=AllergenType.choices, unique=True)
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.get_name_display()}"


class Dish(models.Model):
    """Dish available in the restaurant menu."""

    class Preference(models.TextChoices):
        CHEF_SPECIAL = "chef_special", "Chef's Special"
        VEGETARIAN = "vegetarian", "Vegetarian"
        VEGAN = "vegan", "Vegan"
        SPICY = "spicy", "Spicy Lovers"
        KIDS = "kids", "Kids' Favorite"
        DESSERT = "dessert", "Dessert"
        BEVERAGE = "beverage", "Beverage"

    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    preferred_sauce = models.CharField(
        max_length=80,
        default="House Signature",
        help_text="Sauce pairing or garnish that best matches the dish.",
    )
    preference = models.CharField(
        max_length=20,
        choices=Preference.choices,
        default=Preference.CHEF_SPECIAL,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dishes",
    )
    dietary_tags = models.ManyToManyField(
        DietaryTag,
        blank=True,
        related_name="dishes",
    )
    allergens = models.ManyToManyField(
        Allergen,
        blank=True,
        related_name="dishes",
    )
    class CuisineType(models.TextChoices):
        ITALIAN = "italian", "Italian"
        MEXICAN = "mexican", "Mexican"
        ASIAN = "asian", "Asian"
        MEDITERRANEAN = "mediterranean", "Mediterranean"
        AMERICAN = "american", "American"
        FUSION = "fusion", "Fusion"

    cuisine_type = models.CharField(max_length=30, choices=CuisineType.choices, null=True, blank=True)
    class SpiceLevel(models.TextChoices):
        MILD = "mild", "Mild"
        MEDIUM = "medium", "Medium"
        HOT = "hot", "Hot"
        EXTRA_HOT = "extra_hot", "Extra Hot"

    spice_level = models.CharField(max_length=20, choices=SpiceLevel.choices, default=SpiceLevel.MILD)
    ingredients = models.TextField(blank=True, help_text="Comma-separated list of ingredients")
    prep_time = models.IntegerField(default=15, help_text="Preparation time in minutes")
    times_ordered = models.IntegerField(default=0, help_text="Number of times this dish has been ordered")
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        help_text="Average rating (0-5)",
    )
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.get_preference_display()})"

    @property
    def price_range(self) -> str:
        """Return price range category."""
        if self.price < 10:
            return "budget"
        elif self.price <= 25:
            return "mid"
        else:
            return "premium"

    @property
    def prep_time_category(self) -> str:
        """Return prep time category."""
        if self.prep_time < 15:
            return "quick"
        elif self.prep_time <= 30:
            return "moderate"
        else:
            return "takes_time"
