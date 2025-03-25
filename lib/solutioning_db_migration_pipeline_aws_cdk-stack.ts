import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as docdb from 'aws-cdk-lib/aws-docdb';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import * as rds from 'aws-cdk-lib/aws-rds';
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class SolutioningDbMigrationPipelineAwsCdkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

     // Construct lambda execution role
     const lambdaExecutionRole = new iam.Role(this, 'LambdaExecutionRole', {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole'),
        iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaVPCAccessExecutionRole'),
      ],
    });

    // Create a VPC for our resources
    const vpc = new ec2.Vpc(this, 'VPC');

    // Create a security group for the DocumentDB cluster
    const docdbSecurityGroup = new ec2.SecurityGroup(this, 'DocDBSecurityGroup', {
      securityGroupName: 'DocDBSecurityGroup',
      vpc: vpc,
      allowAllOutbound: true,
    });
    docdbSecurityGroup.node.addDependency(vpc);

    // Create DocumentDB cluster
    const docdbCluster = new docdb.DatabaseCluster(this, 'DocDBCluster', {
      masterUser: {
        username: 'docdbadmin',
        password: cdk.SecretValue.secretsManager('docdb-credentials', {
          jsonField: 'password',
        }),
      },
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MEDIUM),
      instances: 1,
      vpc: vpc,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
      },
      removalPolicy: cdk.RemovalPolicy.RETAIN,
      securityGroup: docdbSecurityGroup,
      backup: {
        retention: cdk.Duration.days(7),
        preferredWindow: '04:34-05:04',
      },
    });

    // Specify dependencies
    docdbCluster.node.addDependency(vpc);
    docdbCluster.node.addDependency(docdbSecurityGroup);

    // Add an inbound rule to allow inbound traffic on port 27017
    docdbSecurityGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(27017), 'MongoDB Access');


    // Create a security group for the PostgreSQL instance
    const postgresSecurityGroup = new ec2.SecurityGroup(this, 'PostgresSecurityGroup', {
      vpc: vpc,
      allowAllOutbound: true,
    });
    // Allow DocumentDB and Lambda to access PostgreSQL
    postgresSecurityGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(5432), 'PostgreSQL Access');
    // create postgresql database
    const postgresSecret = new secretsmanager.Secret(this, 'PostgresSecret', {
      secretName: 'postgres-credentials',
      generateSecretString: {
        secretStringTemplate: JSON.stringify({ username: 'postgresadmin' }),
        generateStringKey: 'password',
        excludeCharacters: '/@" ',
      },
    });

    // Create RDS PostgreSQL instance
    const postgresInstance = new rds.DatabaseInstance(this, 'PostgresInstance', {
      engine: rds.DatabaseInstanceEngine.postgres({ version: rds.PostgresEngineVersion.VER_15 }),
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO),
      vpc: vpc,
      vpcSubnets: { subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS },
      securityGroups: [postgresSecurityGroup],
      credentials: rds.Credentials.fromSecret(postgresSecret),
      allocatedStorage: 20,
      multiAz: false,
      backupRetention: cdk.Duration.days(7),
      deletionProtection: false,
      removalPolicy: cdk.RemovalPolicy.RETAIN,
    });

    // Create a Lambda function for data migration
    this.constructDataMigrationLambda(
      lambdaExecutionRole,
      vpc,
      docdbSecurityGroup,
      postgresSecurityGroup,
    );
  }


  // create a lambda function that uses python
  constructDataMigrationLambda(
    lambdaExecutionRole: cdk.aws_iam.Role,
    vpc: ec2.Vpc,
    docdbSecurityGroup: ec2.SecurityGroup,
    postgresqlSecurityGroup: ec2.SecurityGroup,
  ){
    const dataMigrationLambda = new lambda.Function(this, 'DataMigrationLambda', {
      functionName: 'DataMigrationLambda',
      runtime: lambda.Runtime.PYTHON_3_12,
      code: lambda.Code.fromAsset('app/datamigration'), // Directory containing your Python code
      handler: 'main.handler',
      role: lambdaExecutionRole,
      timeout: cdk.Duration.minutes(15),
      vpc: vpc,
      securityGroups: [docdbSecurityGroup, postgresqlSecurityGroup],
      environment: {
      },
    });
  }
}
