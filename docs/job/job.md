# Job

These APIs are for the `CRUD` of a job

> **NOTE:** The prefix of every `api`' s stated as `api/v1/jobs`
>
> **NOTE:** The user’s `id` can be accessed through this `token` only.
>
> **NOTE:** All these API’s are protected and only can be access by the job-seeker.

## Table Of Content

- **[Get Jobs Search](#get-jobs-search)**
- **[Get Applications](#get-applications)**
- **[Get Recent Applications](#get-recent-applications)**
- **[Get Applications Detail](#get-applications-detail)**
- **[Modify Applications](#modify-applications)**



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
    "params": {
      "jobId": "${UUID}"
    },
  }
  ```

- response:

  ```js
  {
    "code": 200,
    "data": [
                {
                    "id": "${UUID}",
                    "shortlisted_at": null,
                    "rejected_at": null,
                    "created": "2023-02-20T17:16:11",
                    "short_letter": "This is the short letter of the applications...",
                    "user": 
                    {
                        ...
                    },
                    "education": true,
                    "language": true,
                    "skill": true
                }
            ]
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
                      "shortlisted_at": null,
                      "rejected_at": null,
                      "created": "2023-02-20T17:16:11",
                      "short_letter": "This is the short letter of the applications...",
                      "user": 
                      {
                          ...
                      },
                      "education": true,
                      "language": true,
                      "skill": true
                    }
                  ]
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
              "shortlisted_at": null,
              "rejected_at": null,
              "short_letter": "second time apply job in another jobs title.",
              "attachments": [
                              {
                                "id": "${UUID}",
                                "path": "file_path",
                                "title": "file_title",
                                "type": "file_type"
                              },
                            ],
                "job": {
                        ...
                        }
              }
  }
  ```

## Modify Applications:

### Summary:

From this API Modify Applications of any Jobs.

- route: `/applications-detail/:applicationId`
- method: `PATCH`
- request:

  ```js
  {
    "params": {
      "applicationId": "${UUID}"
    },
    "body":{
      "action":"shortlisted" || "rejected" || "blacklisted"
    }
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
