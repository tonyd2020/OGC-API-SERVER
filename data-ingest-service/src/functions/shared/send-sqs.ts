import * as AWS from 'aws-sdk';
import { SendMessageRequest } from 'aws-sdk/clients/sqs';

AWS.config.update({ region: 'ap-southeast-2' });
const SQS = new AWS.SQS({ apiVersion: '2012-11-05' });

function sendMessage(params) {
  return new Promise<void>(function (resolve, reject) {
    SQS.sendMessage(params, (err, result) => {
      if (err) {
        console.log(err);
        reject(err);
      }
      console.log(result);
      resolve();
    });
  });
}

export const sendSQS = async (message: string, path: string): Promise<void> => {
  const params: SendMessageRequest = {
    MessageBody: JSON.stringify({ message, path }),
    QueueUrl: process.env.INGEST_QUEUE_URL,
    MessageAttributes: {
      'Sample-Table-Schema': {
        DataType: 'String',
        StringValue: 'Sensor data',
      },
      'Device-Table-Schema': {
        DataType: 'String',
        StringValue: 'Sensor data',
      },
    },
  };

  await sendMessage(params);
};
