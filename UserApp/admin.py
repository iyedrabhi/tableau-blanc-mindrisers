from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Gerant, Client, Livreur


class UserAdmin(BaseUserAdmin):
    """Custom admin for User model - only show derived role types"""
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        ('Role', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )


class GerantAdmin(UserAdmin):
	"""Admin for Gérant - role set to 'gerant'"""
	list_display = ('username', 'first_name', 'last_name', 'email', 'restaurant_name', 'is_active', 'date_joined')
	fieldsets = (
		(None, {'fields': ('username', 'password')}),
		('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
		('Restaurant Info', {'fields': ('restaurant_name', 'restaurant_address', 'restaurant_phone', 'siret', 'business_license')}),
		('Permissions', {'fields': ('is_active', 'groups', 'user_permissions')}),
		('Important dates', {'fields': ('last_login', 'date_joined')}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'restaurant_name', 'restaurant_address', 'restaurant_phone', 'siret', 'business_license'),
		}),
	)

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		return qs.filter(role='gerant')

	def save_model(self, request, obj, form, change):
		obj.role = 'gerant'
		super().save_model(request, obj, form, change)
class ClientAdmin(UserAdmin):
	"""Admin for Client - includes client-specific fields"""
	list_display = ('username', 'first_name', 'last_name', 'email', 'is_subscribed', 'is_active', 'date_joined')
	fieldsets = (
		(None, {'fields': ('username', 'password')}),
		('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'date_of_birth')}),
		('Address', {'fields': ('living_location',)}),
		('Account', {'fields': ('is_subscribed',)}),
		('Permissions', {'fields': ('is_active', 'groups', 'user_permissions')}),
		('Important dates', {'fields': ('last_login', 'date_joined')}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'living_location', 'is_subscribed'),
		}),
	)

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		return qs.filter(role='client')

	def save_model(self, request, obj, form, change):
		obj.role = 'client'
		obj.is_staff = False
		obj.is_superuser = False
		super().save_model(request, obj, form, change)
class LivreurAdmin(UserAdmin):
	"""Admin for Livreur - includes delivery-specific fields"""
	list_display = ('username', 'first_name', 'last_name', 'email', 'vehicle_type', 'is_available', 'is_active', 'date_joined')
	fieldsets = (
		(None, {'fields': ('username', 'password')}),
		('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
		('Vehicle Info', {'fields': ('vehicle_number', 'vehicle_type', 'vehicle_registration', 'insurance_number')}),
		('Delivery Status', {'fields': ('is_available',)}),
		('Bank Info', {'fields': ('bank_account',)}),
		('Permissions', {'fields': ('is_active', 'groups', 'user_permissions')}),
		('Important dates', {'fields': ('last_login', 'date_joined')}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'vehicle_number', 'vehicle_type', 'vehicle_registration', 'insurance_number', 'is_available', 'bank_account'),
		}),
	)

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		return qs.filter(role='livreur')

	def save_model(self, request, obj, form, change):
		obj.role = 'livreur'
		obj.is_staff = False
		obj.is_superuser = False
		super().save_model(request, obj, form, change)
# Do NOT register User directly - only register the role-specific models
admin.site.register(Gerant, GerantAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Livreur, LivreurAdmin)
