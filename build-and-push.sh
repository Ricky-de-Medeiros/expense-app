#!/bin/bash

# CONFIGURATION
AWS_REGION="ap-southeast-2"
REPOSITORY_NAME="expense-app-repository"  
VERSION="v1.0.0"
IMAGE_NAME="expense-app"
ACCOUNT_ID="898101087885"

# Full ECR URI
ECR_URI="${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${REPOSITORY_NAME}"

echo "🔐 Logging into ECR..."
aws ecr get-login-password --region "$AWS_REGION" | docker login --username AWS --password-stdin "$ECR_URI"

echo "🐳 Building Docker image..."
docker build -t "${IMAGE_NAME}" .

echo "🏷 Tagging image..."
docker tag "${IMAGE_NAME}" "${ECR_URI}:latest"
docker tag "${IMAGE_NAME}" "${ECR_URI}:${VERSION}"

echo "📤 Pushing images to ECR..."
docker push "${ECR_URI}:latest"
docker push "${ECR_URI}:${VERSION}"

echo "✅ Done. Image pushed as: ${ECR_URI}:latest and ${VERSION}"
