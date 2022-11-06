/* eslint-disable no-template-curly-in-string */
import type { AWS } from '@serverless/typescript';

import transformData from '@functions/transform-data';
import postDataAuthorizer from '@functions/post-data-authorizer';
import ingestDataThings from '@functions/ingest-data-things';
import ingestDataLocations from '@functions/ingest-data-locations';
import ingestDataSensors from '@functions/ingest-data-sensors';
import ingestDataObservations from '@functions/ingest-data-observations';
import ingestDataObservedProperties from '@functions/ingest-data-observed-properties';
import ingestDataStreams from '@functions/ingest-data-streams';
import frostAuthProxy from '@functions/frost-auth-proxy';
import hello from '@functions/hello';

const serverlessConfiguration: AWS = {
  service: 'data-ingest-service',
  frameworkVersion: '2',
  custom: {
    defaultStage: 'dev',
    webpack: {
      webpackConfig: './webpack.config.js',
      includeModules: true,
    },
  },
  plugins: [
    'serverless-webpack',
    'serverless-offline',
    'serverless-prune-plugin',
  ],
  provider: {
    name: 'aws',
    runtime: 'nodejs14.x',
    region: 'ap-southeast-2',
    stage: '${opt:stage, env:STAGE, self:custom.defaultStage}',
    iamRoleStatements: [
      {
        Effect: 'Allow',
        Action: ['sqs:*'],
        Resource: [
          {
            'Fn::GetAtt': ['ingestQueue', 'Arn'],
          },
        ],
      },
    ],
    apiGateway: {
      minimumCompressionSize: 1024,
      shouldStartNameWithService: true,
    },
    environment: {
      SECRET_KEY: 'P9rRx5Q8Py',
      INGEST_QUEUE_URL: { Ref: 'ingestQueue' },
      FROST_SERVER_URL: 'https://frost-server.anthonydera.com',
      FROST_SERVER_USERNAME: 'admin',
      FROST_SERVER_PASSWORD: 'admin',
    },
    lambdaHashingVersion: '20201221',
  },
  functions: {
    transformData,
    postDataAuthorizer,
    ingestDataThings,
    ingestDataLocations,
    ingestDataSensors,
    ingestDataObservations,
    ingestDataObservedProperties,
    ingestDataStreams,
    frostAuthProxy,
    hello,
  },
  resources: {
    Resources: {
      ingestQueue: {
        Type: 'AWS::SQS::Queue',
        Properties: {
          QueueName: 'ingestQueue',
        },
      },
    },
  },
};

module.exports = serverlessConfiguration;
