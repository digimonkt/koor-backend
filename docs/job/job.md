# Job

These APIs are for the `CRUD` of a job

> **NOTE:** The prefix of every `api`' s stated as `api/v1/jobs`
>
> **NOTE:** The user’s `id` can be accessed through this `token` only.
>
> **NOTE:** All these API’s are protected and only can be access by the job-seeker.

## Table Of Content

- **[Get Jobs Search](#get-jobs-search)**
- **[Get Jobs Detail](#get-jobs-detail)**
- **[Get Applications](#get-applications)**
- **[Get Recent Applications](#get-recent-applications)**
- **[Get Applications Detail](#get-applications-detail)**
- **[Modify Applications](#modify-applications)**
- **[Get Job Suggestion](#get-job-suggestion)**
- **[Save Job Filter](#save-job-filter)**
- **[Get Job Filter](#get-job-filter)**
- **[Delete Job Filter](#delete-job-filter)**



## Get Jobs Search

This api is used to get all the `jobs search` of the employer.
- route: ` `
- method: `GET`
- request:
  ```js
    // type one
  {
    "query": 
    {
      "search": "", // show all results
      "country": "india" || null;, // filter by country
      "city": "delhi" || null;, // filter by city
      "fullTime": true || false || null;, // filter is full time
      "partTime": true || false || null;, // filter is part time
      "contract": true || false || null;, // filter has contract
      "jobCategory": [ ] || null;, // filter by job category
      "timing": "1" || "2" || "3" || "4" || "5" || "6" || "7" || null;, // filter for working days
      "salary_min": "3500" || null;, // filter for minimum salary
      "salary_max": "4500" || null;, // filter for maximum salary
      "limit": "1" || null;, // page limit
      "page": "1" || null;, // page number
    },
  }
 

  // type two
  {
    "query": 
    {
      "search": "b", // show only those results whose title includes `b` only
      "country": "india" || null;, // filter by country
      "city": "delhi" || null;, // filter by city
      "fullTime": true || false || null;, // filter is full time
      "partTime": true || false || null;, // filter is part time
      "contract": true || false || null;, // filter has contract
      "jobCategory": [ ] || null;, // filter by job category
      "timing": "1" || "2" || "3" || "4" || "5" || "6" || "7" || null;, // filter for working days
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


## Get Jobs Detail

This api is used to get all the `get jobs detail` of the employer.
- route: `/:jobId`
- method: `GET`
- request:
  ```js
    // type one
  {
    params: {
      jobId: "${UUID}"
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


## Get Applications:

### Summary:

From this API get Applications of any Jobs.

- route: `/applications/:jobId`
- method: `GET`
- request:

  ```js
  {
    "query": {
      "filter": "rejected" || "shortlisted"|| "planned_interviews"|| "blacklisted"
    }
    "params": {
      "jobId": "${UUID}"
    },
  }
  ```

- response:

  ```js
  {
    "code": 200,
    "data": {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": "${UUID}",
                "shortlisted_at": "2023-04-10T05:22:25",
                "rejected_at": "2023-04-11T10:48:07",
                "created": "2023-04-05T06:55:52",
                "short_letter": "",
                "user": {
                    ....
                },
                "education": false,
                "language": false,
                "skill": false,
                "job": {
                    ....
                }
            }
        ],
        "rejected_count": 1,
        "shortlisted_count": 3,
        "planned_interview_count": 0,
        "blacklisted_count": 0
      }
  }
  ```

## Get Recent Applications:

### Summary:

From this API Get Recent Applications of any Jobs.

- route: `/applications`
- method: `GET`

- response:

  ```js
  {
    "code": 200,
    "data": {
              "count": 1,
              "next": null,
              "previous": null,
              "results": [
                  {
                    "id": "${UUID}",
                    "shortlisted_at": "2023-04-10T05:22:25",
                    "rejected_at": "2023-04-11T10:48:07",
                    "created": "2023-04-05T06:55:52",
                    "short_letter": "",
                    "user": {
                        ....
                    },
                    "education": false,
                    "language": false,
                    "skill": false,
                    "job": {
                        ....
                    }
                }
              ],
      }
  }
  ```

## Get Applications Detail:

### Summary:

From this API Get Applications Detail of any Jobs.

- route: `/applications-detail/:applicationId`
- method: `GET`
- request:

  ```js
  {
    "params": {
      "applicationId": "${UUID}"
    },
  }
  ```

- response:

  ```js
  {
    "code": 200,
    "data": {
        "id": "${UUID}",
        "shortlisted_at": "2023-03-27T13:17:44",
        "rejected_at": null,
        "short_letter": null,
        "created": "2023-03-17T10:20:28",
        "attachments": [],
        "job": {
            ....
        },
        "user": {
            ....
        }
    }
  }
  ```

## Modify Applications:

### Summary:

From this API Modify Applications of any Jobs.

- route: `/applications-detail/:applicationId/:action`
- method: `PUT`
- request:

  ```js
  {
    "params": {
      "applicationId": "${UUID}",
      "action":"shortlisted" || "rejected" || "blacklisted"
    },
  }
  ```

- response:

  ```js
  {
    "code": 200,
    "data": {
             "message": "Successfully shortlisted"
            }
  }
  ```

## Get Job Suggestion:

### Summary:

From this API get suggested jobs.

- route: `/:jobId/suggestion`
- method: `GET`
- request:

  ```js
  {
    "params": {
      "jobId": "${UUID}"
    },
  }
  ```

- response:

  ```js
  {
    "code": 200,
    "data": {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": "${UUID}",
                "title": "test title",
                "description": "this is testing job profile",
                "budget_currency": "usd",
                "budget_amount": "100.00",
                "budget_pay_period": "hourly",
                "country": {
                    ....
                },
                "city": {
                    ....
                },
                "is_full_time": true,
                "is_part_time": true,
                "has_contract": true,
                "working_days": "6",
                "status": "active",
                "applicant": 3,
                "deadline": "2035-01-31",
                "start_date": "2023-04-01",
                "created": "2023-03-17T10:18:06",
                "is_applied": false,
                "is_saved": false,
                "user": {
                    ....
                }
            }
        ]
    }
  }
  ```

## Save Job Filter:

### Summary:

From this API save job filters.

- route: `/filter`
- method: `POST`
- request:

  ```js
  {
    "body":{
        "title": "a",
        "city": "${UUID}",
        "country": "${UUID}",
        "job_category": ["${UUID}"],
        "is_full_time": true || false || null
        "is_part_time": true || false || null
        "has_contract": true || false || null
        "is_notification": true || false || null
        "working_days": 1 || 2 || 3 || 4 || 5 || 6 || 7
    }
  }
  ```

- response:

  ```js
  {
    "code": 201,
    "data": {
        "id": "accf2781-687e-4660-9f22-6eb49e08e2fa",
        "title": "a",
        "country": "d66842b7-dbc5-4da8-b1d9-fd0b1989ce0a",
        "city": "1c3feef3-0d8c-4e4d-9e6b-c0e85dcf8a49",
        "job_category": [],
        "is_full_time": null,
        "is_part_time": null,
        "has_contract": null,
        "is_notification": null,
        "working_days": "5"
    }
  }
  ```

## Get Job Filter:

### Summary:

From this API get job filters.

- route: `/filter`
- method: `GET`

- response:

  ```js
  {
    "code": 200,
    "data": [
        {
            "id": "${UUID}",
            "title": "a",
            "country": {
                "id": "${UUID}",
                "title": "India"
            },
            "city": {
                "id": "${UUID}",
                "title": "Bhopal"
            },
            "job_category": [],
            "is_full_time": null,
            "is_part_time": null,
            "has_contract": null,
            "is_notification": null,
            "working_days": "5"
        }
    ]
  }
  ```

## Delete Job Filter:

### Summary:

From this API delete any job filters.

- route: `/filter/:filterId`
- method: `DELETE`
- request:

  ```js
  {
    "params":{
        "filterId": "${UUID}"
    }
  }
  ```

- response:

  ```js
  {
    "code": 200,
    "data": {
        "message": "Filter Removed"
    }
  }
  ```
