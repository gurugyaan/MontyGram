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
    image_details = ImageHelper().get_image(user_id, image_id)
    bucket_name = images_api.current_request.query_params.get('bucket_name')
    image_key = images_api.current_request.query_params.get('image_key')
    if not bucket_name or not image_key:
        return {'error': 'bucket_name and image_key are required'}, 400

    try:
        # Download the image from S3
        response = s3.get_object(Bucket=bucket_name, Key=image_key)
        image_data = response['Body'].read()

        # Return the image as a response
        return Response(
            body=image_data,
            status_code=200,
            headers={
                'Content-Type': response['ContentType'],
                'Content-Disposition': f'attachment; filename="{os.path.basename(image_key)}"'
            }
        )
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
