from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db.models import Count, ImageField, DateTimeField
from django.utils import timezone
from django.conf import settings
from .utils import make_thumbnail, remove_img


class ChatUser(AbstractUser):
    image = ImageField(upload_to=settings.USER_IMAGES_DIR, default=settings.DEFAULT_IMAGE)
    last_activity = DateTimeField(default=timezone.now)

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        instance._old_img = values[field_names.index('image')]
        return instance

    def _make_thumbnail(self, field: ImageField):
        thumbnail = make_thumbnail(field)
        field.save(field.name, thumbnail, save=False)

    def save(self, *args, **kwargs):
        if hasattr(self, '_old_img') and self._old_img != self.image:
            self._make_thumbnail(self.image)

            if settings.DEL_OLD_IMAGES and self._old_img != settings.DEFAULT_IMAGE:
                remove_img(self._old_img)

        return super().save(*args, **kwargs)

    def get_my_dialogs(self):
        dialogs = self.dialogs.all()
        return dialogs.annotate(count_msgs=Count('messages')).filter(count_msgs__gte=1)

    def is_online(self):
        delta = settings.USER_ONLINE_DELTA
        return (timezone.now() - self.last_activity) < delta

    def __str__(self):
        return f'user_{self.id}'


class _UserModel:

    def __getattribute__(self, item):
        user_model = get_user_model()
        return getattr(user_model, item)

UserModel = _UserModel()
