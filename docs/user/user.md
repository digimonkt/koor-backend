# User

## Summary

These are the APIs for all 3 types of `users` `job-seeker`, `employer`, and `vendor`. This section includes the APIs for:

- **[Create user](#create-user)**: This route is used to create the user with a particular role
- **[Create user session (login)](#create-user-session-login):** This route is used to create a user session
- **[Forget user password](#delete-user-session-logout):** This route is used to reset the user's password
- **[Delete user session (logout)](#forget-user-password):** This route is used to delete the user session
- **[Get user details](#get-user-details):** This route is used to get user details by id or by token
- **[Update Profile Image](#update-profile-image):** This route is used to update profile Image
- **[Get Location](#get-location):**
- **[Social Login](#social-login):**
- **[Get User Search](#get-user-search):**
- **[Send OTP](#send-otp):**
- **[OTP Verification](#otp-verification):**
- **[Email Verification](#email-verification):**
- **[Change Password](#change-password):**
- **[Get Notification](#get-notification):**
- **[Save Advanced Filter for User](#save-advanced-filter-for-user):**
- **[Get Advanced Filter for User](#get-advanced-filter-for-user):**
- **[Delete Advanced Filter for User](#delete-advanced-filter-for-user):**
- **[Update Advanced Filter for User](#update-advanced-filter-for-user):**

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
  		"password": "123456789",
  		"role": "job_seeker" || "employer" || "vendor"
    }
  }

  {
    "body": {
      "email": "test@test.com",
  		"mobile_number": "1234567890",
  		"password": "123456789",
  		"role": "job_seeker" || "employer" || "vendor",
  		"country_code": "+91"
      }
  }

  {
    "body": {
  		"mobile_number": "123456789",
  		"password": "123456789",
  		"role": "job_seeker" || "employer" || "vendor",
  		"country_code": "+91"
      }
  }
  ```

- response:

  ```js
  {
    "code": 201,
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
      "role":"job_seeker",
      "password": "123456789"
    }
  }
  ```

  ```js
  {
    "body": {
      "mobile": "1234567890",
      "role": "job_seeker",
      "password": "123456789"
    }
  }
  ```

- response:

  1.  If Credentials match:

      ```js
      {
        "code": 201,
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
      	"code": 400,
      	"data": {
      		"message": "Invalid login credentials."
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
  
- response:

  ```js
  {
    "code": 200,
    "data": {
      "message": "OTP sent to <email>"
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
    "code": 200,
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
        "license_id_file": {
            "path": "/media/2023-02-16/tst/tst_Kj1oVRs.txt",
            "type": "text"
        }
      }
    }
  }

  // vendor pending
  ```

## **Update Profile Image**

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

## **Get Location**

This api is used to get all `Get Location`

- route: `/get-location`
- method: `GET`
- request:

  ```js
  {
    "query": 
    {
      "search": "ind" || ""  // for search data
    },
  }
  
  ```
- response:
  ```js
  {
    "code": 200,
    "data": {
      "predictions": [
          {
            "description": "Indore, Madhya Pradesh, India",
            "matched_substrings": [
                {
                    "length": 5,
                    "offset": 0
                }
            ],
            "place_id": "ChIJ2w1BG638YjkR9EBiNdrEbgk",
            "reference": "ChIJ2w1BG638YjkR9EBiNdrEbgk",
            "structured_formatting": {
                "main_text": "Indore",
                "main_text_matched_substrings": [
                    {
                        "length": 5,
                        "offset": 0
                    }
                ],
                "secondary_text": "Madhya Pradesh, India"
            },
            "terms": [
                {
                    "offset": 0,
                    "value": "Indore"
                },
                {
                    "offset": 8,
                    "value": "Madhya Pradesh"
                },
                {
                    "offset": 24,
                    "value": "India"
                }
            ],
            "types": [
                "locality",
                "political",
                "geocode"
            ]
        },
      ],
    "status": "OK"
    }
  }

  ```

## **Social Login**

### Summary

- Route: `api/v1/user/social-login`
- method: `POST`
- request :

  request can be one of the following types:

  ```js
  {
    "body": {
      "email": "test@test.com",
  		"password": "123456789",
  		"role": "job_seeker" || "employer" || "vendor",
      "source": "google" || "facebook" || "apple"
      "display_image": "https://lh3.googleusercontent.com/a/AGNmyxal8J_JI7khcLOMzjacmvXYbBMLcSV3i__M4TyL=s96-c"
    }
  }

  {
    "body": {
        "email": "test@test.com",
  		"mobile_number": "1234567890",
  		"password": "123456789",
  		"role": "job_seeker" || "employer" || "vendor",
      "source": "google" || "facebook" || "apple",
  		"country_code": "+91"
      }
  }

  {
    "body": {
  		"mobile_number": "123456789",
  		"password": "123456789",
  		"role": "job_seeker" || "employer" || "vendor",
      "source": "google" || "facebook" || "apple",
  		"country_code": "+91"
      }
  }
  ```

- response:

  ```js
  {
    "code": 201,
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



## **Get User Search**

This api is used to get all the `user search` of the employer.
- route: `/search/:role`
- method: `GET`
- request:
  ```js
    // type one
  {
    "params": {
      "role": "employer" || "job_seeker" || "vendor"
    },
    "query": 
    {
      "search": "", // show all results
      "country": "india" || null;, // filter by country
      "city": "delhi" || null;, // filter by city
      "fullTime": true || false || null;, // filter is full time
      "partTime": true || false || null;, // filter is part time
      "contract": true || false || null;, // filter has contract
      "availability": true || false || null;, // filter for availability
      "salary_min": "3500" || null;, // filter for minimum salary
      "salary_max": "4500" || null;, // filter for maximum salary
      "limit": "1" || null;, // page limit
      "page": "1" || null;, // page number
    },
  }
 

  // type two
  {
    "params": {
      "role": "employer" || "job_seeker" || "vendor"
    },
    "query": 
    {
      "search": "b", // show only those results whose title includes `b` only
      "country": "india" || null;, // filter by country
      "city": "delhi" || null;, // filter by city
      "fullTime": true || false || null;, // filter is full time
      "partTime": true || false || null;, // filter is part time
      "contract": true || false || null;, // filter has contract
      "availability": true || false || null;, // filter for availability
      "salary_min": "3500" || null;, // filter for minimum salary
      "salary_max": "4500" || null;, // filter for maximum salary
      "limit": "1" || null;, // page limit
      "page": "1" || null;, // page number
    },
  }

  ```
- response:
  ```js
  {
    code: 200,
    data: {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "762ab061-c083-486d-973f-7016b63528f8",
            "role": "job_seeker",
            "name": null,
            "email": "praveen.vaidhya@digimonk.in",
            "country_code": null,
            "mobile_number": null,
            "is_active": true
        }
      ]
    }
  }
  ```

## **Send OTP**

### Summary

- route: `/send-otp`
- method: `GET`
- request :

  request can be one of the following types:

  ```js
  {
    "query": {
      "email": "test@gmail.com"
    }
  }

  ```

- response:

  ```js
  
  {
    "code": 200,
    "body": {
      "token": "${JWT_TOKEN}",
      "message": "OTP sent to test@gmail.com"
    }
  }
  ```


## **OTP Verification**

### Summary

- route: `/otp-verification`
- method: `GET`
- request :

  request can be one of the following types:

  ```js
  {
    "query": {
      "token": "${JWT_TOKEN}"
    }
    "params": {
      "otp":"1234"
    }
  }

  ```

- response:

  ```js
  
  {
    "code": 200,
    "body": {
      "token": "${JWT_TOKEN}",
    }
  }
  ```


## **Change Password**

### Summary

- route: `/change-password`
- method: `GET`
- request :

  request can be one of the following types:

  ```js
  {
    "query": {
      "token": "${JWT_TOKEN}"
    }
    "body": {
      "password":"testpassword"
    }
  }

  ```

- response:

  ```js
  
  {
    "code": 200,
    "body": {
      "message": "Password updated successfully."
    }
  }
  ```


## **Email Verification**

### Summary

- route: `/email-verification`
- method: `GET`
- request :

  request can be one of the following types:

  ```js
  {
    "query": {
      "token": "${JWT_TOKEN}"
    }
    "params": {
      "otp":"1234"
    }
  }

  ```

- response:

  ```js
  
  {
    "code": 200,
    "body": {
      "message": "Your email address is verified.",
    }
  }
  ```


## **Get Notification**

### Summary

- route: `/notification`
- method: `GET`

- response:

  ```js
  
  {
    "code": 200,
    "body": {
      "count": 1,
      "next": null,
      "previous": null,
      "results": [
        {
            "id": "${UUID}",
            "notification_type": "applied",
            "application": {
                "id": "${UUID}",
                "shortlisted_at": "2023-04-10T05:22:25",
                "rejected_at": null,
                "short_letter": null,
                "attachments": [],
                "job": {
                    "id": "${UUID}",
                    "title": "Job Title"
                },
                "user": {
                    "id": "${UUID}",
                    "name": "User Name",
                    "image": "/${PATH}"
                }
            },
            "job": null,
            "job_filter": null,
            "seen": false,
            "created": "2023-04-05T06:55:52"
        },
      ]
    }
  }
  ```


## **Save Advanced Filter for User**

### Summary

- route: `/filter`
- method: `POST`
- request:
  ```js
  {
    "query": 
    {
      "title": "test", // show all results
      "country": "${UUID}" || null;, // filter by country
      "city": "${UUID}" || null;, // filter by city
      "category": "${UUID}" || null;, // filter by category
      "category": "${UUID}" || null;, // filter by category
      "is_full_time": true || false || null;, // filter is full time
      "is_part_time": true || false || null;, // filter is part time
      "has_contract": true || false || null;, // filter has contract
      "is_notification": true || false || null;, // filter for availability
      "availability": true || false || null;, // filter for availability
      "salary_min": "3500" || null;, // filter for minimum salary
      "salary_max": "4500" || null;, // filter for maximum salary
    },
  }
 
  ```

- response:

  ```js
  
  {
    "code": 201,
    "body": {
      {
        "id": "${UUID}",
        "title": "first user filter",
        "country": "${UUID}",
        "city": "${UUID}",
        "category": [
            "${UUID}",
            "${UUID}"
        ],
        "is_full_time": false,
        "is_part_time": false,
        "has_contract": false,
        "is_notification": false,
        "salary_min": null,
        "salary_max": null,
        "availability": false
      }
    }
  }
  ```


## **Get Advanced Filter for User**

### Summary

- route: `/filter`
- method: `GET`

- response:

  ```js
  
  {
    "code": 200,
    "body": {
      {
        "id": "${UUID}",
        "title": "first user filter",
        "country":  {
            "id": "${UUID}",
            "title": "India"
        },
        "city":  {
            "id": "${UUID}",
            "title": "Bhopal"
        },
        "category": [
            {
              "id": "${UUID}",
              "title": "category 1"
            },
            {
              "id": "${UUID}",
              "title": "category 2"
            },
        ],
        "is_full_time": false,
        "is_part_time": false,
        "has_contract": false,
        "availability": false,
        "is_notification": false,
        "salary_min": null,
        "salary_max": null
      }
    }
  }
  ```


## **Delete Advanced Filter for User**

### Summary

- route: `/filter`
- method: `DELETE`
- request:

  ```js
  {
    "params": {
  	    "filterId": "${UUID}"
    }
  }
  ```
- response:

  ```js
  
  {
    "code": 200,
    "body": {
      {
        "message": "Filter Removed"
      }
    }
  }
  ```


## **Update Advanced Filter for User**

### Summary

- route: `/filter`
- method: `PUT`
- request:
  ```js
  {
    "params": {
      "filterId": "${UUID}"
    },
    "body": {
      "title": "test", // show all results
      "country": "${UUID}" || null;, // filter by country
      "city": "${UUID}" || null;, // filter by city
      "category": "${UUID}" || null;, // filter by category
      "category": "${UUID}" || null;, // filter by category
      "is_full_time": true || false || null;, // filter is full time
      "is_part_time": true || false || null;, // filter is part time
      "has_contract": true || false || null;, // filter has contract
      "is_notification": true || false || null;, // filter for availability
      "availability": true || false || null;, // filter for availability
      "salary_min": "3500" || null;, // filter for minimum salary
      "salary_max": "4500" || null;, // filter for maximum salary
    },
  }
 
  ```

- response:

  ```js
  
  {
    "code": 201,
    "body": {
      {
        "id": "${UUID}",
        "title": "first user filter",
        "country": "${UUID}",
        "city": "${UUID}",
        "category": [
            "${UUID}",
            "${UUID}"
        ],
        "is_full_time": false,
        "is_part_time": false,
        "has_contract": false,
        "is_notification": false,
        "salary_min": null,
        "salary_max": null,
        "availability": false
      }
    }
  }
  ```

