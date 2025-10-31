from django_filters import rest_framework as filters
from uploader.models import Image
from django.db.models import Q

class ImageFilter(filters.FilterSet):
    # filtro customizado para Bolo, Torta ou Banoffi
    descricao = filters.CharFilter(field_name="description", method="filter_descricao")

  
    def filter_descricao(self, queryset, name, value):
        return queryset.filter(
            Q(description__istartswith="bolo") |
            Q(description__istartswith="torta") |
            Q(description__istartswith="brigadeiro")
    )

    class Meta:
        model = Image
        fields = ["description"]