import { APIGatewayAuthorizerEvent, PolicyDocument } from 'aws-lambda';

export type AuthPolicy = {
  principalId: string;
  policyDocument: PolicyDocument;
};
export default class AuthService {
  private secretKey: string;

  constructor() {
    this.secretKey = process.env.SECRET_KEY;
  }

  private getPolicyDocument = (
    effect: string,
    resource: string,
  ): PolicyDocument => {
    return {
      Version: '2012-10-17',
      Statement: [
        {
          Action: 'execute-api:Invoke',
          Effect: effect,
          Resource: resource,
        },
      ],
    };
  };

  private getToken = (event: APIGatewayAuthorizerEvent): string => {
    if (!event.type || event.type !== 'TOKEN') {
      throw new Error('Expected "event.type" parameter to have value "TOKEN"');
    }

    const tokenString = event.authorizationToken;
    if (!tokenString) {
      throw new Error(
        'Expected "event.authorizationToken" parameter to be set',
      );
    }

    const match = tokenString.match(/^Bearer (.*)$/);
    if (!match || match.length < 2) {
      throw new Error(
        `Invalid Authorization token - ${tokenString} does not match "Bearer .*"`,
      );
    }
    return match[1];
  };

  authenticate = (event: APIGatewayAuthorizerEvent): AuthPolicy => {
    const token = this.getToken(event);

    if (token !== this.secretKey) {
      console.log('invalid token');
      return {
        principalId: 'frost',
        policyDocument: this.getPolicyDocument('Deny', event.methodArn),
      };
    }

    return {
      principalId: 'frost',
      policyDocument: this.getPolicyDocument('Allow', event.methodArn),
    };
  };
}
