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
      "dob": "DD/MM/YYYY",
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
