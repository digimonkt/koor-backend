# Employer

These APIs are for the `CRUD` of an `employer`

> **NOTE:** The prefix of every `api`' s stated as `api/v1/user/employer`
>
> **NOTE:** The user’s `id` can be accessed through this `token` only.
>
> **NOTE:** All these API’s are protected and only can be access by the employer.

## Table Of Content

- **[Update About](#update-about)**
- **[Create Job](#create-job)**
- **[Get Job](#get-jobs)**
- **[Update Job](#update-job)**

## Update About

### Summary

This API is used to update `employer`'s about section

- route: `/about-me`
- method: `PATCH`
- request:

  ```js
  {
    "headers": {
      "Content-Type": "multipart/form-data"
    },
    "body": {
      "name": "Digimonk Technologies",
      "organization_type": "business" || "ngo" || "government",
      "mobile_number": "1234567890",
      "country_code": "+91",
      "license_id": "LAS001TA",
      "license_id_file": File
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

## Create Job

This route is used to create `jobs`

- route: `/jobs`
- method: `POST`
- request:

  ```js
  {
    body: {
      title: "Senior Software Developer",
      budget_currency: "USD",
      budget_amount: 2000,
      budget_pay_period: "yearly" || "quarterly" || "monthly" || "weekly" || "hourly",
      description: "This is the job description...",
      country: "${countryId}",
      city: "${cityId}",
      address: "Gwalior, Madhya Pradesh",
      job_category_1: "${jobCategoryId}",
      job_category_2: "${jobCategoryId}" || null,
      is_full_time: true,
      is_part_time: false,
      has_contract: false,
      contact_email: "saral.shrivastava@digimonk.in",
      contact_phone: null,
      contact_whatsapp: null,
      highest_education: "${educationLevelId}",
      language_1: "${languageId}",
      language_2: "${languageId}" || null,
      language_3: "${languageId}" || null,
      skill_1: "${skillId}",
      skill_2: "${skillId}" || null,
      skill_3: "${skillId}" || null,
      attachments: [File]
    }
  }
  ```

- response:
  ```js
  {
    code: 200,
    data: {
      message: "Job Added successfully"
    }
  }
  ```

## Get Jobs

This api is used to get all the `jobs` of the employer.

- route: `/jobs`
- method: `GET`
- request:
  ```js
  {
    query: {
      employerId: "${UUID}" || null;
    }
  }
  ```
  > Note: If `employerId` is present in query then return that `employer`'s jobs list else current `employer`'s job list.
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
      working_days: "1" || "2" || "3" || "4" || "5" || "6" || "7"
      status: "active" || "inactive" || "hold",
      user: {...userDetails} // full user details
    }]
  }
  ```

## Update Job

This `api` is used to update existing job

- route: `jobs/:jobId`
- method: `PUT`
- request:
  ```js
  {
    headers: {
      "Content-Type": "multipart/form-data"
    },
    body: {
      title: "Senior Software Developer",
      budget_currency: "USD",
      budget_amount: 2000,
      budget_pay_period: "yearly" || "quarterly" || "monthly" || "weekly" || "hourly",
      description: "This is the job description...",
      country: "${countryId}",
      city: "${cityId}",
      address: "Gwalior, Madhya Pradesh",
      job_category_1: "${jobCategoryId}",
      job_category_2: "${jobCategoryId}" || null,
      is_full_time: true,
      is_part_time: false,
      has_contract: false,
      contact_email: "saral.shrivastava@digimonk.in",
      contact_phone: null,
      contact_whatsapp: null,
      highest_education: "${educationLevelId}",
      language_1: "${languageId}",
      language_2: "${languageId}" || null,
      language_3: "${languageId}" || null,
      skill_1: "${skillId}",
      skill_2: "${skillId}" || null,
      skill_3: "${skillId}" || null,
      attachments: [File]
    }
  }
  ```
- response:
  ```js
  {
    code: 200,
    data: {
      message: "Updated Successfully"
    }
  }
  ```
