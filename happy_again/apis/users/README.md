# **Happy-Again-Users API Documentation**  

## Base URL  

```text
    http://127.0.0.1:1234
```

---

## 1. **User Registration API**  

### Method: **POST**  

### Endpoint: `/users`  

#### **Request Payload:**  

```json
{
 "email": "abc@outlook.com",
 "password": "aaaa1111!",
 "language": "english"
}
```

#### **Response: 200 OK**  

```json
{
    "id": "fbbd5322cbab4990b67ce983b52405af",
    "email": "abc@outlook.com",
    "registered_at": "2021-03-05 18:51:43",
    "confirmed_at_by_user": null
}
```

#### **Response: 409 Conflict**  

```text
    User 'abc@abc.com' already registered
```

---

## 2. **Resend User Confirmation Link API**  

### Method: **POST**  

### Endpoint: `/users/resend-confirmation/<user_id>`  

#### **Response: 200 OK**  

```json
{
    "id": "fbbd5322cbab4990b67ce983b52405af",
    "email": "abc@outlook.com",
    "registered_at": "2021-03-05 18:51:43",
    "confirmed_at_by_user": null
}
```

#### **Response: 404 Not Found**  

```
User 'abc@abc.com' not found
```

---

## 3. **User Confirmation API**  

### Method: **GET**  

### Endpoint: `/users/verify/<token_value>`  

#### **Response Codes:**  

- **200 OK** – User confirmed  
- **401 Unauthorized** – Token expired  
- **400 Bad Request** – Invalid token  
- **404 Not Found** – Invalid user  
- **409 Conflict** – User already confirmed  

---

## 4. **User Login API**  

### Method: **POST**  

### Endpoint: `/users/login`  

#### **Request Payload:**  

```json
{
 "email": "abc@outlook.com",
 "password": "abc123"
}
```

#### **Response: 200 OK**  

```json
{
    "id": "fbbd5322cbab4990b67ce983b52405af",
    "email": "abc@abc.com",
    "registered_at": "2021-03-05 18:51:43",
    "confirmed_at_by_user": "2021-03-05 18:56:36",
    "token": {
        "access_token": "<access_token>",
        "refresh_token": "<refresh_token>"
    },
    "is_trusted": true,
    "session_id": "c6b0268b481848299c0c05216dde045c"
}
```

#### **Response Codes:**  

- **404 Not Found** – Invalid user  
- **401 Unauthorized** – Invalid password  
- **403 Forbidden** – Email not confirmed  

---

## 5. **User Session Update API**  

### Method: **PUT**  

### Endpoint: `/users/session/<session_id>`  

#### **Request Payload:**  

```json
{
    "browser": "google_chrome",
    "version": "12",
    "op_system": "ubuntu",
    "screen_resolution": "1024x1024",
    "pixel_density": "250",
    "user_agent": "agent_info"
}
```

#### **Response: 200 OK**  

```json
{
    "id": "dedd88006805435eb7965ded5194c070",
    "start_time": "2021-03-06 12:08:36",
    "end_time": null,
    "last_completed_task": "0",
    "browser": "google_chrome",
    "version": "12",
    "op_system": "ubuntu",
    "screen_resolution": "1024x1024",
    "pixel_density": "250",
    "user_agent": "agent_info",
    "user_id": "fbbd5322cbab4990b67ce983b52405af"
}
```

#### **Response Codes:**  

- **404 Not Found** – Invalid user or session  
- **409 Conflict** – User already logged off  

---

## 6. **User Logoff API**  

### Method: **PUT**  

### Endpoint: `/users/logoff/<session_id>`  

#### **Response Codes:**  

- **200 OK** – User logged off successfully  
- **404 Not Found** – Invalid user or session  
- **409 Conflict** – User already logged off  

---

## 7. **User Info Update API**  

### Method: **PUT**  

### Endpoint: `/users/info/<session_id>`  

#### **Request Payload:**  

```json
{
    "age": 21,
    "gender": "male"
}
```

#### **Response: 200 OK**  

```json
{
    "id": "38d06b53c298417eaed9115a4021f647",
    "age": 21,
    "gender": "male",
    "language": "english",
    "consent": "2021-03-05 18:51:43",
    "user_id": "fbbd5322cbab4990b67ce983b52405af"
}
```

#### **Response Codes:**  

- **404 Not Found** – Invalid user or session  
- **409 Conflict** – User already logged off  
- **404 Not Found** – Invalid user info  

---

## 8. **User Forgot Password API**  

### Method: **POST**  

### Endpoint: `/users/forgot-password`  

#### **Request Payload:**  

```json
{
    "email": "abc@abc.com"
}
```

#### **Response Codes:**  

- **200 OK** – Password reset link sent  
- **404 Not Found** – User not registered  

---

## 9. **User Reset Password API**  

### Method: **POST**  

### Endpoint: `/users/reset-password/<token_value>`  

#### **Request Payload:**  

```json
{
    "email": "abc@abc.com"
}
```

#### **Response Codes:**

- **200 OK** – Password reset successful  
- **400 Bad Request** – Invalid token  
- **401 Unauthorized** – Token expired  
- **404 Not Found** – Invalid user  

---

## Conclusion  

This documentation outlines the Happy-Again-Users API endpoints for managing user registration, authentication, session updates, and password recovery. Use these endpoints to build and maintain a secure and user-friendly service.
