import os
from PIL import Image
from chalicelib.models.image_model import ImageDetailModel


class ImageHelper:
    def __init__(self):
        self.tmp_location = "/tmp/"
        pass


    def process_uploaded_image(self, raw_body, user):
        file_path = os.path.join('/tmp', 'uploaded_image.png')

        # Write the raw body to a file
        with open(file_path, 'wb') as f:
            f.write(raw_body)
        return True

    def get_image_metadata(self, file_name):
        file_path = self.tmp_location + file_name
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        with Image.open(file_path) as img:
            metadata = img.info
        return metadata

    def fetch_all_images_for_user(self, user_id):
        return ImageDetailModel.fetch_all_images_for_user(user_id)

