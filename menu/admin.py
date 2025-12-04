from django.contrib import admin
from .models import Dish, Category, DietaryTag, Allergen


class DietaryTagInline(admin.TabularInline):
    model = Dish.dietary_tags.through
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "display_order")
    list_editable = ("display_order",)
    ordering = ("display_order",)


@admin.register(DietaryTag)
class DietaryTagAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "color")
    prepopulated_fields = {"color": ("name",)}


@admin.register(Allergen)
class AllergenAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    ordering = ("name",)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_available", "prep_time", "times_ordered")
    list_filter = ("category", "dietary_tags", "allergens", "is_available", "preference")
    search_fields = ("name", "description", "preferred_sauce")
    filter_horizontal = ("dietary_tags", "allergens")
    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "description", "category")
        }),
        ("Pricing & Availability", {
            "fields": ("price", "is_available")
        }),
        ("Preparation", {
            "fields": ("preferred_sauce", "prep_time", "preference")
        }),
        ("Tags & Ratings", {
            "fields": ("dietary_tags", "allergens", "times_ordered", "rating")
        }),
    )
    readonly_fields = ("created_at", "updated_at")
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ["created_at", "updated_at"]
        return self.readonly_fields
