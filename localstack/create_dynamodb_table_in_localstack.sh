aws --endpoint-url http://localhost:4566 dynamodb create-table \
    --table-name montygram_image_details \
    --attribute-definitions \
        AttributeName=user_id,AttributeType=S \
        AttributeName=image_id,AttributeType=S \
    --key-schema \
        AttributeName=user_id,KeyType=HASH \
        AttributeName=image_id,KeyType=RANGE \
    --provisioned-throughput \
        ReadCapacityUnits=10,WriteCapacityUnits=10