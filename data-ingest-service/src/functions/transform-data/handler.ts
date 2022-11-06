import 'source-map-support/register';

import { SQSHandler } from 'aws-lambda';
import axios from 'axios';
import { mapData } from './mapData';

const transformData: SQSHandler = async (event) => {
  console.log(`Event is ${JSON.stringify(event)}`);
  const frostServerUrl = process.env.FROST_SERVER_URL;
  const mappedData = mapData(JSON.parse(event.Records[0].body));
  console.log(mappedData);
  try {
    const serverUrl = `${frostServerUrl}/FROST-Server/v1.1/${mappedData.path}`;
    console.log(serverUrl);
    const response = await axios({
      method: 'post',
      url: `${serverUrl}`,
      data: mappedData.message,
      auth: {
        username: process.env.FROST_SERVER_USERNAME,
        password: process.env.FROST_SERVER_PASSWORD,
      },
    });
    console.log('response', response.data);
    console.log('response status', response.status);
  } catch (err) {
    console.log('error', err);
  }
};

export const main = transformData;
