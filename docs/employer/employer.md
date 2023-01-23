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
      "organizationName": "Digimonk Technologies",
      "typeOfOrganization": "business" || "ngo" || "government",
      "mobileNumber": "1234567890",
      "countryCode": "+91",
      "licenseId": "LAS001TA",
      "license": File
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
      budgetCurrency: "USD",
      budgetAmount: 2000,
      budgetPayPeriod: "yearly",
      description: "This is the job description...",
      country: "${countryId}",
      city: "${cityId}",
      address: "Gwalior, Madhya Pradesh",
      jobCategory1: "${jobCategoryId}",
      jobCategory2: "${jobCategoryId}" || null,
      jobCategory3: "${jobCategoryId}" || null,
      isFulltime: true,
      isPartime: false,
      hasContract: false,
      contactEmail: "saral.shrivastava@digimonk.in",
      contactPhone: null,
      contactWhatsapp: null,
      highestEducation: "${educationLevelId}",
      language1: "${languageId}",
      language2: "${languageId}" || null,
      language3: "${languageId}" || null,
      skill1: "${skillId}",
      skill2: "${skillId}" || null,
      skill3: "${skillId}" || null,
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
    body: {
      title: "Senior Software Developer",
      budgetCurrency: "USD",
      budgetAmount: 2000,
      budgetPayPeriod: "yearly",
      description: "This is the job description...",
      country: "${countryId}",
      city: "${cityId}",
      address: "Gwalior, Madhya Pradesh",
      jobCategory1: "${jobCategoryId}",
      jobCategory2: "${jobCategoryId}" || null,
      jobCategory3: "${jobCategoryId}" || null,
      isFulltime: true,
      isPartime: false,
      hasContract: false,
      contactEmail: "saral.shrivastava@digimonk.in",
      contactPhone: null,
      contactWhatsapp: null,
      highestEducation: "${educationLevelId}",
      language1: "${languageId}",
      language2: "${languageId}" || null,
      language3: "${languageId}" || null,
      skill1: "${skillId}",
      skill2: "${skillId}" || null,
      skill3: "${skillId}" || null,
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
