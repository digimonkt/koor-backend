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
      "organization_name": "Digimonk Technologies",
      "organization_type": "business" || "ngo" || "government",
      "mobile_number": "1234567890",
      "country_code": "+91",
      "market_information_notification":true,
      "other_notification":true,
      "license_id": "LAS001TA",
      "license": File
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
      jobCategory: ["${jobCategoryId}"],
      isFulltime: true,
      isPartime: false,
      hasContract: false,
      contactEmail: "saral.shrivastava@digimonk.in",
      contactPhone: null,
      contactWhatsapp: null,
      highestEducation: "${educationLevelId}",
      language: [{"language":"${languageId}","spoken":"fluent","written":"conversational"}],
      skill: ["${skillId}"],
      working_days: "1" || "2" || "3" || "4" || "5" || "6" || "7",
      attachments: [File],
      deadline: "YYYY-MM-DD"
      start_date: "YYYY-MM-DD"
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
    // type one
  {
    "query": 
    {
      "employerId": "${UUID}" || null;,
      "search": "", // show all results
      "limit": "1" || null;, // page limit
      "page": "1" || null;, // page number
    },
  }
 

  // type two
  {
    "query": 
    {
      "employerId": "${UUID}" || null;,
      "search": "b", // show only those results whose title includes `b` only
      "limit": "1" || null;, // page limit
      "page": "1" || null;, // page number
    },
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
      working_days: "1" || "2" || "3" || "4" || "5" || "6" || "7",
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
      jobCategory: ["${jobCategoryId}"],
      isFulltime: true,
      isPartime: false,
      hasContract: false,
      contactEmail: "saral.shrivastava@digimonk.in",
      contactPhone: null,
      contactWhatsapp: null,
      highestEducation: "${educationLevelId}",
      language: [
        '{"language":"${languageId}","spoken":"fluent","written":"conversational"}' || 
        '{"id":"${UUID}","language":"${languageId}","spoken":"fluent","written":"conversational"}' 
        ],
      language_remove: ["${UUID}"],
      skill: ["${skillId}"],
      start_date: "YYYY-MM-DD"
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
