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
    livraisons = None
    id_client = None

    if request.method == 'POST':
        form = ClientLivraisonSearchForm(request.POST)
        if form.is_valid():
            id_client = form.cleaned_data['id_client']
            livraisons = Livraison.objects.filter(id_client=id_client).order_by('-date_creation')
    else:
        form = ClientLivraisonSearchForm()

    context = {
        'form': form,
        'livraisons': livraisons,
        'id_client': id_client,
    }
    return render(request, 'livraison_list_client.html', context)

# CREATE
def livraison_create(request):
    if request.method == "POST":
        form = LivraisonForm(request.POST)
        if form.is_valid():
            livraison = form.save(commit=False)
            # ici tu peux encore modifier livraison si besoin
            livraison.save()

            # 🔴 Redirection vers la page de suivi du client concerné
            return redirect(
                "suivi_livraisons_client",
                client_id=livraison.id_client
            )
    else:
        form = LivraisonForm()

    return render(request, "livraison_form.html", {"form": form})


from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Livraison

def creer_livraison_client(request):
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        commande_id = request.POST.get('commande_id')
        adresse = request.POST.get('adresse_livraison')

        # ⚠️ Tu peux ajouter des validations ici (champs vides, etc.)
        livraison = Livraison.objects.create(
            client_id=client_id,
            commande_id=commande_id,
            adresse_livraison=adresse,
            statut='EN_ATTENTE'
        )

        # après création, on redirige le client vers le suivi de SES livraisons
        return redirect('suivi_livraisons_client', client_id=client_id)

    return render(request, 'livraison_form.html')
def suivi_livraisons_client(request, client_id):
    """
    Affiche uniquement les livraisons du client dont l'ID est passé dans l'URL.
    Ex : /livraisons/client/1/
    """
    livraisons = Livraison.objects.filter(id_client=client_id).order_by("-date_sortie")

    context = {
        "client_id": client_id,
        "livraisons": livraisons,
    }
    # ⚠️ adapte le chemin au VRAI emplacement du template
    return render(request, "suivi_livraisons_client.html", context)


# UPDATE
def livraison_update(request, pk):
    livraison = get_object_or_404(Livraison, pk=pk)
    if request.method == "POST":
        form = LivraisonForm(request.POST, instance=livraison)
        if form.is_valid():
            form.save()
            return redirect("livraison_list")
    else:
        form = LivraisonForm(instance=livraison)
    return render(request, "livraisons/livraison_form.html", {"form": form, "title": "Modifier la livraison"})

# DELETE
def livraison_delete(request, pk):
    livraison = get_object_or_404(Livraison, pk=pk)
    if request.method == "POST":
        livraison.delete()
        return redirect("livraison_list")
    return render(request, "livraisons/livraison_confirm_delete.html", {"livraison": livraison})


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
def livraison_create_gerant(request):
    if request.method == "POST":
        form = LivraisonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("livraison_list")
    else:
        form = LivraisonForm()

    return render(request, "livraison_form_gerant.html", {"form": form})
from django.views.decorators.http import require_POST

def livreur_livraisons(request, livreur_id):
    # Récupérer le filtre statut depuis l'URL (?statut=...)
    statut_filter = request.GET.get("statut", "").strip()

    # Base : livraisons de CE livreur
    livraisons = Livraison.objects.filter(id_livreur=livreur_id)

    # Si un statut est choisi → on filtre
    if statut_filter:
        livraisons = livraisons.filter(statut=statut_filter)

    livraisons = livraisons.order_by("-date_sortie")

    # Statuts disponibles pour la liste déroulante du livreur (pour filtre + changement de statut)
    livreur_statuts = [
        ('en_cours', 'En cours'),
        ('livree', 'Livrée'),
        ('retour', 'Retour'),
        ('annulee', 'Annulée'),
    ]

    context = {
        "livraisons": livraisons,
        "livreur_id": livreur_id,
        "livreur_statuts": livreur_statuts,
        "statut_filter": statut_filter,  # 🔴 pour garder la sélection dans le template
    }
    return render(request, "livraisons_livreur.html", context)


@require_POST
def livreur_update_statut_row(request, livreur_id, pk):
    """
    Le livreur met à jour le statut d'une de ses livraisons.
    Il ne peut PAS changer le livreur, seulement le statut.
    """
    livraison = get_object_or_404(Livraison, pk=pk, id_livreur=livreur_id)

    new_statut = request.POST.get("statut")

    # Statuts autorisés pour le livreur (tu peux ajuster la liste)
    statuts_autorises = {"en_cours", "prete", "en_attente", "livree", "annulee"}

    if new_statut in statuts_autorises:
        livraison.statut = new_statut
        livraison.save()

    return redirect("livreur_livraisons", livreur_id=livreur_id)
@require_POST
def livreur_update_statut_row(request, livreur_id, pk):
    """
    Le livreur met à jour le statut d'une de ses livraisons.
    Si le statut passe à 'livree', on remplit date_arrivee automatiquement.
    """
    livraison = get_object_or_404(Livraison, pk=pk, id_livreur=livreur_id)

    new_statut = request.POST.get("statut")

    # Statuts que le livreur a le droit de mettre
    statuts_autorises = {"en_cours", "livree", "annulee", "retour"}

    if new_statut in statuts_autorises:
        livraison.statut = new_statut

        # ✅ si livrée → on met la date d'arrivée si pas encore définie
        if new_statut == "livree" and livraison.date_arrivee is None:
            livraison.date_arrivee = timezone.now()

        # (optionnel) si on enlève "livrée", on peut décider de ne pas toucher à date_arrivee
        # elif new_statut != "livree":
        #     livraison.date_arrivee = None

        livraison.save()

    return redirect("livreur_livraisons", livreur_id=livreur_id)
