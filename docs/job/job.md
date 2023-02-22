# Job

These APIs are for the `CRUD` of a job

> **NOTE:** The prefix of every `api`' s stated as `api/v1/jobs`
>
> **NOTE:** The user’s `id` can be accessed through this `token` only.
>
> **NOTE:** All these API’s are protected and only can be access by the job-seeker.

## Table Of Content

- **[Get Applications](#get-applications)**
- **[Get Recent Applications](#get-recent-applications)**
- **[Get Applications Detail](#get-applications-detail)**


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
