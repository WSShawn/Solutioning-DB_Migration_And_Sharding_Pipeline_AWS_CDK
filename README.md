# Solutioning DB Migration Pipeline with AWS CDK

This project is an AWS CDK (Cloud Development Kit) application written in TypeScript. It provisions infrastructure for a database migration pipeline, including resources such as DocumentDB, RDS PostgreSQL, and a Lambda function for data migration.

## Architecture Overview

The stack includes:
- **Amazon DocumentDB**: A managed NoSQL database for storing data.
- **Amazon RDS PostgreSQL**: A managed relational database for storing migrated data.
- **AWS Lambda**: A Python-based Lambda function for handling data migration between DocumentDB and PostgreSQL.
- **AWS Secrets Manager**: Securely stores credentials for both DocumentDB and PostgreSQL.
- **Amazon VPC**: A Virtual Private Cloud to host the resources securely.
- **Security Groups**: Configured to allow secure communication between the resources.

## Features

- **DocumentDB Cluster**:
  - Configured with a security group to allow MongoDB traffic on port `27017`.
  - Credentials are securely stored in AWS Secrets Manager.
  - Backup retention for 7 days.

- **RDS PostgreSQL Instance**:
  - Configured with a security group to allow PostgreSQL traffic on port `5432`.
  - Credentials are securely stored in AWS Secrets Manager.
  - Backup retention for 7 days.

- **Data Migration Lambda**:
  - Python-based Lambda function for migrating data from DocumentDB to PostgreSQL.
  - Packaged with dependencies using AWS Lambda's Python runtime or a custom Docker image.

## Prerequisites

- AWS CLI installed and configured.
- Node.js (v16 or later) installed.
- AWS CDK Toolkit installed globally:
* `npm install -g aws-cdk`

## Useful Commands
- Synthesize the CloudFormation Template:
* `cdk synth`
- Deploy the Stack:
* `cdk deploy`

## Deployment
- Install dependencies
* `npm install`
- Bootstrap your AWS environment (if not already done):
* `cdk bootstrap`
- Deploy the stack:
* `npx cdk deploy`
- Cleanup & To delete the stack and all associated resources:
* `npx cdk destroy`