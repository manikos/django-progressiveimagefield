from os.path import split, splitext
from PIL import Image, ImageFilter

from django.db.models.fields.files import ImageField
from django.core.files.uploadedfile import InMemoryUploadedFile


THUMB_EXT = '_thumb'


class ProgressiveImageField(ImageField):

    def pre_save(self, model_instance, add):
        image = super().pre_save(model_instance, add)
        if image:
            self.generate_thumb(image)
        return image

    def in_memory(self, image):
        return type(image) is InMemoryUploadedFile

    def build_thumb_path(self, image):
        """
        Build the absolute path of the to-be-saved thumbnail.
        """
        image_file = image.file
        image_name_w_ext = split(image.name)[-1]
        image_name, ext = splitext(image_name_w_ext)
        if not self.in_memory(image_file):
            # `image_file` is already in disk (not in memory).
            # `image_name` is the full path, not just the name
            image_name = image_name.split('/')[-1]
        upload_to = image.field.upload_to
        if not upload_to.endswith('/'):
            upload_to = f'{upload_to}/'
        path_upload_to = f'{upload_to}{image_name}'
        return f'{self.storage.location}/{path_upload_to}{THUMB_EXT}{ext}'

    def generate_thumb(self, image):
        """
        Given a (large) image, generate a 10x10px thumbnail
        with blur effect (in order to keep the size small)
        """
        image_file = image.file
        picture = Image.open(image_file).convert('RGB')
        picture.thumbnail((10, 10))
        picture.filter(ImageFilter.GaussianBlur(radius=4))
        absolute_path = self.build_thumb_path(image)
        self.save_thumb(picture, absolute_path)

    def save_thumb(self, picture, absolute_path):
        picture.save(absolute_path)
