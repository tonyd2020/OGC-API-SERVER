import 'source-map-support/register';
import {
  formatErrorResponse,
  formatJSONResponse,
  formatForbiddenResponse,
} from '@libs/apiGateway';
import { middyfy } from '@libs/lambda';
import AuthService from './AuthService';
import axios from 'axios';
import { APIGatewayProxyEvent } from 'aws-lambda';

const frostAuthProxy = async (event: APIGatewayProxyEvent) => {
  console.log(`Event is ${JSON.stringify(event)}`);
  const authService = new AuthService();
  const frostPath = event.path.replace('/sensors/', '');
  let serverUrl = `${process.env.FROST_SERVER_URL}/FROST-Server/${frostPath}`;
  // Check if query string parameters are present
  if (event.queryStringParameters != null) {
    serverUrl = `${serverUrl}?`; // Append the query delimiter to the url
    for (const key in event.queryStringParameters) {
      if (
        Object.prototype.hasOwnProperty.call(event.queryStringParameters, key)
      ) {
        // Append an Ampersand in between key-value pairs
        serverUrl = `${serverUrl}${key}=${event.queryStringParameters[key]}&`;
      }
    }
    // Remove the unwanted Ampersand after the last query string
    if (serverUrl.charAt(serverUrl.length - 1) == '&') {
      serverUrl = serverUrl.slice(0, -1);
    }
  }

  console.log(serverUrl);
  if (!authService.isReadOnlyAuthorized(event)) {
    return formatForbiddenResponse({
      message: `Forbidden`,
      event,
    });
  }
  try {
    const { data } = await axios.get(serverUrl, {
      auth: {
        username: process.env.FROST_SERVER_USERNAME,
        password: process.env.FROST_SERVER_PASSWORD,
      },
    });

    // Removed the 'message' field to make the output JSON equivalent to the FROST server
    return formatJSONResponse(data);
  } catch (err) {
    console.log(err);
    return formatErrorResponse({
      message: `An error occured`,
      event: err,
    });
  }
};

export const main = middyfy(frostAuthProxy);
