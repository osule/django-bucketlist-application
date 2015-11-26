# API Documentation

Bucketlist Tracker exposes its API via the following endpoints to developers:

##Available Endpoints

| Endpoint | Description |
| ---- | --------------- |
| `POST /api/auth/login` | Login user. Session token is valid for an hour|
| `POST /api/auth/logout` | Logout user. |
| `POST /api/auth/register` |  Register user. Request should have _username_ and _password_ in form data. |
| `POST /api/bucketlists/` | Create a new bucket list. Request should have _name_ in form data. |
| `GET /api/bucketlists/` | List all the created bucket lists. |
| `GET /api/bucketlists/:id` | Get single bucket list. |
| `PUT /api/bucketlists/:id` | Update single bucket list. Request should have _name_ in form data. |
| `DELETE /api/bucketlists/:id` | Delete single bucket list. |
| `POST /api/bucketlists/:id/items` | Add a new item to this bucket list. Request should have _name_, _done_(defaults to False) in form data. |
| `PUT /api/bucketlists/:id/items/:item_id` | Update this bucket list. Request should have _name_, _done_(True or False) in form data. |
| `DELETE /api/bucketlists/:id/items/:item_id` | Delete this single bucket list. |
| `GET /api/bucketlists?limit=20` | Get 20 bucket list records belonging to user. Allows for a maximum of 100 records. |
| `GET /api/bucketlists?q=bucket1` | Search for bucket lists with bucket1 in name. |

##Usage
Example usage of Bucketlist Tracker API using `curl` are as follow:

**Authenticating a user**
```
    curl -X POST -H "Content-Type: application/json" -d '{"username":"your_username", "password":"your_password"}' http://HOST_ADDRESS:HOST_PORT/api/auth/login
    
    {"token":"response_token"}
```

**Fetching bucketlists for a user**
```
    curl -H "Authorization: JWT <your_token>" http://HOST_ADDRESS:HOST_PORT/api/bucketlists/
    
```

**Creating a bucketlist for a user**
```
    curl -X POST -H "Content-Type: application/json" -H "Authorization: JWT <your_token>" -d '{"name":"Hikings"}' http://HOST_ADDRESS:HOST_PORT/api/bucketlists/
```

Check out the docs [here](http://bucketlist-staging/docs/) 