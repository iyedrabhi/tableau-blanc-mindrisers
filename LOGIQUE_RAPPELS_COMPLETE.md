# 📚 Logique Complète des Rappels et Notifications

## 🎯 Vue d'ensemble

Le système fonctionne en **deux niveaux**:

1. **Client**: Voit ses rappels intelligents + confirmations + annulations
2. **Gérant**: Voit les événements des clients (confirmations + annulations)

---

## 📋 Flux Complet d'une Réservation

### **Étape 1: Client Crée une Réservation**

**Action**: Client accède à `/reservations/available/` et clique "Réserver"

**Backend (`create_reservation()`):**

```
1. Valide le formulaire (date, heure, table)
2. Crée Reservation object:
   - status = 'reserved'
   - date, start_time, end_time, table, client
3. Calcule reminder_datetime (signal déclenché):
   - Si start_time.hour < 12 → rappel 2h avant
   - Si start_time.hour >= 12 → rappel 4h avant
4. Sauvegarde: reservation.reminder_datetime = datetime calculé
5. Signal `post_save` déclenche:
   a) Notifie TOUS les gérants: notification_type='CONFIRMATION'
   b) Crée un message: "✅ Table X réservée le [date] à [heure]"
```

**Résultat**:

- ✅ Réservation créée avec statut='reserved'
- ✅ Rappel planifié pour plus tard
- ✅ Gérant reçoit notification CONFIRMATION

---

### **Étape 2: Rappel Envoyé au Client**

**Quand**: À l'heure calculée (2h ou 4h avant start_time)

**Comment**:

- Manuellement: `python manage.py test_reminders_scheduled --wait 5`
- Automatiquement: Celery beat schedule (si configuré)

**Backend (`send_reminder()` task):**

```
1. Cherche la réservation
2. Crée Notification pour le client:
   - notification_type = 'RAPPEL'
   - message = "Rappel de votre réservation à Table X"
   - Mark reminder_sent = True
3. Client voit toast Toastr (polling JS détecte nouvelle notif)
4. Notif s'ajoute à la page `/reservations/reminders/`
```

**Résultat**:

- ✅ Client reçoit rappel 2h/4h avant
- ✅ Toast notification apparaît en haut à droite
- ✅ Notification visible dans `/reservations/reminders/?status=reminders`

---

### **Étape 3: Client Annule la Réservation** (Optionnel)

**Action**: Client accède à `/reservations/my_reservations/` et clique "Annuler"

**Validations**:

- ✅ L'utilisateur est le propriétaire de la réservation
- ✅ L'heure de réservation n'a pas commencé (date < aujourd'hui ou heure > maintenant)

**Backend (`cancel_reservation()`):**

```
1. Crée notification pour CLIENT:
   - notification_type = 'cancel'
   - Message: "Votre réservation a été annulée"
2. Crée notification pour TOUS les gérants:
   - notification_type = 'ANNULATION'
   - Message: "❌ Annulation: Table X le [date] à [heure]"
3. Change reservation.status = 'cancelled'
4. Revoke toute tâche Celery associée
```

**Résultat**:

- ✅ Réservation marquée comme 'cancelled'
- ✅ Client voit annulation dans `/reservations/reminders/?status=cancellations`
- ✅ Gérant voit annulation dans `/reservations/gerant/notifications/?filter=annulations`

---

## 🔔 Où Voir Quoi?

### **PAGE CLIENT: `/reservations/reminders/`**

**Onglets disponibles:**

```
📋 Tous (total)
├─ ✅ Confirmations (quand créé)
├─ 🔔 Rappels (2h/4h avant)
└─ ❌ Annulations (si client annule)
```

**Types de notifications visibles:**
| Type | Quand | Emoji | Couleur |
|------|-------|-------|--------|
| CONFIRMATION | Client crée réservation | ✅ | Vert |
| RAPPEL | 2h/4h avant reservation | 🔔 | Orange |
| ANNULATION | Client annule | ❌ | Rouge |

**Exemple:**

```
⏰ Mes Rappels de Réservations

✅ CONFIRMATION
Réservation confirmée - Table 5
Votre réservation pour la table 5 le 2025-12-05 à 14:00 est confirmée.
05/12/2025 09:45

🔔 RAPPEL
Rappel de votre réservation
Rappel pour votre réservation à la Table 5 le 05/12/2025 à 14:00
05/12/2025 10:00

❌ ANNULATION
Réservation annulée
Votre réservation pour la table 5 le 2025-12-05 à 14:00 a été annulée.
05/12/2025 10:15
```

---

### **PAGE GÉRANT: `/reservations/gerant/notifications/`**

**Onglets disponibles:**

```
📋 Tous (total)
├─ ✅ Confirmations (quand client crée)
└─ ❌ Annulations (quand client annule)
```

**Types de notifications visibles:**
| Type | Quand | Emoji | Couleur |
|------|-------|-------|--------|
| CONFIRMATION | Client crée réservation | ✅ | Vert |
| ANNULATION | Client annule | ❌ | Rouge |

**Exemple:**

```
🔔 Notifications - Événements des Clients

✅ CONFIRMATIONS (2)
✅ Table 5 réservée le 2025-12-05 à 14:00
La table 5 a été réservée pour test_client le 2025-12-05 à 14:00.
05/12/2025 09:45

❌ ANNULATIONS (1)
❌ Annulation: Table 3 le 2025-12-05 à 12:00
La réservation de la table 3 du 2025-12-05 à 12:00 a été annulée par test_client.
05/12/2025 10:30
```

---

## 🧠 Logique des Rappels Intelligents

### **Règle de Calcul**

```python
reservation_time = 14:00  # Heure de la réservation

if reservation_time.hour < 12:
    # Matin (9h, 10h, 11h...)
    reminder_time = reservation_time - 2h
    # Exemple: 10:00 → rappel à 08:00
else:
    # Après-midi/Soirée (12h, 13h, 14h...)
    reminder_time = reservation_time - 4h
    # Exemple: 14:00 → rappel à 10:00
    # Exemple: 20:00 → rappel à 16:00
```

### **Pourquoi 2h vs 4h?**

| Catégorie         | Heure | Rappel Avant | Raison                         |
| ----------------- | ----- | ------------ | ------------------------------ |
| 🌅 Petit-déjeuner | 09:00 | 2h (07:00)   | Court préavis                  |
| 🥘 Déjeuner       | 12:00 | 4h (08:00)   | Plus de temps pour préparation |
| 🍽️ Dîner          | 20:00 | 4h (16:00)   | Plus de temps pour préparation |

**Logique métier**: Les réservations l'après-midi/soir nécessitent plus de préparation (cuisiner, mettre la table, etc.)

---

## 📊 Exemples Réels

### **Scénario 1: Réservation Midi (12:00)**

```
09:00 - Client crée réservation 12:00
        → Gérant reçoit CONFIRMATION
        → Rappel planifié pour 08:00 (4h avant)

08:00 - Rappel déclenché
        → Client reçoit notification RAPPEL
        → Notification s'ajoute à /reminders/?status=reminders

12:00 - Client arrive au restaurant ✅
```

### **Scénario 2: Réservation Matin (09:00)**

```
07:30 - Client crée réservation 09:00
        → Gérant reçoit CONFIRMATION
        → Rappel planifié pour 07:00 (2h avant)

07:00 - Rappel déclenché
        → Client reçoit notification RAPPEL
        → Notification s'ajoute à /reminders/?status=reminders

09:00 - Client arrive au restaurant ✅
```

### **Scénario 3: Client Annule**

```
09:00 - Client crée réservation 14:00
        → Gérant voit: ✅ CONFIRMATION
        → Rappel planifié pour 10:00

10:30 - Client annule
        → Gérant voit: ❌ ANNULATION
        → Client voit: ❌ ANNULATION (dans /reminders/?status=cancellations)
        → Rappel annulé (si pas encore envoyé)
```

---

## 🔄 Types de Notifications

### **Pour CLIENT** (`notification_type`)

- `CONFIRMATION`: Réservation créée
- `RAPPEL`: 2h/4h avant réservation
- `ANNULATION` ou `cancel`: Réservation annulée
- `client`: Notifications générales client

### **Pour GÉRANT** (`notification_type`)

- `CONFIRMATION`: Quand client crée réservation
- `ANNULATION`: Quand client annule réservation

---

## 🧪 Comment Tester

### **Test 1: Créer et Envoyer Rappel Immédiatement**

```bash
python manage.py test_reminders
```

✅ Crée réservation 14:00
✅ Envoie rappel IMMÉDIATEMENT
✅ Va voir à `/reservations/reminders/`

### **Test 2: Créer Rappel qui Attend**

```bash
python manage.py test_reminders_scheduled --wait 5
```

✅ Crée réservation 14:00
✅ Attend 5 secondes
✅ Envoie rappel
✅ Simule l'attente réelle

### **Test 3: Vérifier les Filtres Gérant**

```
1. Connecte-toi comme test_gerant
2. Va à /reservations/gerant/notifications/
3. Clique sur onglet "✅ Confirmations"
4. Clique sur onglet "❌ Annulations"
5. Les notifications doivent filtrer correctement
```

---

## ✅ Résumé

| Action           | Client Voit     | Gérant Voit     | notification_type |
| ---------------- | --------------- | --------------- | ----------------- |
| Crée réservation | ✅ CONFIRMATION | ✅ CONFIRMATION | CONFIRMATION      |
| Reçoit rappel    | 🔔 RAPPEL       | —               | RAPPEL            |
| Annule           | ❌ ANNULATION   | ❌ ANNULATION   | ANNULATION        |

**Important**:

- Les notifications sont **filtrables par onglets**
- Les rappels sont **intelligents** (2h vs 4h)
- Le système fonctionne **sans Celery** (test_reminders_scheduled)
