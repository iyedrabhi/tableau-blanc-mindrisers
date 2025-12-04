from django.core.management.base import BaseCommand
from django.conf import settings
from pathlib import Path
from UserApp.models import User


class Command(BaseCommand):
    help = "Seed demo users (gerant, clients, livreurs) and write credentials to users_seed.txt"

    def handle(self, *args, **options):
        from datetime import date
        
        # Define demo users with complete data
        demo_users = [
            # GERANTS
            {
                "username": "gerant1",
                "email": "gerant1@foodfunday.com",
                "role": "gerant",
                "password": "Gerant@123",
                "first_name": "Marcel",
                "last_name": "Dubois",
                "phone_number": "+33 1 42 56 78 90",
                "restaurant_name": "Food Funday Paris",
                "restaurant_address": "6 E Esplanade, St Albans VIC 3021, Australia",
                "restaurant_phone": "+61 3 9366 1234",
                "siret": "85234567891234",
                "business_license": "BL-2023-8923",
            },
            {
                "username": "gerant2",
                "email": "gerant2@foodfunday.com",
                "role": "gerant",
                "password": "Gerant@123",
                "first_name": "Isabelle",
                "last_name": "Lefevre",
                "phone_number": "+33 1 43 67 89 01",
                "restaurant_name": "Food Funday Lyon",
                "restaurant_address": "15 Place Bellecour, 69002 Lyon, France",
                "restaurant_phone": "+33 4 78 92 45 67",
                "siret": "89345678912345",
                "business_license": "BL-2023-9834",
            },
            {
                "username": "gerant3",
                "email": "gerant3@foodfunday.com",
                "role": "gerant",
                "password": "Gerant@123",
                "first_name": "Thomas",
                "last_name": "Moreau",
                "phone_number": "+33 1 44 78 90 12",
                "restaurant_name": "Food Funday Marseille",
                "restaurant_address": "8 Vieux Port, 13001 Marseille, France",
                "restaurant_phone": "+33 4 91 33 56 78",
                "siret": "92456789123456",
                "business_license": "BL-2023-7765",
            },
            {
                "username": "gerant4",
                "email": "gerant4@foodfunday.com",
                "role": "gerant",
                "password": "Gerant@123",
                "first_name": "Céline",
                "last_name": "Garnier",
                "phone_number": "+33 1 45 89 01 23",
                "restaurant_name": "Food Funday Toulouse",
                "restaurant_address": "22 Rue Alsace Lorraine, 31000 Toulouse, France",
                "restaurant_phone": "+33 5 61 23 45 67",
                "siret": "95567890234567",
                "business_license": "BL-2023-6654",
            },
            {
                "username": "gerant5",
                "email": "gerant5@foodfunday.com",
                "role": "gerant",
                "password": "Gerant@123",
                "first_name": "Alexandre",
                "last_name": "Rousseau",
                "phone_number": "+33 1 46 90 12 34",
                "restaurant_name": "Food Funday Nice",
                "restaurant_address": "10 Promenade des Anglais, 06000 Nice, France",
                "restaurant_phone": "+33 4 93 87 65 43",
                "siret": "98678901345678",
                "business_license": "BL-2023-5543",
            },
            
            # CLIENTS
            {
                "username": "client1",
                "email": "client1@email.com",
                "role": "client",
                "password": "Client@123",
                "first_name": "Jean",
                "last_name": "Dupont",
                "phone_number": "+33 6 12 34 56 78",
                "living_location": "45 Rue de la Paix, 75002 Paris, France",
                "is_subscribed": True,
                "date_of_birth": date(1985, 3, 15),
            },
            {
                "username": "client2",
                "email": "client2@email.com",
                "role": "client",
                "password": "Client@123",
                "first_name": "Sophie",
                "last_name": "Martin",
                "phone_number": "+33 6 23 45 67 89",
                "living_location": "12 Avenue des Champs-Élysées, 75008 Paris, France",
                "is_subscribed": True,
                "date_of_birth": date(1992, 7, 22),
            },
            {
                "username": "client3",
                "email": "client3@email.com",
                "role": "client",
                "password": "Client@123",
                "first_name": "Pierre",
                "last_name": "Bernard",
                "phone_number": "+33 6 34 56 78 90",
                "living_location": "78 Boulevard Saint-Germain, 75005 Paris, France",
                "is_subscribed": True,
                "date_of_birth": date(1988, 11, 8),
            },
            {
                "username": "client4",
                "email": "client4@email.com",
                "role": "client",
                "password": "Client@123",
                "first_name": "Marie",
                "last_name": "Leroy",
                "phone_number": "+33 6 45 67 89 01",
                "living_location": "23 Rue du Faubourg Saint-Honoré, 75008 Paris, France",
                "is_subscribed": True,
                "date_of_birth": date(1990, 5, 30),
            },
            {
                "username": "client5",
                "email": "client5@email.com",
                "role": "client",
                "password": "Client@123",
                "first_name": "Lucas",
                "last_name": "Durand",
                "phone_number": "+33 6 56 78 90 12",
                "living_location": "56 Rue de Rivoli, 75004 Paris, France",
                "is_subscribed": True,
                "date_of_birth": date(1995, 1, 12),
            },
            
            # LIVREURS
            {
                "username": "livreur1",
                "email": "livreur1@delivery.com",
                "role": "livreur",
                "password": "Livreur@123",
                "first_name": "Antoine",
                "last_name": "Moreau",
                "phone_number": "+33 6 67 89 01 23",
                "vehicle_number": "DL-2023-001",
                "vehicle_type": "scooter",
                "vehicle_registration": "AB-123-CD",
                "insurance_number": "INS-FR-9876543",
                "is_available": True,
                "bank_account": "FR7612345678901234567890123",
            },
            {
                "username": "livreur2",
                "email": "livreur2@delivery.com",
                "role": "livreur",
                "password": "Livreur@123",
                "first_name": "Camille",
                "last_name": "Roux",
                "phone_number": "+33 6 78 90 12 34",
                "vehicle_number": "DL-2023-002",
                "vehicle_type": "bike",
                "vehicle_registration": "EF-456-GH",
                "insurance_number": "INS-FR-8765432",
                "is_available": True,
                "bank_account": "FR7698765432109876543210987",
            },
            {
                "username": "livreur3",
                "email": "livreur3@delivery.com",
                "role": "livreur",
                "password": "Livreur@123",
                "first_name": "Nicolas",
                "last_name": "Petit",
                "phone_number": "+33 6 89 01 23 45",
                "vehicle_number": "DL-2023-003",
                "vehicle_type": "motorcycle",
                "vehicle_registration": "IJ-789-KL",
                "insurance_number": "INS-FR-7654321",
                "is_available": True,
                "bank_account": "FR7687654321098765432109876",
            },
            {
                "username": "livreur4",
                "email": "livreur4@delivery.com",
                "role": "livreur",
                "password": "Livreur@123",
                "first_name": "Emma",
                "last_name": "Girard",
                "phone_number": "+33 6 90 12 34 56",
                "vehicle_number": "DL-2023-004",
                "vehicle_type": "scooter",
                "vehicle_registration": "MN-012-OP",
                "insurance_number": "INS-FR-6543210",
                "is_available": True,
                "bank_account": "FR7676543210987654321098765",
            },
            {
                "username": "livreur5",
                "email": "livreur5@delivery.com",
                "role": "livreur",
                "password": "Livreur@123",
                "first_name": "Julien",
                "last_name": "Lambert",
                "phone_number": "+33 6 01 23 45 67",
                "vehicle_number": "DL-2023-005",
                "vehicle_type": "car",
                "vehicle_registration": "QR-345-ST",
                "insurance_number": "INS-FR-5432109",
                "is_available": True,
                "bank_account": "FR7665432109876543210987654",
            },
        ]

        created = 0
        updated = 0

        # Create or update users
        for u in demo_users:
            user, exists = User.objects.get_or_create(
                username=u["username"],
                defaults={
                    "email": u["email"],
                    "role": u["role"],
                }
            )
            
            # Update all fields
            if exists:
                created += 1
            else:
                updated += 1
            
            user.email = u["email"]
            user.role = u["role"]
            user.first_name = u.get("first_name", "")
            user.last_name = u.get("last_name", "")
            user.phone_number = u.get("phone_number", "")
            
            # Gerant fields
            if u["role"] == "gerant":
                user.restaurant_name = u.get("restaurant_name", "")
                user.restaurant_address = u.get("restaurant_address", "")
                user.restaurant_phone = u.get("restaurant_phone", "")
                user.siret = u.get("siret", "")
                user.business_license = u.get("business_license", "")
            
            # Client fields
            elif u["role"] == "client":
                user.living_location = u.get("living_location", "")
                user.is_subscribed = u.get("is_subscribed", False)
                user.date_of_birth = u.get("date_of_birth")
            
            # Livreur fields
            elif u["role"] == "livreur":
                user.vehicle_number = u.get("vehicle_number", "")
                user.vehicle_type = u.get("vehicle_type", "")
                user.vehicle_registration = u.get("vehicle_registration", "")
                user.insurance_number = u.get("insurance_number", "")
                user.is_available = u.get("is_available", True)
                user.bank_account = u.get("bank_account", "")

            user.set_password(u["password"])
            user.save()

        # Write credentials file at project root
        project_root = Path(settings.BASE_DIR)
        outfile = project_root / "users_seed.txt"
        lines = [
            "=" * 90,
            "FOOD FUNDAY - SEEDED DEMO USERS",
            "=" * 90,
            "",
            "GERANTS (Managers) - 5 instances:",
            "-" * 90,
        ]
        
        for u in demo_users:
            if u["role"] == "gerant":
                lines.append(f"Username: {u['username']} | Password: {u['password']}")
                lines.append(f"Email: {u['email']}")
                lines.append(f"Name: {u['first_name']} {u['last_name']} | Phone: {u['phone_number']}")
                lines.append(f"Restaurant: {u['restaurant_name']}")
                lines.append(f"Address: {u['restaurant_address']}")
                lines.append(f"Restaurant Phone: {u['restaurant_phone']}")
                lines.append(f"SIRET: {u['siret']} | License: {u['business_license']}")
                lines.append("")
        
        lines.append("-" * 90)
        lines.append("CLIENTS - 5 instances:")
        lines.append("-" * 90)
        
        for u in demo_users:
            if u["role"] == "client":
                lines.append(f"Username: {u['username']} | Password: {u['password']}")
                lines.append(f"Email: {u['email']}")
                lines.append(f"Name: {u['first_name']} {u['last_name']} | Phone: {u['phone_number']}")
                lines.append(f"Address: {u['living_location']}")
                lines.append(f"Date of Birth: {u['date_of_birth']} | Subscribed: {u['is_subscribed']}")
                lines.append("")
        
        lines.append("-" * 90)
        lines.append("LIVREURS (Delivery Personnel) - 5 instances:")
        lines.append("-" * 90)
        
        for u in demo_users:
            if u["role"] == "livreur":
                lines.append(f"Username: {u['username']} | Password: {u['password']}")
                lines.append(f"Email: {u['email']}")
                lines.append(f"Name: {u['first_name']} {u['last_name']} | Phone: {u['phone_number']}")
                lines.append(f"Vehicle: {u['vehicle_type'].title()} ({u['vehicle_number']}) | Registration: {u['vehicle_registration']}")
                lines.append(f"Insurance: {u['insurance_number']}")
                lines.append(f"Bank Account: {u['bank_account']} | Available: {u['is_available']}")
                lines.append("")
        
        lines.append("=" * 90)
        lines.append(f"TOTAL: {len(demo_users)} users (5 gerants, 5 clients, 5 livreurs)")
        lines.append("=" * 90)

        outfile.write_text("\n".join(lines), encoding="utf-8")

        self.stdout.write(self.style.SUCCESS(
            f"Seeding complete: created={created}, updated={updated}. Credentials written to {outfile}"
        ))