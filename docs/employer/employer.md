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
- **[Create Tenders](#create-tenders)**
- **[Get Tenders](#get-tenders)**
- **[Update Tenders](#update-tenders)**
- **[Active Inactive Job](#active-inactive-job)**
- **[Active Inactive Tender](#active-inactive-tender)**
- **[Dashboard Activity](#dashboard-activity)**

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
      budget_currency: "USD",
      budget_amount: 2000,
      budget_pay_period: "yearly",
      description: "This is the job description...",
      country: "${countryId}",
      city: "${cityId}",
      address: "Gwalior, Madhya Pradesh",
      job_category: ["${jobCategoryId}"],
      is_full_time: true,
      is_part_time: false,
      has_contract: false,
      contact_email: "saral.shrivastava@digimonk.in",
      contact_phone: null,
      contact_whatsapp: null,
      highest_education: "${educationLevelId}",
      language: [{"language":"${languageId}","spoken":"fluent","written":"conversational"}],
      skill: ["${skillId}"],
      duration: 20,
      experience: 3,
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
      duration: 20,
      experience: 3,
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
      budget_currency: "USD",
      budget_amount: 2000,
      budget_pay_period: "yearly",
      description: "This is the job description...",
      country: "${countryId}",
      city: "${cityId}",
      address: "Gwalior, Madhya Pradesh",
      job_category: ["${jobCategoryId}"],
      is_full_time: true,
      is_part_time: false,
      has_contract: false,
      contact_email: "saral.shrivastava@digimonk.in",
      contact_phone: null,
      contact_whatsapp: null,
      highest_education: "${educationLevelId}",
      language: [
        '{"language":"${languageId}","spoken":"fluent","written":"conversational"}' || 
        '{"id":"${UUID}","language":"${languageId}","spoken":"fluent","written":"conversational"}' 
        ],
      language_remove: ["${UUID}"],
      skill: ["${skillId}"],
      duration: 20,
      experience: 3,
      attachments: [File],
      attachments_remove: ["${UUID}"],
      deadline: "YYYY-MM-DD",
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

## Create Tenders

This route is used to create `tenders`

- route: `/tenders`
- method: `POST`
- request:

  ```js
  {
    body: {
      tender_category: ["${tenderCategoryId}"],
      tag: ["${tagId}"],
      attachments: [File],
      title: "test title",
      budget_currency: "USD",
      budget_amount: 2000,
      description: "This is the tenders description...",
      country: "${countryId}",
      city: "${cityId}",
      address: "Gwalior, Madhya Pradesh",
      tender_type: "government" || "ngo" || "business" ,
      sector: "ngo" || "private" || "public",
      deadline: "yyyy-mm-dd",
      start_date: "yyyy-mm-dd"
    }
  }
  ```

- response:
  ```js
  {
    code: 201,
    data: {
      message: "Tender added successfully."
    }
  }
  ```

## Get Tenders

This api is used to get all the `tenders` of the employer.
- route: `/tenders`
- method: `GET`
- request:
  ```js
  {
    "query": {
      "employerId": "${UUID}" || null
    }
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
              "id": "${UUID}",
              "title": "test data",
              "description": null,
              "tender_category": [
                  {
                      "id": "${UUID}",
                      "title": "Auduting"
                  }
              ],
              "sector": "ngo",
              "created": "2023-04-11T16:13:21",
              "is_applied": false,
              "is_saved": false,
              "user": {
                  "id": "${UUID}",
                  "name": "TCS",
                  "email": "test@email.com",
                  "country_code": "+91",
                  "mobile_number": "9988990099",
                  "image": null,
                  "description": null
              },
              "vendor": 0,
              "status": "active"
          }
      ]
    }
  }
  ```

## Update Tenders

This api is used to update existing `tenders`

- route: `/tenders`
- method: `PUT`
- request:

  ```js
  {
    params: {
      "tendersId": "${UUID}",
    },
    body: {
      tender_category: ["${tenderCategoryId}"],
      tag: ["${tagId}"],
      attachments: [File],
      title: "test title",
      budget_currency: "USD",
      budget_amount: 2000,
      description: "This is the tenders description...",
      country: "${countryId}",
      city: "${cityId}",
      address: "Gwalior, Madhya Pradesh",
      tender_type: "government" || "ngo" || "business" ,
      sector: "ngo" || "private" || "public",
      deadline: "yyyy-mm-dd",
      start_date: "yyyy-mm-dd"
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

## Active Inactive Job

This route is used to active inactive `jobs`

- route: `/jobs/:jobId/status`
- method: `PUT`
- request:

  ```js
  {
    params: {
      "jobId": "${UUID}",
    },
  }
  ```

- response:
  ```js
  {
    code: 200,
    data: {
      message: "This job is active" || "This job placed on hold"
    }
  }
  ```

## Active Inactive Tender

This route is used to active inactive `tenders`

- route: `/tenders/:tendersId/status`
- method: `PUT`
- request:

  ```js
  {
    params: {
      "tendersId": "${UUID}",
    },
  }
  ```

- response:
  ```js
  {
    code: 200,
    data: {
      message: "This tender placed on hold" || "This tender is active"
    }
  }
  ```

## Dashboard Activity

This api is used to get count of `activity` for employer dashboard.
- route: `/activity`
- method: `GET`

- response:
  ```js
  {
    code: 200,
    data: {
        "active_jobs": 6,
        "active_tender": 2,
        "applied_jobs": 4,
        "applied_tender": 0
    }
  }
  ```

## Dashboard Job Analysis

This api is used to get count of `job analysis` for employer dashboard.
- route: `/job-analysis`
- method: `GET`

- response:
  ```js
  {
    code: 200,
    data: {
        "order_counts": [
            {
                "month": "YYYY-MM-DD HH:mm:ss",
                "count": 2
            },
            {
                "month": "YYYY-MM-DD HH:mm:ss",
                "count": 9
            }
        ]
    }
  }
  ```
