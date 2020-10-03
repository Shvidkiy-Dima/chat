from django_filters import CharFilter
from django_filters.rest_framework import FilterSet
from .models import ChatUser


class UsersFilter(FilterSet):
    username = CharFilter(field_name='username', lookup_expr='icontains')

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        return qs.exclude(id=self.request.user.id) if self.request.user.is_authenticated else qs

    class Meta:
        model = ChatUser
        fields = ['username']
