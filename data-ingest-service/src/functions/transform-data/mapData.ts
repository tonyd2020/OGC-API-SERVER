export const mapData = (params) => {
  if (params.path == 'Things') {
    params.message = {
      // name: params.message.location_name,
      name: params.message['Device-Table-Schema'].location_name,
      description: '',
      properties: params.message,
    };
  }

  if (params.path == 'Locations') {
    params.message = {
      name: params.message['SubSite-Table-Schema'].name,
      description: '',
      encodingType: 'application/geo+json',
      location: {
        type: 'Point',
        coordinates: [
          params.message['Site-Table-Schema'].todo_geo_fence,
          params.message['SubSite-Table-Schema'].todo_geo_fence,
        ],
      },
      properties: params.message,
      Things: [{ '@iot.id': params.message.Relations.Thing }],
    };
  }

  if (params.path == 'Sensors') {
    params.message = {
      name: params.message['OemSensor-Table-Schema'].name,
      description: params.message['OemSensor-Table-Schema'].description,
      encodingType: 'application/pdf',
      properties: params.message,
      metadata: '',
    };
  }

  if (params.path == 'ObservedProperties') {
    params.message = {
      name: params.message['OemDevice-Table-Schema'].name,
      description: '',
      properties: params.message,
      definition: '',
    };
  }

  if (params.path == 'Datastreams') {
    params.message = {
      name: params.message['Sample-Table-Schema'].metric,
      description: '',
      observationType: '',
      unitOfMeasurement: {
        name: params.message['Sample-Table-Schema'].metric,
        symbol: params.message['Sample-Table-Schema'].metric,
        definition: '',
      },
      Thing: { '@iot.id': params.message.Relations.Thing },
      Sensor: { '@iot.id': params.message.Relations.Sensor },
      ObservedProperty: {
        '@iot.id': params.message.Relations.ObservedProperty,
      },
    };
  }

  if (params.path == 'Observations') {
    params.message = {
      result: params.message['Sample-Table-Schema'].value,
      resultTime: params.message['Sample-Table-Schema'].time,
      parameters: params.message['Sample-Table-Schema'],
      Datastream: { '@iot.id': params.message.Relations.Datastream },
    };
  }

  return params;
};
