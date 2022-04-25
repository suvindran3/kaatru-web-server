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

The `message` attribute contains a message commonly used to indicate errors or, in the case of deleting a resource, success that the resource was properly deleted.

The `success` attribute describes if the transaction was successful or not.

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
| 201 | `CREATED` |
| 400 | `BAD REQUEST` |
| 404 | `NOT FOUND` |
| 500 | `INTERNAL SERVER ERROR` |
