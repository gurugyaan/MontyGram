import os
import uuid

from PIL import Image
from chalicelib.common.aws_s3 import AWSS3
from chalicelib.models.image_model import ImageDetailModel

S3_bucket = "montygram-assets"
class ImageHelper:
    def __init__(self):
        self.tmp_location = "/tmp/"
        pass

    # Renames the
    def get_image_name(self, image_id):
        return True


    def process_uploaded_image(self, raw_body, user_id):
        image_id = str(uuid.uuid4())
        file_path = os.path.join(self.tmp_location, f'{image_id}.png')
        with open(file_path, 'wb') as f:
            f.write(raw_body)
        image_metadata = self.get_image_metadata(file_path)
        image_details = {"image_id": image_id, "user_id": user_id}
        print(image_metadata)
        image_metadata.update(image_details)
        is_uploaded = ImageDetailModel(**image_metadata).save()
        return is_uploaded

    def get_image_metadata(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        with Image.open(file_path) as img:
            image_width, image_height = img.size

        metadata = {"image_format": img.format, "image_mode": img.mode,
                    "image_width": image_width, "image_height": image_height}
        return metadata

    def fetch_all_images_for_user(self, user_id):
        return ImageDetailModel.fetch_all_images_for_user(user_id)

    def get_image(self, user_id, image_id):
        return ImageDetailModel.fetch_image_by_id(user_id, image_id)

    def delete_image(self, user_id, image_id):
        # image_details = self.get_image(user_id, image_id)
        s3_key = f"/{user_id}/{image_id}.png"
        AWSS3(S3_bucket).delete_s3_object(s3_key)
        return ImageDetailModel.delete_image(user_id, image_id)



