import { handlerPath } from '@libs/handlerResolver';
import ingestDataSchema from '../shared/ingestDataSchema';

export default {
  handler: `${handlerPath(__dirname)}/handler.main`,
  events: [
    {
      http: {
        method: 'post',
        path: 'ingest-data/Datastreams',
        authorizer: { name: 'postDataAuthorizer', resultTtlInSeconds: 0 },
        request: {
          schema: {
            'application/json': ingestDataSchema,
          },
        },
      },
    },
  ],
};
