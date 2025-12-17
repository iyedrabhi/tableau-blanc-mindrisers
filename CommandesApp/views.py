from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Commande
from .forms import CommandeForm
from LivraisonApp.models import Livraison  # import lazy



class CommandeCreate(LoginRequiredMixin, CreateView):
    model = Commande
    form_class = CommandeForm
    template_name = "commandes/commandes_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plates_dict'] = {str(plate.id): plate for plate in self.get_form().fields['plates'].queryset}
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.customer = self.request.user

        # Set the delivery address from the form (if livraison)
        if form.cleaned_data.get('type_commande') == "livraison":
            self.object.adresse_livraison = form.cleaned_data.get('adresse_livraison')

        self.object.save()
        form.save_m2m()

        if self.object.type_commande == "livraison":
            Livraison.objects.get_or_create(
                commande=self.object,
                defaults={
                    "customer": self.object.customer,
                    "statut": "en_attente",
                    "adresse_livraison": self.object.adresse_livraison,  # ✅ use real address
                }
            )
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("commande_detail", kwargs={"pk": self.object.pk})


class CommandeListView(LoginRequiredMixin, ListView):
    model = Commande
    template_name = "commandes/commande_list.html"
    context_object_name = "commandes"
    ordering = ['-created_at']  # Remplace 'created_at' par le champ date de création de ta commande



class CommandeDetailView(LoginRequiredMixin, DetailView):
    model = Commande
    template_name = "commandes/commande_detail.html"
    context_object_name = "commande"


class CommandeUpdateView(LoginRequiredMixin, UpdateView):
    model = Commande
    form_class = CommandeForm
    template_name = "commandes/commande_update.html"
    def form_valid(self, form):
        response = super().form_valid(form)
        # 🔥 Update related Livraison addresses
        if self.object.type_commande == "livraison":
            Livraison.objects.filter(commande=self.object).update(adresse_livraison=self.object.adresse_livraison)
        return response
    def get_success_url(self):
        return reverse_lazy("commande_detail", kwargs={"pk": self.object.pk})


class CommandeDeleteView(LoginRequiredMixin, DeleteView):
    model = Commande
    template_name = "commandes/commande_confirm_delete.html"
    success_url = reverse_lazy("commande_list")


class CommandeDetailAdminView(LoginRequiredMixin, DetailView):
    model = Commande
    template_name = "commandes/commande_detail_admin.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.status = request.POST.get("status")
        self.object.save()
        return redirect("commande_detail_admin", pk=self.object.pk)
