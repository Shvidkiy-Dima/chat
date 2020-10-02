from rest_framework.serializers import SerializerMethodField


class RequestMethodField(SerializerMethodField):

    def to_representation(self, value):
        request = self.context.get('request', None)
        if not request:
            return None

        method = getattr(self.parent, self.method_name)
        return method(value, request)
