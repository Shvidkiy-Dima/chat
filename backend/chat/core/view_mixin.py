class ChangeSerializerMixin:
    serializers = dict()

    def get_serializer_class(self):
        serializer_cls = self.serializers.get(self.action)
        return serializer_cls if serializer_cls is not None else self.serializers['default']