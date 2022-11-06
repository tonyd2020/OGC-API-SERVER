import { APIGatewayProxyEvent } from 'aws-lambda';

type UserProfile = {
  userId: string;
  userPassword: string;
};

// this array should hold all the userProfiles for farms that need readonly access
// can be moved to a database when required
const defaultProfiles: UserProfile[] = [
  {
    userId: '123123',
    userPassword: '456456',
  },
];

export default class AuthService {
  private userProfiles: UserProfile[];

  constructor() {
    this.userProfiles = defaultProfiles;
  }

  private getToken = (event: APIGatewayProxyEvent): string => {
    const tokenString = event.headers.Authorization;
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

  private isAuthorized = (
    event: APIGatewayProxyEvent,
    token: string,
  ): boolean => {
    // if auth restrictions required per path
    // change this function to check that the path requested matches the id of the user
    // const idFromPath = event.path;
    const { userId } = this.userProfiles.find(
      (user) => user.userPassword === token,
    );
    return this.userProfiles.map((user) => user.userId).includes(userId);
  };

  isReadOnlyAuthorized = (event: APIGatewayProxyEvent): boolean => {
    const token = this.getToken(event);

    if (this.userProfiles.map((user) => user.userPassword).includes(token)) {
      return this.isAuthorized(event, token);
    }
    console.log('invalid token');
    return false;
  };
}
