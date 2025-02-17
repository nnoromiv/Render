# Happy Again Backend

## Base URL

```text
    https://127.0.0.1:1234
```

---

## Authentication

**Authorization:** Bearer Token  
Include an `Authorization` header with a valid token:

```text
    Authorization: Bearer <your_token>
```

---

## Endpoints

### 1. **Get User Data**

**Request:**  
`GET /users/{user_id}`

**Description:**  
Retrieve details for a specific user.

**Example Request:**  
`GET /users/10150`

**Headers:**  

- `Authorization`: Bearer Token
- `Content-Type`: application/json  

**Response:**

```json
{
  "user_id": 10150,
  "name": "John Doe",
  "email": "john.doe@example.com",
  "response_time": 1200,
  "status": "active"
}
```

---

### 2. **Create a New User**

**Request:**  
`POST /users`

**Description:**  
Create a new user with the provided details.

**Headers:**  

- `Authorization`: Bearer Token  
- `Content-Type`: application/json  

**Body:**

```json
{
  "name": "Jane Smith",
  "email": "jane.smith@example.com",
  "password": "securepassword123"
}
```

**Response:**

```json
{
  "message": "User created successfully",
  "user_id": 10151
}
```

### 3. **Update User Information**

**Request:**  
`PUT /users/{user_id}`

**Description:**  
Update the information for an existing user.

**Example Request:**  
`PUT /users/10150`

**Headers:**  

- `Authorization`: Bearer Token  
- `Content-Type`: application/json  

**Body:**

```json
{
  "name": "John Doe Updated",
  "status": "inactive"
}
```

**Response:**

```json
{
  "message": "User updated successfully"
}
```

---

### 4. **Delete a User**

**Request:**  
`DELETE /users/{user_id}`

**Description:**  
Delete a user by their `user_id`.

**Example Request:**  
`DELETE /users/10150`

**Headers:**  

- `Authorization`: Bearer Token  

**Response:**

```json
{
  "message": "User deleted successfully"
}
```

### 5. **Get All Users**

**Request:**  
`GET /users`

**Description:**  
Retrieve a list of all users.

**Headers:**  

- `Authorization`: Bearer Token  
- `Content-Type`: application/json  

**Response:**

```json
[
  {
    "user_id": 10150,
    "name": "John Doe",
    "email": "john.doe@example.com"
  },
  {
    "user_id": 10151,
    "name": "Jane Smith",
    "email": "jane.smith@example.com"
  }
]
```

---

### 6. **Filter User Responses**

**Request:**  
`GET /responses?user_id=10150`

**Description:**  
Filter responses for a specific user.

**Example Request:**  
`GET /responses?user_id=10150`

**Response:**

```json
{
  "user_id": 10150,
  "responses": [
    {
      "question_id": 11,
      "response": "2 - No worse than usual",
      "response_time_ms": 1200
    }
  ]
}
```

## Error Handling

**Standard Response Format for Errors:**

```json
{
  "error": {
    "code": 400,
    "message": "Bad Request",
    "details": "The 'email' field is required."
  }
}
```

## Contribution

To run the server open a terminal and go to the repository happy-again-backend, and run `python main.py`

Default database is sqlite. Once the project will be run, It will create a file of the database and the path of the database file will be `happy-again-backend/happy-again/happy_again.db`
