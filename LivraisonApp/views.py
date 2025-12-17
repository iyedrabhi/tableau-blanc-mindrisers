from django.shortcuts import render, get_object_or_404, redirect
from .models import Livraison
from .forms import LivraisonForm , ClientLivraisonSearchForm
# 🔽 IMPORTS API DRF À AJOUTER EN HAUT DU FICHIER
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import LivraisonSerializer
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

# LISTE GÉRANT AVEC FILTRES
def livraison_list(request):
    # Récupérer les filtres depuis l'URL (?statut=...&livreur=...)
    statut_filter = request.GET.get("statut", "").strip()
    livreur_filter = request.GET.get("livreur", "").strip()

    # Base queryset
    livraisons = Livraison.objects.all().order_by("-date_sortie")

    # Filtre par statut si choisi
    if statut_filter:
        livraisons = livraisons.filter(statut=statut_filter)

    # Filtre par livreur si choisi
    if livreur_filter:
        livraisons = livraisons.filter(id_livreur=livreur_filter)

    # Pour alimenter la liste déroulante des statuts
    statuts = Livraison.STATUT_LIVRAISON  # tes choices

    # Pour alimenter la liste des livreurs (ids distincts non nuls)
    livreurs = (
        Livraison.objects.exclude(id_livreur__isnull=True)
        .values_list("id_livreur", flat=True)
        .distinct()
    )

    context = {
        "livraisons": livraisons,
        "statuts": statuts,
        "livreurs": livreurs,
        "statut_filter": statut_filter,
        "livreur_filter": livreur_filter,
    }
    return render(request, "livraisons_gerant.html", context)

def livraison_list_client(request):
    customer = request.user  # take the logged-in user
    livraisons = Livraison.objects.filter(customer=customer).order_by('-date_sortie')

    context = {
        'livraisons': livraisons,
        'customer': customer,
    }
    return render(request, 'livraison_list_client.html', context)


from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Livraison

def creer_livraison_client(request):
    if request.method == 'POST':
        customer = request.POST.get('customer')
        commande = request.POST.get('commande')
        adresse = request.POST.get('adresse_livraison')

        # ⚠️ Tu peux ajouter des validations ici (champs vides, etc.)
        livraison = Livraison.objects.create(customer=customer, commande=commande, adresse_livraison=adresse,statut='EN_ATTENTE'  )

        # après création, on redirige le client vers le suivi de SES livraisons
        return redirect('suivi_livraisons_client', customer=customer)

    return render(request, 'livraison_form.html')


# UPDATE
def livraison_update(request, pk):
    livraison = get_object_or_404(Livraison, pk=pk)
    if request.method == "POST":
        form = LivraisonForm(request.POST, instance=livraison)
        if form.is_valid():
            livraison = form.save(commit=False)
            
            # Vérifier si statut Livrée mais pas de livreur
            if livraison.statut == "Livrée" and not livraison.id_livreur:
                form.add_error('id_livreur', "Vous devez affecter un livreur avant de marquer la livraison comme Livrée.")
                return render(request, "livraison_form.html", {"form": form, "title": "Modifier la livraison"})

            # si statut Livrée et date_arrivee vide, on remplit la date
            if livraison.statut == "Livrée" and not livraison.date_arrivee:
                from django.utils import timezone
                livraison.date_arrivee = timezone.now()

            livraison.save()

            # Mettre à jour le statut de la commande liée
            if livraison.commande:
                livraison.commande.statut = livraison.statut
                livraison.commande.save()

            return redirect("livraison_list")
    else:
        form = LivraisonForm(instance=livraison)

    return render(request, "livraison_form.html", {"form": form, "title": "Modifier la livraison"})


# DELETE
def livraison_delete(request, pk):
    livraison = get_object_or_404(Livraison, pk=pk)
    if request.method == "POST":
        livraison.delete()
        return redirect("livraison_list")
    return render(request, "livraison_confirm_delete.html", {"livraison": livraison})


# =========================
#       API REST (DRF)
# =========================

@api_view(['GET', 'POST'])
def livraison_list_create_api(request):
    # GET => liste toutes les livraisons
    if request.method == 'GET':
        livraisons = Livraison.objects.all().order_by('-date_sortie')
        serializer = LivraisonSerializer(livraisons, many=True)
        return Response(serializer.data)

    # POST => créer une nouvelle livraison
    elif request.method == 'POST':
        serializer = LivraisonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def livraison_detail_api(request, pk):
    # Récupérer l'objet ou 404
    try:
        livraison = Livraison.objects.get(pk=pk)
    except Livraison.DoesNotExist:
        return Response({'detail': 'Livraison introuvable'}, status=status.HTTP_404_NOT_FOUND)

    # GET => détails
    if request.method == 'GET':
        serializer = LivraisonSerializer(livraison)
        return Response(serializer.data)

    # PUT => mise à jour
    elif request.method == 'PUT':
        serializer = LivraisonSerializer(livraison, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE => suppression
    elif request.method == 'DELETE':
        livraison.delete()
        return Response({'detail': 'Livraison supprimée'}, status=status.HTTP_204_NO_CONTENT)



def home(request):
    return render(request, "index.html")
@require_POST
def livraison_update_row(request, pk):
    """Mise à jour d'une livraison (statut + id_livreur) depuis la ligne du tableau gérant."""
    livraison = get_object_or_404(Livraison, pk=pk)

    # Récupérer les valeurs envoyées par le formulaire de la ligne
    new_statut = request.POST.get("statut")
    new_id_livreur = request.POST.get("id_livreur")

    # Vérifier que le statut est valide
    statuts_valides = dict(Livraison.STATUT_LIVRAISON).keys()
    if new_statut in statuts_valides:
        livraison.statut = new_statut

    # Gérer l'affectation du livreur (id entier ou None)
    if new_id_livreur:
        try:
            livraison.id_livreur = int(new_id_livreur)
        except ValueError:
            pass  # si valeur invalide, on ignore
    else:
        livraison.id_livreur = None  # aucune affectation

    livraison.save()
    return redirect("livraison_list")


def livraison_detail(request, pk):
    livraison = get_object_or_404(Livraison, pk=pk)
    return render(request, "livraison_detail.html", {"livraison": livraison})
def livraison_annuler(request, pk):
    livraison = get_object_or_404(Livraison, pk=pk)
    livraison.statut = "annulee"
    livraison.save()
    return redirect("livraison_list")

from django.views.decorators.http import require_POST

def livreur_livraisons(request, livreur_id):
    # Récupère les livraisons affectées à ce livreur
    livraisons_affectees = Livraison.objects.filter(id_livreur=livreur_id)
    
    # Récupère les livraisons sans livreur (nouvelles)
    livraisons_non_affectees = Livraison.objects.filter(id_livreur__isnull=True)

    mes_en_cours = livraisons_affectees.filter(id_livreur=livreur_id).exclude(statut="Livrée")

    nouvelles = Livraison.objects.filter(id_livreur__isnull=True)

    # Combine les deux queryset
    livraisons = livraisons_affectees | livraisons_non_affectees

    precedentes = livraisons_affectees.filter(statut__in=["Livrée", "Annulée"]).order_by('-date_sortie')

    # Optionnel : trier par date_sortie descendante (nouveautés en premier)
    livraisons = livraisons.order_by('-date_sortie')

    # Statuts possibles pour le filtre
    livreur_statuts = [
        ("En cours de livraison", "En cours de livraison"),
        ('Livrée', 'Livrée'),
        ('Annulée', 'Annulée'),
    ]

    # Filtrage par statut si fourni via GET
    statut_filter = request.GET.get('statut')
    if statut_filter:
        livraisons = livraisons.filter(statut=statut_filter)

    context = {
        'livraisons': livraisons,
        "nouvelles": nouvelles,
        'livreur_id': livreur_id,
        'livreur_statuts': livreur_statuts,
        'statut_filter': statut_filter,
        'mes_en_cours': mes_en_cours,
        'precedentes': precedentes,
        'livraisons_non_affectees': livraisons_non_affectees,
    }

    return render(request, 'livreur_livraisons.html', context)

@require_POST
@require_POST
def livreur_update_statut_row(request, livreur_id, pk):
    """
    Le livreur met à jour le statut de SA livraison.
    Le statut de la commande liée est synchronisé.
    """

    livraison = get_object_or_404(
        Livraison,
        pk=pk,
        id_livreur=livreur_id
    )

    new_statut = request.POST.get("statut")

    # ✅ ON GARDE LES STATUTS DU MODÈLE
    statuts_autorises = {
        "En cours de livraison",
        "Livrée",
        "Annulée",
    }

    if new_statut in statuts_autorises:
        livraison.statut = new_statut

        # ✅ si livrée → date arrivée
        if new_statut == "Livrée" and livraison.date_arrivee is None:
            livraison.date_arrivee = timezone.now()

        livraison.save()

        # 🔥 synchronisation avec la commande
        if livraison.commande:
            livraison.commande.statut = new_statut
            livraison.commande.save()

    return redirect("livreur_livraisons", livreur_id=livreur_id)



def livreur_affecter_livraison(request, livreur_id, livraison_id):
    livraison = get_object_or_404(Livraison, pk=livraison_id)

    # Affecter le livreur
    livraison.id_livreur = livreur_id
    livraison.save()

    # Rediriger vers la liste des livraisons du livreur
    return redirect("livreur_livraisons", livreur_id=livreur_id)
