from os import path, listdir
from tempfile import TemporaryDirectory
from django.conf import settings
from djoser.serializers import UserCreateSerializer
from rest_framework import status
from django.utils import timezone
from core.tests import LoginTestCase
from chat_user.serializers import ChatUserSerializer
from core.utils import random_string
from chat_user.models import UserModel


class TestUser(LoginTestCase):
    users_count = 0
    need_to_login = True

    def _get_images_paths(self):
        new_images_dir = path.join(settings.MEDIA_ROOT, settings.USER_IMAGES_DIR)
        imgs = listdir(new_images_dir)
        return [path.join(new_images_dir, img) for img in imgs]

    def test_change_image(self):
        self.assertTrue(self.current_user.image.name == settings.DEFAULT_IMAGE)
        default_image_path = path.join(settings.MEDIA_ROOT, settings.DEFAULT_IMAGE)

        with TemporaryDirectory() as temp_dir, open(default_image_path, 'rb') as test_img:

            # Now all images will be saved in temp dir
            settings.MEDIA_ROOT = temp_dir

            res=self.client.patch(f'/users/{self.current_user.id}/', data={'image': test_img})
            self.current_user.refresh_from_db()

            # Check that we changed image
            imgs_pahts = self._get_images_paths()
            self.assertTrue(len(imgs_pahts) == 1, f'Awaited 1 img but got {len(imgs_pahts)}')
            image_path = imgs_pahts.pop()
            self.assertTrue(image_path == self.current_user.image.path, 'Didnt change image')

            # Check that we really made thumbnail
            test_img.seek(0)
            self.assertTrue(len(test_img.read()) > (self.current_user.image.size * 4),
                            'Didnt make thumbnail')

            test_img.seek(0)
            self.client.patch(f'/users/{self.current_user.id}/', data={'image': test_img})
            self.current_user.refresh_from_db()

            #Check that we change user image again
            new_imgs_pahts = self._get_images_paths()
            self.assertTrue(len(new_imgs_pahts) == 1)
            new_img_paht = new_imgs_pahts.pop()
            self.assertTrue(new_img_paht == self.current_user.image.path)

    def test_retrieve(self):
        self.current_user.refresh_from_db()
        res = self.client.get('/users/me/')
        data = ChatUserSerializer(self.current_user,
                                  context={'request': res.wsgi_request}).data

        self.assertEqual(res.data, data, 'Got wrong serialized data')

    def test_create(self):
        self.logout()
        res = self.client.post('/users/', data={'username': random_string(),
                                                'password': random_string()})
        self.assertTrue(res.status_code == status.HTTP_201_CREATED)
        new_user = UserModel.objects.get(id=res.data['id'])
        self.assertEqual(res.data, UserCreateSerializer(new_user).data, 'Got wrong serialized data')
        self.login()

    def test_is_online(self):
        self.current_user.last_activity = timezone.now()
        self.assertTrue(self.current_user.is_online())
        self.current_user.last_activity = timezone.now() - (settings.USER_ONLINE_DELTA * 2)
        self.assertFalse(self.current_user.is_online())