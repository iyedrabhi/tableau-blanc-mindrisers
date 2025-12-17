# 📋 Guide de Test - Système de Rappels Intelligents

## 🎯 Vue d'ensemble

Le système de rappels intelligent envoie automatiquement des notifications aux clients:

- **Avant 12h00**: Rappel **2h avant** la réservation
- **À partir de 12h00**: Rappel **4h avant** la réservation

---

## 🚀 Comment Tester les Rappels

### **Option 1: Test Rapide (Rappels Immédiats) - RECOMMANDÉ**

#### Étape 1: Créer une réservation de test

1. Connecte-toi comme **client** (`test_client` / `Test@123`)
2. Va à `http://127.0.0.1:8000/reservations/available/`
3. Clique sur **"Réserver"** sur une table
4. Choisis:
   - **Date**: Aujourd'hui (2025-12-05)
   - **Heure**: 14:00 (après 12h00 → 4h de rappel)
   - **Durée**: 90 minutes
5. Clique **"Créer la réservation"**

#### Étape 2: Déclencher le rappel manuellement

Ouvre un **terminal** dans le dossier `restaurant_project/` et exécute:

```bash
python manage.py test_reminders
```

**Résultat attendu:**

- La commande crée une réservation de test pour **aujourd'hui à 14:00**
- Elle déclenche immédiatement le rappel
- Tu dois voir une **notification Toastr** appear dans le coin en haut à droite
- La notification dit: "⏰ Rappel de votre réservation..."

#### Étape 3: Vérifier le rappel sur la page

1. Connecte-toi comme **client**
2. Va à `http://127.0.0.1:8000/reservations/reminders/`
3. Tu dois voir:
   - Le titre: "⏰ Mes Rappels de Réservations"
   - Une box verte expliquant: "Réservation à partir de 12h00 → Rappel 4h avant"
   - La notification de rappel listée avec:
     - Badge: ⏰ RAPPEL
     - Message: "Rappel de votre réservation pour la Table X le [date] à [heure]"
     - Date/heure du rappel

---

### **Option 2: Test Complet (Attendre le délai réel)**

#### Pour tester une réservation à 09:00 (Rappel 2h avant)

1. Crée une réservation pour **demain à 09:00**
2. Le rappel se déclenche **automatiquement à 07:00 demain**
3. Attends que Celery beat envoie le rappel

#### Pour tester une réservation à 15:00 (Rappel 4h avant)

1. Crée une réservation pour **demain à 15:00**
2. Le rappel se déclenche **automatiquement à 11:00 demain**

---

## 📱 Interface de Test

### **Page des Rappels Client** (`/reservations/reminders/`)

Affiche:

- 📊 Total des notifications
- 💡 Box d'explication du système intelligent (2h/4h)
- 📋 Liste des rappels avec badges par type
- 🗑️ Bouton "Effacer tout"

### **Page des Notifications Gérant** (`/reservations/gerant/notifications/`)

Affiche:

- 3 onglets: **📋 Tous | ✅ Confirmations | ❌ Annulations**
- Quand un **client crée une réservation** → notification CONFIRMATION
- Quand un **client annule une réservation** → notification ANNULATION
- Compteurs de chaque type

---

## 🔧 Commandes Utiles

### **Créer les utilisateurs de test**

```bash
python manage.py setup_test_users
```

Crée:

- `test_client` / `Test@123` (client normal)
- `test_gerant` / `Gerant@123` (manager)

### **Déclencher les rappels immédiatement**

```bash
python manage.py test_reminders
```

### **Voir les tâches Celery planifiées**

```bash
# Vérifier que Celery beat est en train de tourner
python manage.py celery -A restaurant_project worker -B
```

---

## ✅ Checklist de Validation

### Client - Page Rappels (`/reservations/reminders/`)

- [ ] Page charge sans erreur
- [ ] Titre "⏰ Mes Rappels de Réservations" visible
- [ ] Box d'explication avec règles 2h/4h visible
- [ ] Rappels listés avec badges (⏰)
- [ ] Badge affiche le type de notification
- [ ] Date/heure du rappel affichée correctement
- [ ] Bouton "Effacer tout" fonctionne

### Gérant - Page Notifications (`/reservations/gerant/notifications/`)

- [ ] Page charge sans erreur
- [ ] 3 onglets visibles: Tous | Confirmations | Annulations
- [ ] Compteurs corrects pour chaque type
- [ ] Cliquer sur les onglets filtre correctement
- [ ] Notifications affichent correctement par type
- [ ] Badges de couleur: vert (confirmation) / rouge (annulation)
- [ ] Formulaire "Effacer tout" fonctionne

### Système Global

- [ ] Polling JavaScript fonctionne (5s d'intervalle)
- [ ] Toasts Toastr s'affichent quand rappel arrive
- [ ] Pas d'erreur 404 ou 500
- [ ] URLs correctes pour client et gérant

---

## 🌐 URLs de Test

**ESPACE CLIENT:**

```
http://127.0.0.1:8000/reservations/reminders/          ← Rappels
http://127.0.0.1:8000/reservations/my/                 ← Mes réservations
http://127.0.0.1:8000/reservations/available/          ← Réserver
```

**ESPACE GÉRANT:**

```
http://127.0.0.1:8000/reservations/gerant/             ← Tables
http://127.0.0.1:8000/reservations/all/                ← Toutes réservations
http://127.0.0.1:8000/reservations/gerant/history/     ← Historique
http://127.0.0.1:8000/reservations/gerant/notifications/ ← Notifications (avec filtres)
```

---

## 🐛 Dépannage

### Je ne vois pas la notification

1. ✅ Vérifie que le serveur Django tourne (`python manage.py runserver`)
2. ✅ Vérifie que Celery beat tourne (pour les rappels programmés)
3. ✅ Utilise `python manage.py test_reminders` pour test immédiat
4. ✅ Hard-reload (Ctrl+F5) le navigateur

### L'onglet "Confirmations" ne montre rien

1. ✅ Crée une nouvelle réservation comme client
2. ✅ Le gérant doit voir une notification CONFIRMATION
3. ✅ Vérifie que `notification_type='CONFIRMATION'` dans la BD

### Erreur "TemplateDoesNotExist"

1. ✅ Hard-reload (Ctrl+F5)
2. ✅ Redémarre le serveur Django
3. ✅ Vérifie les chemins des templates

---

## 📊 Timeline d'Exemple

**Résultats attendus après `python manage.py test_reminders`:**

```
14:00 (maintenant) ← Réservation créée
       ↓
14:00 ← Rappel déclenché immédiatement (par la commande)
       ↓
✅ Notification affichée dans la page `/reservations/reminders/`
✅ Toast Toastr en haut à droite
✅ Notification visible 5 secondes après (polling)
```

---

## 📞 Support

Si tu as des problèmes:

1. Vérifie les logs Django: `python manage.py runserver` affiche les erreurs
2. Vérifie les logs Celery: `python manage.py celery -A restaurant_project worker -B`
3. Vérifiez la base de données: `python manage.py shell` puis `Notification.objects.all()`
