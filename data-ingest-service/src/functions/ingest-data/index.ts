import { handlerPath } from '@libs/handlerResolver';
import schema from '../shared/ingestDataSchema';

export default {
  handler: `${handlerPath(__dirname)}/handler.main`,
  events: [
    {
      http: {
        method: 'post',
        path: 'ingest-data',
        authorizer: { name: 'postDataAuthorizer', resultTtlInSeconds: 0 },
        request: {
          schema: {
            'application/json': schema,
          },
        },
      },
    },
  ],
};
