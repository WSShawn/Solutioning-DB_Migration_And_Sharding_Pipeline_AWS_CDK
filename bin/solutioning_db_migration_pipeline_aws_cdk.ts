#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { SolutioningDbMigrationPipelineAwsCdkStack } from '../lib/solutioning_db_migration_pipeline_aws_cdk-stack';

const app = new cdk.App();
new SolutioningDbMigrationPipelineAwsCdkStack(app, 'SolutioningDbMigrationPipelineAwsCdkStack', {
  env: {
    account: "730335418687",
    region: 'us-east-1',
  },
});

app.synth();