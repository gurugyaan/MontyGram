from chalice import Chalice
from chalicelib.apis.images_api import images_api
app = Chalice(app_name='montygram')
app.api.binary_types = [
    'image/jpeg',
    'application/json',
    'image/png',
    'image/gif',
    'video/mpeg',
    'video/mp4'
]

app.register_blueprint(images_api)