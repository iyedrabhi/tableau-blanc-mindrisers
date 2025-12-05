from django.db.models import Q, F, Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Value
from django.db.models.functions import Lower
from django.views.decorators.csrf import csrf_exempt

from .forms import DishForm, DishFilterForm
from .models import Dish, Category, DietaryTag, Allergen


# API endpoint for dish count (for iyed integration)
@csrf_exempt
def api_dishes_count(request):
    """Return count of all dishes"""
    count = Dish.objects.count()
    return JsonResponse({'count': count})


def dish_list(request):
    """List dishes with advanced Phase 1 filtering and sorting."""

    # Initialize form with GET parameters (allow empty form for display)
    filter_form = DishFilterForm(request.GET or None)
    
    # Start with all dishes
    dishes = Dish.objects.prefetch_related('dietary_tags', 'category')
    
    # Initialize filter variables
    search_query = ''
    price_range = None
    min_price = None
    max_price = None
    categories = None
    dietary_tags = None
    allergens = None
    prep_time = None
    only_available = False
    sort_by = None
    
    # Apply filters from form - only if form is valid AND has data
    if request.GET and filter_form.is_valid():
        # Search filter
        search_query = filter_form.cleaned_data.get('search', '').strip()
        if search_query:
            dishes = dishes.filter(
                Q(name__icontains=search_query)
                | Q(description__icontains=search_query)
                | Q(preferred_sauce__icontains=search_query)
            )
        
        # Price range filter - either use preset or custom min/max
        price_range = filter_form.cleaned_data.get('price_range')
        min_price = filter_form.cleaned_data.get('min_price')
        max_price = filter_form.cleaned_data.get('max_price')
        
        if price_range == 'budget':
            dishes = dishes.filter(price__lt=10)
        elif price_range == 'mid':
            dishes = dishes.filter(price__gte=10, price__lte=25)
        elif price_range == 'premium':
            dishes = dishes.filter(price__gt=25)
        else:
            # Apply custom min/max if provided
            if min_price is not None:
                dishes = dishes.filter(price__gte=min_price)
            if max_price is not None:
                dishes = dishes.filter(price__lte=max_price)
        
        # Category filter - get from GET params
        category_ids = request.GET.getlist('categories')
        if category_ids:
            categories = Category.objects.filter(id__in=category_ids)
            dishes = dishes.filter(category__in=categories)
        
        # Dietary tags filter - get from GET params
        dietary_tag_ids = request.GET.getlist('dietary_tags')
        if dietary_tag_ids:
            dietary_tags = DietaryTag.objects.filter(id__in=dietary_tag_ids)
            for tag in dietary_tags:
                dishes = dishes.filter(dietary_tags=tag)
        
        # Allergens filter - get from GET params since form may not include it
        allergen_ids = request.GET.getlist('allergens')
        if allergen_ids:
            allergens = Allergen.objects.filter(id__in=allergen_ids)
            for allergen in allergens:
                dishes = dishes.filter(allergens=allergen)
        
        # Prep time filter
        prep_time = filter_form.cleaned_data.get('prep_time')
        if prep_time == 'quick':
            dishes = dishes.filter(prep_time__lt=15)
        elif prep_time == 'moderate':
            dishes = dishes.filter(prep_time__gte=15, prep_time__lte=30)
        elif prep_time == 'takes_time':
            dishes = dishes.filter(prep_time__gt=30)
        
        # Availability filter
        only_available = filter_form.cleaned_data.get('only_available')
        if only_available:
            dishes = dishes.filter(is_available=True)
        
        # Apply sorting
        sort_by = filter_form.cleaned_data.get('sort_by')
        if sort_by == 'name_asc':
            dishes = dishes.order_by(Lower('name'))
        elif sort_by == 'name_desc':
            dishes = dishes.order_by(Lower('name')).reverse()
        elif sort_by == 'price_asc':
            dishes = dishes.order_by('price')
        elif sort_by == 'price_desc':
            dishes = dishes.order_by('-price')
        elif sort_by == 'prep_time_asc':
            dishes = dishes.order_by('prep_time')
        elif sort_by == 'popularity':
            dishes = dishes.order_by('-times_ordered')
        elif sort_by == 'rating_desc':
            dishes = dishes.order_by('-rating')
        elif sort_by == 'newest':
            dishes = dishes.order_by('-created_at')
        else:
            dishes = dishes.order_by('name')
    else:
        # If form not valid, order by name by default
        dishes = dishes.order_by('name')
    
    # Remove duplicates if multiple dietary tags filtered
    dishes = dishes.distinct()
    
    # Build applied filters list for display
    filters_applied = []
    if search_query:
        filters_applied.append(('Search', f'"{search_query}"', 'search'))
    if price_range:
        price_labels = {'budget': 'Budget (< $10)', 'mid': 'Mid-Range ($10-25)', 'premium': 'Premium (> $25)'}
        filters_applied.append(('Price', price_labels.get(price_range), 'price_range'))
    if min_price is not None or max_price is not None:
        price_text = f"${min_price or '0'}-${max_price or '∞'}"
        filters_applied.append(('Custom Price', price_text, 'price'))
    if categories:
        for cat in categories:
            filters_applied.append(('Category', cat.get_name_display(), f'cat_{cat.id}'))
    if dietary_tags:
        for tag in dietary_tags:
            filters_applied.append(('Dietary', tag.get_name_display(), f'tag_{tag.id}'))
    if prep_time:
        prep_labels = {'quick': 'Quick (< 15 min)', 'moderate': 'Moderate (15-30 min)', 'takes_time': 'Takes Time (> 30 min)'}
        filters_applied.append(('Prep Time', prep_labels.get(prep_time), 'prep_time'))
    if only_available:
        filters_applied.append(('Status', 'Available Only', 'available'))
    
    context = {
        'dishes': dishes,
        'dishes_count': dishes.count(),
        'total_dishes': Dish.objects.count(),
        'filter_form': filter_form,
        'filters_applied': filters_applied,
        'categories': Category.objects.all(),
        'dietary_tags': DietaryTag.objects.all(),
        'allergens': Allergen.objects.all(),
        'selected_categories': request.GET.getlist('categories'),
        'selected_dietary_tags': request.GET.getlist('dietary_tags'),
        'selected_allergens': request.GET.getlist('allergens'),
    }
    
    return render(request, 'menu/dish_list.html', context)


def dish_create(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if request.method == "POST":
        form = DishForm(request.POST)
        if form.is_valid():
            form.save()
            if is_ajax:
                return JsonResponse({"success": True, "redirect": True})
            return redirect("menu:dish_list")
        else:
            # Form has errors
            if is_ajax:
                return render(request, "menu/dish_form.html", {"form": form, "title": "Add Dish"}, status=400)
    else:
        form = DishForm()
    
    return render(request, "menu/dish_form.html", {"form": form, "title": "Add Dish"})


def dish_update(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    
    if request.method == "POST":
        form = DishForm(request.POST, instance=dish)
        if form.is_valid():
            form.save()
            return redirect("menu:dish_list")
        else:
            # Form has errors, show the form again
            return render(
                request,
                "menu/dish_form.html",
                {"form": form, "title": f"Edit {dish.name}", "dish": dish}
            )
    else:
        form = DishForm(instance=dish)
    
    return render(
        request,
        "menu/dish_form.html",
        {"form": form, "title": f"Edit {dish.name}", "dish": dish},
    )


def dish_delete(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    if request.method == "POST":
        dish.delete()
        return redirect("menu:dish_list")
    return render(request, "menu/dish_confirm_delete.html", {"dish": dish})


def landing(request):
    """Render the Cure & Simple marketing landing page."""
    return render(request, 'menu/landing.html', {})
