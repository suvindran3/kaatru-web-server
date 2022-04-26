# kaatru-web-server

```http
GET /cleanest_route?
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `origin` | `list` | **Required**. A list containing origin latitude and longitude |
| `destination` | `list` | **Required**. A list containing destination latitude and longitude |

## Responses

```javascript
{
  "message": string,
  "status": int,
  "data": list
}
```

The `message` attribute contains a message commonly used to indicate status of the request.

The `status` attribute contains the HTTP status code.

The `data` attribute contains a list of routes found for the given origin and destination with its respective `pm 2.5` aggregate in the following format

```javascript
{
  "route": list,
  "aggregate": float
}
```

The `route` attribute contains list of coordinates which can be used to draw the respective polyline for that route. The data will be in the following format

```javascript
{
  "lat": float,
  "lng": float
}
```

## Status Codes

Server returns the following status codes in its API:

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 400 | `BAD REQUEST` |
| 403 | `ACCESS RESTRICTED` |
| 404 | `NOT FOUND` |
| 500 | `INTERNAL SERVER ERROR` |

#

```http
GET /air_quality?
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `lat` | `float` | **Required**. latitude of the querying location |
| `lng` | `float` | **Required**. longitude of the querying location |

## Responses

```javascript
{
  "message": string,
  "status": int,
  "data": json
}
```

The `message` attribute contains a message commonly used to indicate status of the request.

The `status` attribute contains the HTTP status code.

The `data` attribute contains a JSON object containing latitude, longitude and the respective pm2.5 in the following format

```javascript
{
  "lat": float,
  "lng": float,
  "pm2.5": float
}
```

## Status Codes

Server returns the following status codes in its API:

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 400 | `BAD REQUEST` |
| 403 | `ACCESS RESTRICTED` |
| 404 | `NOT FOUND` |
| 500 | `INTERNAL SERVER ERROR` |

#
