from django import forms
import django_filters

from .models import Dish, Category, DietaryTag, Allergen


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = [
            "name",
            "description",
            "price",
            "preferred_sauce",
            "preference",
            "is_available",
            "category",
            "cuisine_type",
            "prep_time",
            "dietary_tags",
            "allergens",
            "spice_level",
            "ingredients",
            "rating",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "preferred_sauce": forms.TextInput(
                attrs={"placeholder": "e.g. Tahini drizzle, Chimichurri"}
            ),
            "category": forms.Select(attrs={"class": "form-control"}),
            "cuisine_type": forms.Select(attrs={"class": "form-control"}),
            "prep_time": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
            "dietary_tags": forms.CheckboxSelectMultiple(),
            "allergens": forms.CheckboxSelectMultiple(),
            "spice_level": forms.Select(attrs={"class": "form-control"}),
            "ingredients": forms.Textarea(attrs={"rows": 3, "placeholder": "e.g. tomato, basil, garlic"}),
            "rating": forms.NumberInput(attrs={"class": "form-control", "min": "0", "max": "5", "step": "0.1"}),
        }


class DishFilterForm(forms.Form):
    """Advanced filtering form for dishes."""

    SORT_CHOICES = [
        ("", "Sort by..."),
        ("name_asc", "Name (A→Z)"),
        ("name_desc", "Name (Z→A)"),
        ("price_asc", "Price (Low→High)"),
        ("price_desc", "Price (High→Low)"),
        ("prep_time_asc", "Prep Time (Fastest)"),
        ("newest", "Newest First"),
        ("popularity", "Most Popular"),
        ("rating_desc", "Highest Rating"),
    ]

    PRICE_RANGE_CHOICES = [
        ("", "All Prices"),
        ("budget", "Budget (< $10)"),
        ("mid", "Mid-Range ($10-25)"),
        ("premium", "Premium (> $25)"),
    ]

    PREP_TIME_CHOICES = [
        ("", "All Prep Times"),
        ("quick", "Quick (< 15 min)"),
        ("moderate", "Moderate (15-30 min)"),
        ("takes_time", "Takes Time (> 30 min)"),
    ]

    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Search dishes...",
            "id": "search-input",
        }),
    )

    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Min price",
            "step": "0.01",
            "id": "min-price",
        }),
    )

    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Max price",
            "step": "0.01",
            "id": "max-price",
        }),
    )

    price_range = forms.ChoiceField(
        required=False,
        choices=PRICE_RANGE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    categories = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "filter-checkbox"}),
    )

    dietary_tags = forms.ModelMultipleChoiceField(
        required=False,
        queryset=DietaryTag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "filter-checkbox"}),
    )

    prep_time = forms.ChoiceField(
        required=False,
        choices=PREP_TIME_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    only_available = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Only show available dishes",
    )

    sort_by = forms.ChoiceField(
        required=False,
        choices=SORT_CHOICES,
        widget=forms.Select(attrs={"class": "form-control", "id": "sort-select"}),
    )
