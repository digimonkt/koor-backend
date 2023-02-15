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
- **[Add Languages](#add-language)**
- **[Update Language](#update-language)**
- **[Delete Language](#delete-language)**
- **[Add Work experience](#add-work-experience)**
- **[Update Work experience](#update-work-experience)**
- **[Delete Work experience](#delete-work-experience)**
- **[Add Skill](#add-skills)**
- **[Delete Skill](#delete-skills)**
- **[Add Resume](#add-resume)**
- **[Update Resume](#update-resume)**
- **[Apply for a job](#apply-for-a-job)**
- **[Get Applied jobs](#get-applied-jobs)**
- **[Save a job](#save-a-job)**
- **[Get Saved Jobs](#get-saved-jobs)**

## Edit About Me:

### Summary:

From this API `job-seeker` will be able to update only his profile.

- route: `/about-me`
- method: `PUT`
- request:

  ```js
  {
    "body": {
      "gender": "male" || "female",
      "dob": "YYYY-MM-DD",
      "employmentStatus": "employed" || "fresher" || "other",
      "description": "This is the description of the user...",
      "marketInformation": false,
      "jobNotification": false,
      "fullName": "Test User"
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

## Add Education

### Summary:

From this API `user` will be able to add new education to his profile

- route: `/educations`
- method: `POST`
- request:

  ```js
  {
    "body": {
      "title": "Software Engineer",
      "startDate": "DD/MM/YYYY",
      "endDate": "DD/MM/YYYY" || null,
      "present": false,
      "organization": "MIT",
      "description": "This is the description of the education..."
    }
  }
  ```

- response:

  ```js
  {
    "code": 200,
    "data": {
      "id": "${UUID}",
      "title": "Software Engineer",
      "startDate": "DD/MM/YYYY",
      "endDate": "DD/MM/YYYY" || null,
      "present": false,
      "organization": "MIT",
      "description": "This is the description of the education..."
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
      "description": "This is the new description of the education..."
    }
  }
  ```

> **NOTE:** _Only those field will be sent that are going to update_

- response:

  ```js
  {
    "code": 204,
    "data": {
      "message": "Update Successful"
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
    "code": 204,
    "data": {
      "message": "Deleted Successfully"
    }
  }
  ```

## Add Language:

### Summary:

From this API users can add their `language` details.

- route: `/languages`
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
    "code": 200,
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
      "written": "basic" || "conversational" || "fluent"
    }
  }
  ```

> **Note:** User can only update `written` and `spoken` fields. If he want to update `language` itself, he can add new `language` and delete current one.
>
> **Note:** Only those `fields` were sent, which need to update.

- response:

  ```js
  {
    "code": 204,
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
    "code": 204,
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
      "startDate": "DD/MM/YYYY",
      "endDate": "DD/MM/YYYY" || null,
      "present": false,
      "organization": "MIT",
      "description": "This is the description of the work experience..."
    }
  }
  ```

- response:

  ```js
  {
    "code": 200,
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

## Update Work Experience

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
    "code": 204,
    "data": {
      "message": "Updated Successfully"
    }
  }
  ```

## Delete Work Experience

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
    "code": 204,
    "data": {
      "message": "Deleted Successfully"
    }
  }
  ```

## Add Skills

### Summary:

From this API users and add new skills to their profile

- route: `/skills/:originalSkillId`
- method: `POST`
- request:

  ```js
  {
    "params": {
      "originalSkillId": "${UUID}"
    }
  }
  ```

- response:

  ```js
  {
    "code": 200,
    "data": {
      "id": ${UUID},
      "title": "Software Engineer"
    }
  }
  ```

## Delete Skills

### Summary:

From this API users can delete their existing skills

- route: `/skills/:skillId`
- method: `DELETE`
- request:

  ```js
  {
    "params": {
      "skillId": "${UUID}"
    }
  }
  ```

- response:

  ```js
  {
    "code": 204,
    "data": {
      "message": "Deleted Successfully"
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

## Apply for a job

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

## Get Applied jobs

This api is used to get `user`'s applied jobs

- route: `/jobs/apply`
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

## Save a job

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

## Get Saved jobs

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

## Get Jobs Search

This api is used to get all the `jobs search` of the employer.
- route: `/job-search`
- method: `GET`
- request:
  ```js
    // type one
  {
    "query": 
    {
      "search": "", // show all results
      "limit": "1" || null;, // page limit
      "page": "1" || null;, // page number
    },
  }
 

  // type two
  {
    "query": 
    {
      "search": "b", // show only those results whose title includes `b` only
      "limit": "1" || null;, // page limit
      "page": "1" || null;, // page number
    },
  }

  ```
- response:
  ```js
  {
    code: 200,
    data: [{
      id: "${UUID}",
      title: "Retail Assistant Cashier",
      description: "This is the description of job...",
      budget_currency: "$",
      budget_amount: 3500,
      budget_pay_period: "UP TO",
      country: "India",
      city: "Gwalior",
      is_fulltime: true,
      is_partime: false,
      has_contract: false,
      working_days: "1" || "2" || "3" || "4" || "5" || "6" || "7",
      status: "active" || "inactive" || "hold",
      user: {...userDetails} // full user details
    }]
  }
  ```
