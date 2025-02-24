# MontyCloud

## Description

This project is built using AWS Chalice and utilizes AWS Lambda, AWS API Gateway, DynamoDB, and AWS S3.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running Locally](#running-locally)
- [Deploying to AWS](#deploying-to-aws)
- [Validation](#validation)

## Prerequisites

- AWS CLI installed and configured with the necessary credentials.
- LocalStack installed (for local development).

## Setup

### LocalStack Environment

1. **Run LocalStack Setup Script**

   ```bash
   ./localstack_setup.sh
   ```

2. **Start LocalStack**

   ```bash
   ./run_local_stack.sh
   ```

3. **Create DynamoDB Table in LocalStack**

   ```bash
   ./create_dynamodb_table_in_localstack.sh
   ```

4. **Create S3 Bucket in LocalStack**

   ```bash
   ./create_s3_bucket_in_localstack.sh
   ```

## Running Locally

1. **Navigate to the Project Directory**

   ```bash
   cd /montycloud
   ```

2. **Run Chalice Locally**

   ```bash
   chalice local --stage local
   ```

## Deploying to AWS

To deploy the project directly to AWS, use the following command:

```bash
chalice deploy --stage prod
```

**Note:** Ensure that your AWS credentials are configured in the AWS CLI for this to work.

## Validation

You can validate the creation of the DynamoDB table and S3 bucket using the provided validation scripts.

