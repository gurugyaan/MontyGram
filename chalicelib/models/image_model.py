import time
from dataclasses import dataclass
from typing import ClassVar, Optional
from chalicelib.common.aws_dynamodb import AWSDynamoDB

@dataclass
class ImageDetailModel:
    # Class Variables (Not Present in the Instance)
    table_name: ClassVar[str] = "montygram_image_details"
    pk: ClassVar[str] = "user_id"
    sk: ClassVar[str] = "image_id"

    # Instance Variables (Will be Saved in the Database)
    user_id: str
    image_id: str
    image_format: str
    image_mode: str
    image_width: int
    image_height: int
    created_timestamp: Optional[int] = -1
    is_deleted: Optional[bool] = False
    deleted_timestamp: Optional[int] = -1

    def __post_init__(self):
        self.validate()
        self._add_additional_info()

    def _add_additional_info(self):
        self.created_timestamp = int(time.time())
        self.deleted_timestamp = -1
        is_deleted = False


    def validate(self):
        if not self.user_id:
            raise ValueError("User Id cannot be empty")
        if not self.image_id:
            raise ValueError("Image Id Cannot be empty")

    def save(self):
        print(self.__dict__)
        return AWSDynamoDB(self.table_name).insert_record(self.__dict__)

    @classmethod
    def delete_image(cls, user_id, image_id):
        return AWSDynamoDB(cls.table_name).delete_record(user_id, image_id, cls.pk, cls.sk)


    @classmethod
    def fetch_all_images_for_user(cls, user_id):
        user_images = AWSDynamoDB(cls.table_name).fetch_records_by_pk(user_id, cls.pk)
        return user_images

    @classmethod
    def fetch_image_by_id(cls, user_id, image_id):
        image_details = AWSDynamoDB(cls.table_name).fetch_record_by_pk_sk(user_id, image_id, cls.pk, cls.sk)
        return image_details
