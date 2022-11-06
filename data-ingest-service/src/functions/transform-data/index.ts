import { handlerPath } from '@libs/handlerResolver';
import type { AWS } from '@serverless/typescript';

const functionInfo: AWS['functions'][string] = {
  handler: `${handlerPath(__dirname)}/handler.main`,
  events: [
    {
      sqs: { arn: { 'Fn::GetAtt': ['ingestQueue', 'Arn'] } },
    },
  ],
};

export default functionInfo;
