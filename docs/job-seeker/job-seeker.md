# Job Seeker

These APIs are for the `CRUD` of a job seeker

> **NOTE:** The prefix of every `api`' s stated as `api/v1/user/job-seeker`
>
> **NOTE:** The user’s `id` can be accessed through this `token` only.
>
> **NOTE:** All these API’s are protected and only can be access by the job-seeker.

## Table Of Content

- **[Edit About Me](#edit-about-me)**
- **[Add Education](#add-education)**
- **[Update Education](#update-education)**
- **[Delete Education](#delete-education)**
- **[Add Language](#add-language)**
- **[Update Language](#update-language)**
- **[Delete Language](#delete-language)**
- **[Add Work experience](#add-work-experience)**
- **[Update Work experience](#update-work-experience)**
- **[Delete Work experience](#delete-work-experience)**
- **[Add Skills](#add-skills)**
- **[Add Resume](#add-resume)**
- **[Update Resume](#update-resume)**
- **[Apply for a job](#apply-for-a-job)**
- **[Get Applied jobs](#get-applied-jobs)**
- **[Save a job](#save-a-job)**
- **[Get Saved Jobs](#get-saved-jobs)**
- **[Unsave a job](#unsave-a-job)**
- **[Revoke applied job](#revoke-applied-job)**
- **[Update Job Preferences](#update-job-preferences)**
- **[Get Category for Job Seekers](#get-category-for-job-jeekers)**
- **[Update Category for Job Seekers](#update-category-for-job-seekers)**

## Edit About Me:

### Summary:

From this API `job-seeker` will be able to update only his profile.

- route: `/about-me`
- method: `PATCH`
- request:

  ```js
  {
    "body": {
      "gender": "male" || "female",
      "dob": "YYYY-MM-DD",
      "employment_status": "employed" || "other" || "fresher",
      "description": "This is the description of the user...",
      "market_information_notification": false,
      "job_notification": false,
      "full_name": "Test User"
      "email": "test@test.com"
      "mobile_number": "9900998877"
      "country_code": "+91"
      "highest_education": "${UUID}"
      "country": "${UUID}"
      "city": "${UUID}"
    }
  }
  ```

- response:

  ```js
  {
    "code": 200,
    "data": {
      "message": "Updated Successfully"
    }
  }
  ```

## Add Education:

### Summary:

From this API `job-seeker` will be able to add new education to his profile

- route: `/educations`
- method: `POST`
- request:

  ```js
  {
    "body": {
      "title": "Software Engineer",
      "start_date": "DD/MM/YYYY",
      "end_date": "DD/MM/YYYY" || null,
      "institute": "MIT",
      "education_level": "${UUID}"
    }
  }
  ```

- response:

  ```js
  {
    "code": 201,
    "data": {
      "id": "${UUID}",
      "title": "Software Engineer",
      "start_date": "DD/MM/YYYY",
      "end_date": "DD/MM/YYYY" || null,
      "institute": "MIT",
      "education_level": "${UUID}"
    }
  }
  ```

## Update Education:

### Summary:

From this API `users` can update their Education details

- route: `/educations/:educationId`
- method: `PATCH`
- request:

  ```js
  {
    "params": {
      "educationId": "${UUID}"
    }
    "body": {
      "title": "Software Engineer" || null,
      "start_date": "DD/MM/YYYY" || null,
      "end_date": "DD/MM/YYYY" || null,
      "institute": "MIT" || null,
      "education_level": "${UUID}" || null
    }
  }
  ```

> **NOTE:** _Only those field will be sent that are going to update_

- response:

  ```js
  {
    "code": 200,
    "data": {
      "message": "Updated Successfully"
    }
  }
  ```

## Delete Education:

### Summary:

From this API users can delete their `education` details.

- route: `/educations/:educationId`
- method: `DELETE`
- request:

  ```js
  {
    "params": {
      "educationId": "${UUID}"
    }
  }
  ```

- response:

  ```js
  {
    "code": 200,
    "data": {
      "message": "Deleted Successfully"
    }
  }
  ```

## Add Language:

### Summary:

From this API users can add their `language` details.

- route: `/language`
- method: `POST`
- request:

  ```js
  {
    "language": "${UUID}",
    "written": "basic" || "conversational" || "fluent",
    "spoken": "basic" || "conversational" || "fluent"
  }
  ```

- response:

  ```js
  {
    "code": 201,
    "data": {
      "id": "${UUID}",
      "language": "English",
      "written": "basic" || "conversational" || "fluent",
      "spoken": "basic" || "conversational" || "fluent"
    }
  }
  ```

## Update Language:

### Summary:

From this API users can update their `language` details.

- route: `/languages/:languageId`
- method: `PATCH`
- request:

  ```js
  {
    "params": {
      languageId: "${UUID}"
    },
    "body": {
      "written": "basic" || "conversational" || "fluent",
      "spoken": "basic" || "conversational" || "fluent"
    }
  }
  ```

> **Note:** User can only update `written` and `spoken` fields. If he want to update `language` itself, he can add new `language` and delete current one.
>
> **Note:** Only those `fields` were sent, which need to update.

- response:

  ```js
  {
    "code": 200,
    "data": {
      "message": "Updated Successfully"
    }
  }
  ```

## Delete Language:

### Summary:

From this API users can delete their language

- route: `/languages/:languageId`
- method: `DELETE`
- request:

  ```js
  {
    "params": {
      "languageId": "${UUID}"
    }
  }
  ```

- response:

  ```js
  {
    "code": 200,
    "data": {
      "message": "Deleted Successfully"
    }
  }
  ```

## Add Work Experience:

### Summary:

From this API users can add new work experience.

- route: `/work-experiences`
- method: `POST`
- request:

  ```js
  {
    "body": {
      "title": "Software Engineer",
      "start_date": "DD/MM/YYYY",
      "end_date": "DD/MM/YYYY" || null,
      "organization": MIT,
      "description": "This is the description of the work experience..."
    }
  }
  ```

- response:

  ```js
  {
    "code": 201,
    "data": {
      "id": "${UUID}",
      "title": "Software Engineer",
      "startDate": "DD/MM/YYYY",
      "endDate": "DD/MM/YYYY" || null,
      "present": false,
      "organization": "MIT",
      "description": "This is the description of the work experience..."
    }
  }
  ```

## Update Work Experience:

### Summary:

From this API users can update their existing work experiences.

- route: `/work-experiences/:workExperienceId`
- method: `PATCH`
- request:

  ```js
  {
    "params": {
      "workExperienceId": "${UUID}"
    },
    "body": {
      "description": "This is the new description of the work experience..."
    }
  }
  ```

- response:

  ```js
  {
    "code": 200,
    "data": {
      "message": "Updated Successfully"
    }
  }
  ```

## Delete Work Experience:

### Summary:

From this API users can delete their existing work experiences.

- route: `/work-experiences/:workExperienceId`
- method: `DELETE`
- request:

  ```js
  {
    "params": {
      "workExperienceId": "${UUID}"
    }
  }
  ```

- response:

  ```js
  {
    "code": 200,
    "data": {
      "message": "Deleted Successfully"
    }
  }
  ```

## Add Skills:

### Summary:

From this API users and add new skills to their profile

- route: `/skills`
- method: `POST`
- request:

  ```js
  {
    "body": {
      "skill_remove": ["${UUID}"]
      "skill_add": ["${UUID}"]
    }
  }
  ```

- response:

  ```js
  {
    "code": 200,
    "data": {
      "message": "Skills added."
    }
  }
  ```

## Add Resume

### Summary:

From this API users can add new resume

- route: `/resumes`
- method: `POST`
- request:

  ```js
  {
    "headers": {
      "Content-Type": "multipart/form-data"
    },
    "body": {
      "title": "Resume Title",
      "resume": File // acceptable .docs, .pdf, .docx
    }
  }
  ```

- response:

  ```js
  {
    "code": 200,
    "data": {
      "id": "${UUID}",
      "title":"Resume Title",
      "path": "${FILE_PATH}"
    }
  }
  ```

## Update Resume

### Summary:

From this API users can update their resume

- route: `/resume/:resumeId`
- method: `PATCH`
- request:

  ```js
  {
    "params": {
      "resumeId": "${UUID}"
    },
    "headers": {
      "Content-Type": "multipart/form-data"
    },
    "body": {
      "file": FILE
    }
  }
  ```

- response:

  ```js
  {
    "code": 200,
    "data": {
      "id": "${UUID}",
      "title": "Resume Title",
      "path": "${FILE_PATH}"
    }
  }
  ```

## Apply for a job:

### Summary:

This api is used to apply for a job by job-seeker

- route: `/jobs/apply/:jobId`,
- method: `POST`
- request:
  ```js
  {
    headers: {
      "Content-Type": "multipart/form-data"
    },
    params: {
      jobId: "${UUID}"
    },
    body: {
      shortLetter: "This is the sort letter....",
      attachment: File[],
    }
  }
  ```
- response:
  ```js
  {
    code: 200,
    data: {
      message: "Applied Successfully"
    }
  }
  ```

## Get Applied jobs:

This api is used to get `user`'s applied jobs

- route: `/jobs/apply`
- method: `GET`
- request:
  ```js
  {
    query: {
      order_by: "descending" || "ascending",
      search_by: "expiration" || "salary",
      page: 1,
      limit: 10,
    }
  }
  ```
- response:
  ```js
  {
    code: 200,
    data: {
      appliedJobs: [
        {
          title: "RETAIL ASSISTANT CASHIER",
          description: "Role and Responsibilities - Provide good ...",
          city: "Geldern",
          timing: "5 Day week",
          is_fulltime: true,
          is_part_time: false,
          has_contract: false,
          user: {
            id: "${UUID}",
            display_name: "UTS Marketing Solution Sdn Bhd",
            display_image: "${PATH}"
          },
          budget_currency: "USD",
          budget_amount: 15000,
          budget_pay_period: "yearly" || "quarterly" || "monthly" || "weekly" || "hourly"
          created_at: "2023-01-04T09:56:23.144Z"
        }
      ],
      total: 20, // total number of applied jobs
      current_page: 1,
      current_limit: 10,
    }
  }
  ```

## Save a job:

This api is used to save a `job`

- route: `/jobs/save/:jobId`
- method: `POST`
- request:
  ```
  {
    jobId: "${UUID}"
  }
  ```
- response:
  ```
  {
    code: 200,
    data:{
      message: "Saved Successfully"
    }
  }
  ```

## Get Saved jobs:

This api is used to get `user`'s applied jobs

- route: `/jobs/save`
- method: `GET`
- request:

  ```js
  {
    query: {
      page: 1,
      limit: 10,
    }
  }
  ```
- response:
  ```js
  {
    code: 200,
    data: {
      appliedJobs: [
        {
          title: "RETAIL ASSISTANT CASHIER",
          description: "Role and Responsibilities - Provide good ...",
          city: "Geldern",
          timing: "5 Day week",
          is_fulltime: true,
          is_part_time: false,
          has_contract: false,
          user: {
            id: "${UUID}",
            display_name: "UTS Marketing Solution Sdn Bhd",
            display_image: "${PATH}"
          },
          budget_currency: "USD",
          budget_amount: 15000,
          budget_pay_period: "yearly" || "quarterly" || "monthly" || "weekly" || "hourly"
          created_at: "2023-01-04T09:56:23.144Z"
        }
      ],
      total: 20, // total number of applied jobs
      current_page: 1,
      current_limit: 10,
    }
  }
  ```

## Unsave a job:

This api is used to save a `unsave a job`

- route: `/jobs/save/:jobId`
- method: `DELETE`
- request:
  ```
  {
    jobId: "${UUID}"
  }
  ```
- response:
  ```
  {
    code: 200,
    data:{
      message: "Job Unsaved"
    }
  }
  ```


## Revoke applied job:

This api is used to save a `revoke applied job`

- route: `/jobs/apply/:jobId`
- method: `DELETE`
- request:
  ```
  {
    jobId: "${UUID}"
  }
  ```
- response:
  ```
  {
    code: 200,
    data:{
      message: "Revoked applied job"
    }
  }
  ```


## Update Job Preferences:

This api is used to save a `update job preferences`

- route: `/job-preferences`
- method: `PATCH`
- request:
  ```js
  {
    "body": {
        "is_available":false || true,
        "display_in_search":false || true,
        "is_part_time":false || true,
        "is_full_time":false || true,
        "has_contract":false || true,
        "expected_salary":300000
    }
  }
  ```
- response:
 ```js
  {
    "code": 200,
    "data": {
      "message": "Updated Successfully"
    }
  }
  ```


## Get Category for Job Seekers:

This api is used to save a `get category for job seekers`

- route: `/category`
- method: `GET`

- response:
 ```js
  {
    "code": 200,
    "data": [
        {
            "id": "${UUID}",
            "title": "title 1",
            "sub_category": [
                {
                    "id": "${UUID}",
                    "title": "sub title 1",
                    "status": true
                },
                {
                    "id": "${UUID}",
                    "title": "sub title 2",
                    "status": false
                }
            ]
        },
        {
            "id": "${UUID}",
            "title": "title 2",
            "sub_category": [
                {
                    "id": "${UUID}",
                    "title": "sub title 1",
                    "status": true
                },
                {
                    "id": "${UUID}",
                    "title": "sub title 2",
                    "status": false
                },
                {
                    "id": "${UUID}",
                    "title": "sub title 3",
                    "status": false
                }
            ]
        }
    ]
  }
  ```


## Update Category for Job Seekers:

This api is used to save a `update category for job seekers`

- route: `/category`
- method: `PUT`
- request:
  ```js
  {
    body: {
      "category": ["${UUID}", "${UUID}"]
    }
  }
  ```

- response:
 ```js
  {
    "code": 200,
    "data": [
        {
            "id": "${UUID}",
            "title": "title 1",
            "sub_category": [
                {
                    "id": "${UUID}",
                    "title": "sub title 1",
                    "status": true
                },
                {
                    "id": "${UUID}",
                    "title": "sub title 2",
                    "status": false
                }
            ]
        },
        {
            "id": "${UUID}",
            "title": "title 2",
            "sub_category": [
                {
                    "id": "${UUID}",
                    "title": "sub title 1",
                    "status": true
                },
                {
                    "id": "${UUID}",
                    "title": "sub title 2",
                    "status": false
                },
                {
                    "id": "${UUID}",
                    "title": "sub title 3",
                    "status": false
                }
            ]
        }
    ]
  }
  ```

