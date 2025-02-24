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
    created_timestamp: int
    is_deleted: bool
    deleted_timestamp: int

    def __post_init__(self):
        self.validate()

    def validate(self):
        if not self.user_id:
            raise ValueError("User Id cannot be empty")
        if not self.image_id:
            raise ValueError("Image Id Cannot be empty")

    def save(self):
        return AWSDynamoDB(self.table_name).insert_record(self.__dict__)

    @classmethod
    def fetch_all_images_for_user(cls, user_id):
        user_images = AWSDynamoDB(cls.table_name).fetch_records_by_pk(user_id, cls.pk)
        return user_images
