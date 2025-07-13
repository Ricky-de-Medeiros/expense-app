# Expense App - Business Expense Report Generator

A Python-based Streamlit web application that processes PDF bank statements, extracts business-related expenses, and generates categorized reports for tax declaration. Designed with a modular architecture and deployed using AWS services, including ECS Fargate, Lambda, CloudWatch, and S3. CI/CD is handled through AWS CodePipeline and CodeBuild.

---

## Project Overview

**Main Features:**

* Upload CSV bank statements
* Apply vendor rules and business profiles
* Categorize and visualize business expenses
* Generate Google Sheets-ready reports with business usage percentages

**Tech Stack:**

* **Frontend**: [Streamlit](https://streamlit.io/)
* **Backend**: Python 3.x
* **Infrastructure**: AWS CloudFormation, ECS Fargate, S3, Lambda, CloudWatch
* **CI/CD**: AWS CodePipeline, CodeBuild

---

## Deployment

This project uses a modular CloudFormation deployment structure. Deploy the stacks in the following order:

### 1. Prerequisites Stack

**Creates**: S3 artifacts bucket, KMS key.

```sh
aws cloudformation deploy \
  --stack-name expense-app-pipeline-prereqs \
  --template-file infra/pipeline-prereqs-template.yaml \
  --capabilities CAPABILITY_NAMED_IAM
```

### 2. ECR Stack

**Creates**: ECR repository.

```sh
aws cloudformation deploy \
  --stack-name expense-app-ecr \
  --template-file infra/ecr-template.yaml \
  --capabilities CAPABILITY_NAMED_IAM
```

### 3. CI/CD Pipeline Stack

**Creates**: CodePipeline, CodeBuild projects, IAM roles.

```sh
aws cloudformation deploy \
  --stack-name expense-app-pipeline \
  --template-file infra/pipeline-template.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    SourceRepoName=<bitbucket-repo-name> \
    SourceBranchName=main
```

### 4. Application Infrastructure Stack

**Creates**: ECS Cluster, Task Definition, Lambda trigger, CloudWatch resources, S3 buckets.

```sh
aws cloudformation deploy \
  --stack-name expense-app-infra \
  --template-file infra/app-infra-template.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    VpcExportName=expense-app-VPC \
    SubnetExportName=expense-app-Subnets \
    SecurityGroupExportName=expense-app-AppSG
```

---

## Usage

1. Push to the main Bitbucket branch.
2. Pipeline builds and pushes the Docker image to ECR.
3. App can be triggered by visiting the ECS-hosted URL or via S3 trigger.

---

## Future Enhancements

* Add user authentication with Cognito
* Multi-account deployment support
* Scheduled report generation

---

## Author

**Ricky de Medeiros**
DevSecOps Engineer | AWS Builder

---
