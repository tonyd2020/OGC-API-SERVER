import { APIGatewayAuthorizerEvent } from 'aws-lambda';
import 'source-map-support/register';
import AuthService, { AuthPolicy } from './AuthService';

const postDataAuthorizer = async (
  event: APIGatewayAuthorizerEvent,
): Promise<AuthPolicy> => {
  console.log(`Event is ${JSON.stringify(event)}`);
  const authService = new AuthService();

  return authService.authenticate(event);
};

export const main = postDataAuthorizer;
