""" Django admin customization. """
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from core.models import Autor, Categoria, Editora, Livro, User, Compra

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'name', 'is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name', 'foto')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            },
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
        (_('Groups'), {'fields': ('groups',)}),
        (_('User Permissions'), {'fields': ('user_permissions',)}),
    )
    readonly_fields = ['last_login']
    # Mantendo o add_fieldsets padrão do BaseUserAdmin para evitar erros de fields com 'password1'
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'name', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email')
    search_fields = ('nome', 'email')
    list_filter = ('nome',)
    ordering = ('nome', 'email')
    list_per_page = 10

class ItensCompraInline(admin.TabularInline):
    model = ItensCompra
    extra = 1 

@admin.register(Compra)
class CompraAdmin(ModelAdmin):
    list_display = ('usuario', 'status')
    search_fields = ('usuario', 'status')
    list_filter = ('usuario', 'status')
    ordering = ('usuario', 'status')
    list_per_page = 10
    inlines = [ItensCompraInline]

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('descricao',)
    search_fields = ('descricao',)
    list_filter = ('descricao',)
    ordering = ('descricao',)
    list_per_page = 10

@admin.register(Editora)
class EditoraAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'cidade')
    search_fields = ('nome', 'email', 'cidade')
    list_filter = ('nome', 'email', 'cidade')
    ordering = ('nome', 'email', 'cidade')
    list_per_page = 10

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'editora', 'categoria')
    search_fields = ('titulo', 'editora__nome', 'categoria__descricao')
    list_filter = ('editora', 'categoria')
    ordering = ('titulo', 'editora', 'categoria')
    list_per_page = 25
