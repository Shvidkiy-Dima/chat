from django_filters import CharFilter
from django_filters.rest_framework import FilterSet
from .models import ChatUser


class UsersFilter(FilterSet):
    username = CharFilter(field_name='username', lookup_expr='icontains')

    class Meta:
        model = ChatUser
        fields = ['username']
