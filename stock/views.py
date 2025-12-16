from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.contrib import messages
from django.db.models import Sum, Min
from django.db.models.functions import Lower
from types import SimpleNamespace
from django.utils import timezone
from datetime import timedelta
from .models import StockItem, OrderItem
from .forms import StockItemForm, SignUpForm
from .utils import is_manager  # utilitaire qui vérifie si l'utilisateur est manager


# -------------------------
# Redirection après login
# -------------------------
@login_required
def role_redirect(request):
    profile = getattr(request.user, "profile", None)
    if profile:
        if profile.role == "manager":
            return redirect("stock_list")
        elif profile.role == "chef":
            return redirect("stock_list")
        elif profile.role == "staff":
            return redirect("stock_list")
    return redirect("stock_list")


# -------------------------
# Liste des stocks (regroupée par nom pour éviter les doublons)
# -------------------------
@login_required
def stock_list(request):
    category = request.GET.get("category", "all")

    if category != "all":
        queryset = StockItem.objects.filter(category=category)
    else:
        queryset = StockItem.objects.all()

    # Regroupe par nom (insensible à la casse) et catégorie, additionne quantités et seuils, prend la date d'expiration la plus proche
    grouped = (
        queryset
        .annotate(normalized_name=Lower('name'))
        .values('normalized_name', 'category')
        .annotate(total_quantity=Sum('quantity'), total_threshold=Sum('threshold'), earliest_expiration=Min('expiration_date'))
        .order_by('normalized_name', 'category')
    )

    def unit_for_category(cat):
        if cat in ["Légume", "Fruit", "Viande"]:
            return "kg"
        elif cat == "Boisson":
            return "L"
        elif cat == "Épice":
            return "g"
        else:
            return "u"

    items = []
    today = timezone.now().date()
    for g in grouped:
        name_lower = g['normalized_name']
        category = g['category']
        quantity = g['total_quantity'] or 0
        threshold = g['total_threshold'] or 0
        exp = g['earliest_expiration']

        is_expired = False
        is_expiring_soon = False
        if exp:
            is_expired = exp < today
            is_expiring_soon = today <= exp <= today + timedelta(days=7)

        is_low_stock = quantity <= threshold

        # Limit representative query to matching name (case-insensitive) AND category
        rep_qs = queryset.filter(name__iexact=name_lower, category=category)
        rep = rep_qs.first()

        unit = unit_for_category(category) if category else 'u'

        rep_id = rep.id if rep else None
        display_name = rep.name if rep else name_lower

        items.append(SimpleNamespace(
            id=rep_id,
            name=display_name,
            category=category,
            quantity=quantity,
            threshold=threshold,
            expiration_date=exp,
            is_expired=is_expired,
            is_expiring_soon=is_expiring_soon,
            is_low_stock=is_low_stock,
            get_unit=unit,
        ))

    categories = (
        StockItem.objects.values_list("category", flat=True)
        .distinct()
        .order_by("category")
    )

    expired_items = [item for item in items if item.is_expired]
    expiring_soon_items = [item for item in items if item.is_expiring_soon]
    low_stock_items = [item for item in items if item.is_low_stock]

    return render(request, "stock/stock_list.html", {
        "items": items,
        "categories": categories,
        "selected_category": category,
        "expired_items": expired_items,
        "expiring_soon_items": expiring_soon_items,
        "low_stock_items": low_stock_items,
    })


# -------------------------
# Création d’un stock (manager uniquement)
# -------------------------
@login_required
@user_passes_test(is_manager)
def stock_create(request):
    if request.method == "POST":
        form = StockItemForm(request.POST)
        if form.is_valid():
            # Normalize name and prevent exact duplicate (same name + same category, case-insensitive name)
            name = form.cleaned_data.get('name', '').strip()
            category = form.cleaned_data.get('category')
            existing = StockItem.objects.filter(name__iexact=name, category=category).first()
            if existing:
                messages.warning(request, "⚠️ Cet ingrédient avec cette catégorie existe déjà. Vous pouvez le modifier pour ajouter du stock.")
                return redirect('stock_update', id=existing.id)

            # Only create the ingredient record; quantity from the form is preserved (clamped >= 0)
            item = form.save(commit=False)
            item.name = name
            # Preserve quantity if provided, otherwise default to 0. Ensure non-negative integer.
            qty_val = form.cleaned_data.get('quantity')
            try:
                qty = int(qty_val) if qty_val is not None else 0
            except (TypeError, ValueError):
                qty = 0
            item.quantity = max(0, qty)

            # Preserve threshold value provided in the form (fallback to 0)
            threshold_val = form.cleaned_data.get('threshold')
            item.threshold = threshold_val if threshold_val is not None else 0
            item.save()
            messages.success(request, f"✅ Ingrédient créé (quantité initiale {item.quantity}, seuil enregistré).")
            return redirect("stock_list")
    else:
        form = StockItemForm()
    return render(request, "stock/stock_form.html", {"form": form})


# -------------------------
# Mise à jour d’un stock (manager uniquement)
# -------------------------
@login_required
@user_passes_test(is_manager)
def stock_update(request, id):
    item = get_object_or_404(StockItem, id=id)
    if request.method == "POST":
        form = StockItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("stock_list")
    else:
        form = StockItemForm(instance=item)
    return render(request, "stock/stock_form.html", {"form": form})


# -------------------------
# Suppression d’un stock (manager uniquement)
# -------------------------
@login_required
@user_passes_test(is_manager)
def stock_delete(request, id):
    item = get_object_or_404(StockItem, id=id)
    item.delete()
    return redirect("stock_list")


# -------------------------
# Inscription utilisateur avec rôle
# -------------------------
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "✅ Votre compte a été créé avec succès. Vous pouvez maintenant vous connecter."
            )
            return redirect("login")
    else:
        form = SignUpForm()
    return render(request, "stock/signup.html", {"form": form})


# -------------------------
# Déconnexion
# -------------------------
@login_required
def logout_simple(request):
    request.session.flush()
    logout(request)
    return redirect("login")


# -------------------------
# Création d’une commande (incrémente le stock — réception)
# -------------------------
@login_required
def create_order(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity"))
        product = get_object_or_404(StockItem, id=product_id)

        # Crée un OrderItem et applique l'incrémentation du stock
        order_item = OrderItem.objects.create(product=product, quantity=quantity)
        try:
            order_item.apply_stock()
            messages.success(request, f"✅ Commande enregistrée : {quantity} x {product.name} — stock mis à jour (+{quantity})")
        except ValueError as e:
            messages.error(request, str(e))

        return redirect("stock_list")
    else:
        products = StockItem.objects.all()
        return render(request, "stock/order_form.html", {"products": products})





