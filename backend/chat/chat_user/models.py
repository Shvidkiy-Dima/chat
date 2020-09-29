from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db.models import Count, ImageField
from .utils import make_thumbnail


class ChatUser(AbstractUser):
    image = ImageField(upload_to='user_image/', default='default.jpeg')

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        instance._image_value = values[field_names.index('image')]
        return instance


    def save(self, *args, **kwargs):
        if not self._state.adding and self._image_value != self.image:
            thumbnail = make_thumbnail(self.image)
            self.image.save(self.image.name, thumbnail, save=False)

        return super().save(*args, **kwargs)



    def get_my_dialogs(self):
        dialogs = self.dialogs.all()
        return dialogs.annotate(count_msgs=Count('messages')).filter(count_msgs__gte=1).distinct()

    def __str__(self):
        return f'user_{self.id}'


class _UserModel:

    def __getattribute__(self, item):
        user_model = get_user_model()
        return getattr(user_model, item)

UserModel = _UserModel()
