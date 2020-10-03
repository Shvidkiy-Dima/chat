from django_filters.rest_framework.backends import DjangoFilterBackend


class FilterBackend(DjangoFilterBackend):

    def get_filterset_kwargs(self, request, queryset, view):
        # Add filter arguments from url patterns

        kwargs = super().get_filterset_kwargs(request, queryset, view)
        kwargs['data'] = kwargs['data'].dict()
        kwargs['data'].update(view.kwargs)
        return kwargs
