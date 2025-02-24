import json, os
from chalice import Blueprint, Response
from chalicelib.common.cors_support import cors_config
from chalicelib.helpers.image_helper import ImageHelper


images_api = Blueprint(__name__)
accepted_types = ['image/png']

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

@images_api.route('/api/v1/image/download', methods=['GET'])
def download_image():
    image_name = images_api.current_request.query_params.get('image_name')
    if not image_name:
        return {'error': 'image_name is required'}, 400

    tmp_image_path = os.path.join('/tmp', image_name)

    # Check if the image exists in the /tmp directory
    if not os.path.exists(tmp_image_path):
        return {'error': 'Image not found in /tmp'}, 404

    # Read the image file
    with open(tmp_image_path, 'rb') as file:
        image_data = file.read()

    # Return the image as a response
    return Response(
        body=image_data,
        status_code=200,
        headers={
            'Content-Type': 'image/jpeg',  # Adjust content type based on your image format
            'Content-Disposition': f'attachment; filename="{image_name}"'
        }
    )

@images_api.route('/api/v1/view_image/id/{image_id}', methods=['GET'])
def view_image_by_id(image_id):
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

    except NoCredentialsError:
        return {'error': 'Credentials not available'}, 403
    except ClientError as e:
        return {'error': str(e)}, 400

