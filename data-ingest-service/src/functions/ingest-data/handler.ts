import 'source-map-support/register';

import type { ValidatedEventAPIGatewayProxyEvent } from '@libs/apiGateway';
import { formatJSONResponse } from '@libs/apiGateway';
import { middyfy } from '@libs/lambda';

import schema from '../shared/ingestDataSchema';
import { sendSQS } from '../shared/send-sqs';

const ingestData: ValidatedEventAPIGatewayProxyEvent<typeof schema> = async (
  event,
) => {
  console.log(`Event is ${JSON.stringify(event)}`);
  // @ts-ignore
  await sendSQS(event.body.sensorData);
  return formatJSONResponse({
    message: `Success`,
    event,
  });
};

export const main = middyfy(ingestData);
