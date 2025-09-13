"""
Django admin customization.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core.models import Categoria, Produto, Pedido,Orcamento,Tamanho, PrecoQuantidade, Endereco, Avaliacao, ItensPedido, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name', 'passage_id', 'endereco', 'foto')}),
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
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'name',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                ),
            },
        ),
    )

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome', 'descricao')
    list_filter = ('nome', 'descricao',)
    ordering = ('nome', 'descricao')
    list_per_page = 10
    
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'listar_categorias', 'tipo')
    search_fields = ('nome', 'categoria__nome')
    list_filter = ('categoria',)
    ordering = ('nome',)
    list_per_page = 10

    def listar_categorias(self, obj):
        return ", ".join([c.nome for c in obj.categoria.all()])
    listar_categorias.short_description = "Categorias"
    
@admin.register(Tamanho)
class TamanhoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'qtdFatia', 'massakg')
    search_fields = ('nome', 'qtdFatia', 'massakg')
    list_filter = ('nome', 'qtdFatia', 'massakg')
    ordering =  ('nome', 'qtdFatia', 'massakg')
    list_per_page = 10
    
@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'produto', 'nota', 'data')
    search_fields = ('usuario', 'produto', 'nota', 'data')
    list_filter = ('usuario', 'produto', 'nota', 'data')
    ordering =  ('usuario', 'produto', 'nota', 'data')
    list_per_page = 10
    
@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('logradouro', 'bairro', 'numero', 'cidade', 'estado')
    search_fields = ('logradouro', 'bairro', 'numero', 'cidade', 'estado')
    list_filter = ('logradouro', 'bairro', 'numero', 'cidade', 'estado')
    ordering =  ('logradouro', 'bairro', 'numero', 'cidade', 'estado')
    list_per_page = 10
    
@admin.register(PrecoQuantidade)
class PrecoQuantidadeAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'quantidade', 'preco')
    search_fields = ('categoria', 'quantidade', 'preco')
    list_filter = ('categoria', 'quantidade', 'preco')
    ordering =  ('categoria', 'quantidade', 'preco')
    list_per_page = 10
    
@admin.register(Orcamento)
class OrcamentoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'data')
    search_fields = ('usuario', 'data')
    list_filter = ('usuario', 'data')
    ordering = ('usuario', 'data')
    list_per_page = 10
    
    
class ItensPedidoInline(admin.TabularInline):
    model = ItensPedido
    extra = 1 
    
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'status', 'data', 'horario_entrega', 'formaDeRetirada','total_formatado')
    search_fields = ('usuario', 'status', 'data', 'horario_entrega', 'formaDeRetirada')
    list_filter = ('usuario', 'status', 'data', 'horario_entrega', 'formaDeRetirada')
    ordering = ('usuario', 'status', 'data', 'horario_entrega', 'formaDeRetirada')
    list_per_page = 10
    inlines = [ItensPedidoInline]
    readonly_fields = ("total_formatado",)
    
    @admin.display(description="Total")
    def total_formatado(self, obj):
        """Exibe R$ 123,45 em vez de 123.45."""
        return f"R$ {obj.total:.2f}"
    

# admin.site.register(models.User, UserAdmin)
# admin.site.register(models.Categoria)
# admin.site.register(models.Produto)
# admin.site.register(models.Orcamento)
# admin.site.register(models.Tamanho)
# admin.site.register(models.PrecoQuantidade)
# admin.site.register(models.Endereco)
# admin.site.register(models.Avaliacao)
# admin.site.register(models.Pedido)