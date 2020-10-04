from django_filters import CharFilter
from django_filters.rest_framework import FilterSet
from .models import ChatUser


class UsersFilter(FilterSet):
    username = CharFilter(field_name='username', method='filter_users')

    def filter_users(self, queryset, name, value):
        return queryset.filter(username__icontains=value).exclude(id=self.request.user.id)

    class Meta:
        model = ChatUser
        fields = ['username']
