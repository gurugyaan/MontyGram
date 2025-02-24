from chalice import CORSConfig

cors_config = CORSConfig(
    allow_origin='*',
    allow_headers=['Content-Type', 'X-Amz-Date', 'Authorization', 'X-Api-Key', 'X-Amz-Security-Token']
)
