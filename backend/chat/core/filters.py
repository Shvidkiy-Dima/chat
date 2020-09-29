from django_filters import NumberFilter
from django_filters.rest_framework import FilterSet
from .models import Message


class MessageFilter(FilterSet):
    dialog = NumberFilter(field_name='dialog', lookup_expr='exact')

    class Meta:
        model = Message
        fields = ['dialog']
