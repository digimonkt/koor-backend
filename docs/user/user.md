# User

## Summary

These are the APIs for all 3 types of `users` `job-seeker`, `employer`, and `vendor`. This section includes the APIs for:

- **[Create user](#create-user)**: This route is used to create the user with a particular role
- **[Create user session (login)](#create-user-session-login):** This route is used to create a user session
- **[Forget user password](#delete-user-session-logout):** This route is used to reset the user's password
- **[Delete user session (logout)](#forget-user-password):** This route is used to delete the user session
- **[Get user details](#get-user-details):** This route is used to get user details by id or by token
- **[Update Profile Image](#update-profile-image):** This route is used to update profile Image

## **Create User**

### Summary

- Route: `api/v1/user`
- method: `POST`
- request :

  request can be one of the following types:

  ```js
  {
    "body": {
      	"email": "test@test.com",
  		"mobileNumber": "",
  		"password": "123456789",
  		"role": "job_seeker" || "employer" || "vendor",
  		"countryCode": "+91"
    }
  }

  {
    "body": {
        "email": "test@test.com",
  		"mobileNumber": "1234567890",
  		"password": "123456789",
  		"role": "job_seeker" || "employer" || "vendor",
  		"countryCode": "+91"
      }
  }

  {
    "body": {
      	"email": "",
  		"mobileNumber": "123456789",
  		"password": "123456789",
  		"role": "job_seeker" || "employer" || "vendor",
  		"countryCode": "+91"
      }
  }
  ```

- response:

  ```js
  {
    "code": 204,
    "headers": {
      "x-access": "${JWT_TOKEN}",
      "x-refresh": "${JWT_TOKEN}"
    },
    "body": {
      "message": "User Created Successfully"
    }
  }
  ```

> Note: When a `user` is creating we need to create a `session` of the `user` also

## **Create user session (login):**

- Route: `api/v1/user/session`
- method: `POST`
- request:

  request can be one of the following types:

  ```js
  {
    "body": {
      "email": "test@test.com",
      "mobile": "",
      "password": "123456789"
    }
  }
  ```

  ```js
  {
    "body": {
      "email": "",
      "mobile": "1234567890",
      "password": "123456789"
    }
  }
  ```

- response:

  1.  If Credentials match:

      ```js
      {
        "code": 204,
        "headers": {
          "x-access": "${JWT_TOKEN}",
          "x-refresh": "${JWT_TOKEN}"
        },
        "data": {
          "message": "User LoggedIn Successfully"
        }
      }
      ```

  2.  If credentials did not match:

      ```js
      {
      	"code": 401,
      	"data": {
      		"message": "Invalid Email or Mobile Number or Password"
      	}
      }
      ```

## **Forget user password:**

### Summary:

These routes are used to reset the `user`’s `password`. This will be 2 step process

1.  get the `user`’s email and send a password reset link with `token`
2.  when the user requests to update the password with the `token`, we will update it according to the `token` validity.

### Step 1:

- route: `api/v1/user/forget-password`
- method: `GET`
- request:

  ```js
  {
    "query": {
      "email": "test@gmail.com"
    }
  }
  ```

### Step 2:

- route: `api/v1/user/change-password/:token`
- method: `PUT`
- request:

  ```js
  {
    "body": {
  	    "password": "123456789"
    },
    "params": {
  	    "token": "${TOKEN}" // token from email link
    }
  }
  ```

- response:

  ```js
  {
    "code": 204,
    "data": {
      "message": "Password updated successfully"
    }
  }
  ```

## **Delete user session (logout)**

### Summary

This route is used to delete `user` `sessions`. We are not exactly going to delete the `user`'s session, but we are going to mark them as invalid.

- route: `api/v1/user/delete-session`
- method: `DELETE`
- response:

  ```js
  {
    "code": 204,
    "data": {
      "message": "Logged Out successfully"
    }
  }
  ```

## **Get User Details**

### Summary

This route is used to get `user` details. If `userId` is provided inside the `query` then provide the user’s details of the given `userId` else provide the details of the `loggedIn` user.

- route: `api/v1/user`
- method: `GET`
- request:

  ```js
  {
    "query": {
      "userId": string || null
    }
  }
  ```

- response: data varies according to the `user’s` `role`

  ```js
  // job seeker
  {
    "code": 200,
    "data": {
      "id": "${UUID}"
      "email": "test@gmail.com",
      "mobile_number": "1234567890",
      "country_code": "+91",
      "name": "Test User",
      "image": "/${PATH}",
      "role": "job_seeker",
      "profile": {
        "gender": "male" || "female",
        "dob": DD/MM/YYYY,
        "employment_status": "employed" || "fresher" || "other",
        "description": "This is the description of the user...",
        "market_information": false,
        "job_notification": false,
      },
      "education_record": [{
        "id": ${UUID}
        "title": "Bechlour of Engineer",
        "start_date": DD/MM/YYYY,
        "end_date": DD/MM/YYYY || null,
        "present": false,
        "organization": "MIT",
        "description": "This is the description of the education..."
      }],
      "work_experience": [{
        "id": ${UUID},
        "title": "Software Engineer",
        "start_date": DD/MM/YYYY,
        "end_date": DD/MM/YYYY || null,
        "present": true,
        "organization": "digimonk Technologies",
        "description": "This is the description of the work experience..."
      }],
      "resume": [{
        "id": ${UUID},
        "title": "Resume",
        "file_path": "/${PATH}",
        "created_at": DD/MM/YYYY,
      }],
      "languages": [{
        "id": ${UUID},
        "language": "English",
        "written": "basic" || "conversational" || "fluent",
        "spoken": "basic" || "conversational" || "fluent"
      }],
      "skills": [{
        "id": ${UUID},
        "skill": "ReactJS",
      }]
      // pending job preferences
    }
  }

  // employer
  {
    code: 200,
    data: {
      "id": "${UUID}"
      "email": "test@gmail.com",
      "mobile_number": "1234567890",
      "country_code": "+91",
      "name": "Test User",
      "image": "/${PATH}",
      "role": "employer",
      "profile": {
        "organization_name": "digimonk Technologies",
        "description": "This is the description of organization...",
        "organization_type": "business" || "ngo" || "government",
        "license_id": "AB1235E5342",
        "license_id_file": "${PATH}"
      }
    }
  }

  // vendor pending
  ```

## Update Profile Image

### Summary

This API is used to update the `display_image` of the user.

> **Note**: This will be the `authenticated` route i.e. if `user` is logged in then only be able to update profile image for some obvious reason.
- route: `api/v1/user/display-image`
- method: `PATCH`
- request
  ```js
  {
    "headers": {
      "Content-Type": "multipart/form-data",
      "Authorization": "${TOKEN}"
    },
    "body": {
      "image": File
    }
  }
  ```
- response:
  ```js
  {
    "code": 200,
    "data": {
      "image": "${PATH}"
    }
  }
  ```
