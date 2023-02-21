# Job

These APIs are for the `CRUD` of a job

> **NOTE:** The prefix of every `api`' s stated as `api/v1/jobs`
>
> **NOTE:** The user’s `id` can be accessed through this `token` only.
>
> **NOTE:** All these API’s are protected and only can be access by the job-seeker.

## Table Of Content

- **[Get Applicaitons](#get-applicaitons)**


## Get Applicaitons:

### Summary:

From this API get Applicaitons of any Jobs.

- route: `/applicaitons/:jobId`
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
    "code": 204,
    "data": [
                {
                    "id": "${UUID}",
                    "shortlisted_at": null,
                    "rejected_at": null,
                    "created": "2023-02-20T17:16:11",
                    "short_letter": "This is the short letter of the applicaitons...",
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
