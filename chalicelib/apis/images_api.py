import json, os
from chalice import Blueprint, Response
from chalicelib.common.cors_support import cors_config
from chalicelib.helpers.image_helper import ImageHelper


images_api = Blueprint(__name__)
accepted_types = ['image/png', 'multipart/form-data', 'image/jpeg']

#Assuming we will have multiple users in this project and using one specific user for dev (defined below)
#Ideally the user id will be retrieved from the auth flow (JWT token) after successfull validation.
user_id = "abcd1234xyz"

@images_api.route('/api/v1/images/list', methods=['GET'], cors=cors_config)
def list_user_images():
    try:
        user_images_list = ImageHelper().fetch_all_images_for_user(user_id)
        return Response(status_code=200, body={"images": user_images_list})
    except Exception as err:
        return Response(status_code=500, body={"error": str(err)})

@images_api.route('/api/v1/images/upload', methods=['POST'], cors=cors_config, content_types=accepted_types)
def upload_image():
    try:
        content_type = images_api.current_request.headers.get('Content-Type')
        if content_type != 'image/png':
            return Response(status_code=400, body={"error": "Unsupported media type: {}'.format(content_type)"})

        raw_body = images_api.current_request.raw_body
        is_uploaded = ImageHelper().process_uploaded_image(raw_body, user_id)
        if is_uploaded:
            return Response(status_code=200, body={"message": "Image uploaded successfully!"})
        else:
            return Response(status_code=400, body={"error": "Failed to process image!"})
    except Exception as err:
        return Response(status_code=500, body={"error": str(err)})

@images_api.route('/api/v1/download/id/{image_id}', methods=['GET'])
def view_or_download_image_by_id(image_id):
    try:
        image_data, content_type = ImageHelper().download_image(user_id, image_id)
        headers = {
            'Content-Type': content_type,
            'Content-Disposition': f'attachment; filename="{os.path.basename(f"{image_id}.png")}"'
        }
        return Response(body=image_data, status_code=200, headers=headers)
    except Exception as err:
        return Response(status_code=500, body={"error": str(err)})



@images_api.route('/api/v1/delete/image/{image_id}', methods=['GET'])
def delete_image_by_id(image_id):
    try:
        is_deleted = ImageHelper().delete_image(user_id, image_id)
        if is_deleted:
            return Response(status_code=200, body={"message": "Image deleted successfully!"})
        else:
            return Response(status_code=400, body={"error": "Failed to delete image!"})
    except Exception as err:
        return Response(status_code=500, body={"error": str(err)})
