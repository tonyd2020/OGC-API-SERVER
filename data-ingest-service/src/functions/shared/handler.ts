import 'source-map-support/register';

import type { ValidatedEventAPIGatewayProxyEvent } from '@libs/apiGateway';
import { formatJSONResponse } from '@libs/apiGateway';
import { middyfy } from '@libs/lambda';

import schema from './ingestDataSchema';
import { sendSQS } from './send-sqs';

const ingestData: ValidatedEventAPIGatewayProxyEvent<typeof schema> = async (
  event,
) => {
  console.log(`Event is ${JSON.stringify(event)}`);
  const path = event.path.split('/').slice(-1)[0];
  // @ts-ignore
  await sendSQS(event.body, path);
  return formatJSONResponse({
    message: `Success`,
    event,
  });
};

export const handler = middyfy(ingestData);
