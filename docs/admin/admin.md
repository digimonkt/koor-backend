# Admin

> **Note:** All `api`'s prefix with `api/v1/admin`

> **Note:** All api's will be Protected and can only be accessed by `admin`

> **Note: All `GET` api's can be access by any `role`**

> **Note:** In database we are going to update flag `deleted` to `true` to delete the tag, we are not actually deleting the `document` from table

## Table Of Content

- [Admin](#admin)
  - [Table Of Content](#table-of-content)
  - [Create Tag](#create-tag)
  - [Get Tags](#get-tags)
  - [Delete Tags](#delete-tags)
  - [Create Language](#create-language)
  - [Get Languages](#get-languages)
  - [Delete Language](#delete-language)
  - [Create Skills](#create-skills)
  - [Get Skills](#get-skills)
  - [Delete Skills](#delete-skills)
  - [Create Education Level](#create-education-level)
  - [Get Education Level](#get-education-level)
  - [Delete Education Level](#delete-education-level)
  - [Create Country](#create-country)
  - [Get Country](#get-country)
  - [Delete Countries](#delete-countries)
  - [Create City](#create-city)
  - [Get City](#get-city)
  - [Delete Cities](#delete-cities)
  - [Create Job Category](#create-job-category)
  - [Get Job Category](#get-job-category)
  - [Delete Job Categories](#delete-job-categories)
  - [Get Users Count](#get-users-count)
  - [Get Credit](#get-credit)
  - [Get Dashboard](#get-dashboard)
  - [Get Jobs List](#get-jobs-list)
  - [Delete Jobs](#delete-jobs)
  - [Restored Job](#restored-job)
  - [Active Inactive Jobs](#active-inactive-jobs)
  - [Get Employers List](#get-employers-list)
  - [Get Candidates List](#get-candidates-list)
  - [Delete Users](#delete-users)
  - [Inactive Users](#inactive-users)
  - [Get User Rights](#get-user-rights)
  - [Update User Rights](#update-user-rights)
  - [Get Privacy Policy](#get-privacy-policy)
  - [Update Privacy Policy](#update-privacy-policy)
  - [Change Password](#change-password)
  - [Create Job Seekers Category](#create-job-seekers-category)
  - [Get Job Seekers Category](#get-job-seekers-category)
  - [Delete Job Seekers Category](#delete-job-seekers-category)
  - [Create Tender Category](#create-tender-category)
  - [Get Tender Category](#get-tender-category)
  - [Delete Tender Category](#delete-tender-category)
  - [Create Sectors](#create-sectors)
  - [Get Sectors](#get-sectors)
  - [Delete Sector](#delete-sector)

## Create Tag

This API is used to create `tags`.

- route: `/tag`
- method: `POST`
- request:
  ```js
  {
    "body": {
      "title": "Backend"
    }
  }
  ```
- response:
  ```js
  {
    "code": 201,
    "data": {
      "id": "${UUID}",
      "title": "Backend"
    }
  }
  ```

## Get Tags

This api is used to get all `tags`

- route: `/tag`
- method: `GET`
- request:

  ```js
  // type one
  {
    "query": {
      "search": "" // show all results
      "page": 1,
      "limit": 10,
    },
  }

  // type two
  {
    "query": {
      "search": "b" // show only those results whose title includes `b` only
      "page": 1,
      "limit": 10,
    },
  }
  ```

- response:
  ```js
  {
    "code": 200,
    "data": {
      "count": 200, // total number of skills available
      "next": "${NEXT_PAGE_PATH}",
      "previous": "${PREVIOUS_PAGE_PATH}",
      "results": [{
        "id": "${UUID}"
        "title": "Backend"
      }],

    }
  }
  ```

## Delete Tags

This api is used to `delete` tag

- route: `/tag/:tagId`
- method: `DELETE`
- request:
  ```js
  {
    "params": {
      "tagId": ["${tagId}"]
    }
  }
  ```
- response:
  ```js
  {
    "code": 200,
    "data": {
      "message": "Deleted Successfully"
    }
  }
  ```

## Create Language

This api is used to create language by admin for the `job-seeker` and `job-details`

- route: `/language`
- method: `POST`
- request:
  ```js
  {
    "body": {
      "title": "Hindi"
    }
  }
  ```
- response:
  ```js
  {
    "code": 201,
    "data": {
      "id": "${UUID}",
      "title": "Hindi"
    }
  }
  ```

## Get Languages

This api is used get list of `languages`

- route: `/languages`
- method: `GET`
- request:

  ```js
  // type one
  {
    "query": {
      "search": "" // show all results
      "page": 1,
      "limit": 10
    },
  }

  // type two
  {
    "query": {
      "search": "b" // show only those results whose title includes `b` only
      "page": 1,
      "limit": 10,
    },
  }
  ```

- response:
  ```js
  {
    "code": 200,
    "data": {
      "count": 200, // total number of skills available
      "next": "${NEXT_PAGE_PATH}",
      "previous": "${PREVIOUS_PAGE_PATH}",
      "results": [{
        "id": "${UUID}"
        "title": "Backend"
      }],
    }
  }
  ```

## Delete Language

This api is used to delete `language`.

- route: `/language/:languageId`
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
    "code": 200,
    "data": {
      "message": "Deleted Successfully"
    }
  }
  ```

## Create Skills

- route: `/skills`
- method: `POST`
- request:
  ```js
  {
    "body": {
      "title": "Python"
    }
  }
  ```
- response:
  ```js
  {
    "code": 201,
    "data": {
      "id": "${UUID}",
      "title": "Python"
    }
  }
  ```

## Get Skills

- route: `/skills`
- method: `GET`
- request:

  ```js
  // type one
  {
    "query": {
      "search": "" // show all results
      "page": 1,
      "limit": 10
    },
  }

  // type two
  {
    "query": {
      "title": "p" // show only those results whose title includes `p` only
      "page": 1,
      "limit": 10
    },
  }
  ```

- response:
  ```js
  {
    "code": 200,
    "data": {
      "count": 200,
      "next": "${NEXT_PAGE_PATH}",
      "previous": "${PREVIOUS_PAGE_PATH}",
      "results": [{
        "id": "${UUID}"
        "title": "Python"
      }],
    }
  }
  ```

## Delete Skills

- route: `/skills/:skillId`
- method: `DELETE`
- request:
  ```js
  {
    "query": {
      "skillId": "${UUID}"
    }
  }
  ```
- response:
  ```js
  {
    "code": 200,
    "data": {
      "message": "Deleted Successfully"
    }
  }
  ```

## Create Education Level

- route: `/education-level`
- method: `POST`
- request:
  ```js
  {
    "body": {
      "title": "Bachelors"
    }
  }
  ```
- response:
  ```js
  {
    "code": 200,
    "data": {
      "id": "${UUID}",
      "title": "Bachelors"
    }
  }
  ```

## Get Education Level

- route: `/education-level`
- method: `GET`
- request:

  ```js
  // type one
  {
    "query": {
      "search": "" // show all results
      "page": 1,
      "limit": 10
    },
  }

  // type two
  {
    "query": {
      "search": "b" // show only those results whose title includes `p` only
      "page": 1,
      "limit": 10
    },
  }
  ```

- response:
  ```js
  {
    "code": 200,
    "data": {
      "count": 200,
      "next": "${NEXT_PAGE_PATH}",
      "previous": "${PREVIOUS_PAGE_PATH}",
      "results": [{
        "id": "${UUID}"
        "title": "Bachelors"
      }],
    }
  }
  ```

## Delete Education Level

- route: `/education-level/:educationLevelId`
- method: `DELETE`
- request:
  ```js
  {
    "query": {
      "educationLevelId": "${UUID}"
    }
  }
  ```
- response:
  ```js
  {
    "code": 200,
    "data": {
      "message": "Deleted Successfully"
    }
  }
  ```


## Create Country

This API is used to create `country`.

- route: `/country`
- method: `POST`
- request:
  ```js
  {
    "body": {
      "title": "Russia",
      "currency_code":"RUR",
      "country_code":"+7",
      "iso_code2":"test iso 2",
      "iso_code3":"test iso 3"
    }
  }
  ```
- response:
  ```js
  {
    "code": 201,
    "data": {
      "id": "${UUID}",
      "title": "Nepal1",
      "currency_code": "NPR",
      "country_code": "+977",
      "iso_code2": "test iso 2",
      "iso_code3": "test iso 3"
    }
  }
  ```

## Get Country

This api is used to get all `countries`

- route: `/country`
- method: `GET`
- request:

  ```js
  // type one
  {
    "query": 
    {
      "search": "" // show all results
      "page": 1,
      "limit": 10
    },
  }
 

  // type two
  {
    "query": 
    {
      "search": "b" // show only those results whose title includes `b` only
      "page": 1,
      "limit": 10
    },
  }

  ```

- response:
  ```js
  {
    "code": 200,
    "data": {
      "count": 200,
      "next": "${NEXT_PAGE_PATH}",
      "previous": "${PREVIOUS_PAGE_PATH}",
      "results": [{
        "id": "${UUID}"
        "title": "India",
        "currency_code": "INR",
        "country_code": "+91",
        "iso_code2": "123",
        "iso_code3": "456"
      }],
    }
  }
  ```

  
## Delete Countries

This api is used to `delete` tag

- route: `/country/:countryId`
- method: `DELETE`
- request:
  ```js
  {
    "params": {
      "countryId": ["${UUID}"]
    }
  }
  ```
- response:
  ```js
  {
    "code": 200,
    "data": {
      "message": "Deleted Successfully"
    }
  }
  ```

## Create City

This API is used to create `city`.

- route: `/city`
- method: `POST`
- request:
  ```js
  {
    "body": {
      "title": "Indore",
      "country":"${UUID}"
    }
  }
  ```
- response:
  ```js
  {
    "code": 201,
    "data": {
      "id": "${UUID}",
      "title": "Indore"
    }
  }
  ```

## Get City

This api is used to get all `cities`

- route: `/city`
- method: `GET`
- request:

  ```js
  // type one
  {
    "query": 
    {
      "search": "", // show all results
      "countryId":"${UUID}",
      "page": 1,
      "limit": 10
    },
  }
 

  // type two
  {
    "query": 
    {
      "title": "b" // show only those results whose title includes `b` only
      "countryId":"${UUID}"
      "page": 1,
      "limit": 10
    },
  }

  ```

- response:
  ```js
  {
    "code": 200,
    "data": {
      "count": 200,
      "next": "${NEXT_PAGE_PATH}",
      "previous": "${PREVIOUS_PAGE_PATH}",
      "results": [{
        "id": "${UUID}",
        "title": "Gwalior",
        "country": "${UUID}"
      }],
    }
  }
  ```

## Delete Cities

This api is used to `delete` cities

- route: `/city/:cityId`
- method: `DELETE`
- request:
  ```js
  {
    "params": {
      "cityId": ["${UUID}"]
    }
  }
  ```
- response:
  ```js
  {
    "code": 200,
    "data": {
      "message": "Deleted Successfully"
    }
  }
  ```

## Create Job Category

This API is used to create `Job Category`.

- route: `/job-category`
- method: `POST`
- request:
  ```js
  {
    "body": {
      "title": "Teacher"
    }
  }
  ```
- response:
  ```js
  {
    "code": 201,
    "data": {
      "id": "${UUID}",
      "title": "Teacher"
    }
  }
  ```

## Get Job Category

This api is used to get all `Job Categories`

- route: `/job-category`
- method: `GET`
- request:

  ```js
  // type one
  {
    "query": 
    {
      "search": "" // show all results
      "page": 1,
      "limit": 10
    },
  }
 

  // type two
  {
    "query": 
    {
      "title": "b" // show only those results whose title includes `b` only
      "page": 1,
      "limit": 10
    },
  }

  ```

- response:
  ```js
  {
    "code": 200,
    "data": {
      "count": 200,
      "next": "${NEXT_PAGE_PATH}",
      "previous": "${PREVIOUS_PAGE_PATH}",
      "results": [{
        "id": "${UUID}",
        "title": "Teacher"
      }],
    }
  }
  ```

## Delete Job Categories

This api is used to `delete` job categories

- route: `/job-category/:jobCategoryId`
- method: `DELETE`
- request:
  ```js
  {
    "params": {
      "jobCategoryId": ["${UUID}"]
    }
  }
  ```
- response:
  ```js
  {
    "code": 200,
    "data": {
      "message": "Deleted Successfully"
    }
  }
  ```

## Get Users Count

This api is used to get all `Users Count`

- route: `/users-count`
- method: `GET`

- response:
  ```js
  {
    "code": 200,
    "data": {
        "total_user": 36,
        "job_seekers": 26,
        "employers": 7,
        "vendors": 3,
        "active_user": 35,
        "total_jobs": 8,
        "active_jobs": 3
    }
  }
  ```

## Get Credit

This api is used to get all `Credit`

- route: `/credit`
- method: `GET`
- request:

  ```js
  {
    "query": 
    {
      "preiod": 0 || 1 || 2...  // 0 for current month ; 1 for last months
    },
  }
  ```

- response:
  ```js
  {
    "code": 200,
    "data": {
        "total": 17374,
        "gold": 6428,
        "silver": 5907,
        "copper": 4863
    }
  }
  ```

## Get Dashboard

This api is used to get all `Dashboard `

- route: `/dashboard`
- method: `GET`
- request:

  ```js
  // type one
  {
    "query": 
    {
      "preiod": "this week" || "last week" || "this month"|| "last month"|| "this year"|| "last year"  // 0 for current year ; 1 for last year
    },
  }

  // type two
  {
    "query": 
    {
      "start-date": "YYYY-MM-DD"  // 0 for current year ; 1 for last year
      "end-date": "YYYY-MM-DD"  // 0 for current year ; 1 for last year
    },
  }
  ```

- response:
  ```js
  {
    "code": 200,
    "data": {
        "employers": 345,
        "jobs": 252
    }
  }
  ```

## Get Jobs List

This api is used to get all `Jobs List `

- route: `/jobs`
- method: `GET`
- request:

  ```js
  {
    "query": 
    {
      "search": "search keyword" || "",  // for search data
      "country": "country name" || "",
      "city": "city name" || "",
      "fullTime": true || false || null,
      "partTime": true || false || null,
      "contract": true || false || null,
      "timing": 1 || 2 || 3 || 4 || 5 || 6 || 7,
      "salary_min": 1000,
      "salary_max": 2000,
      "limit": 10,
      "page": 1
    },
  }
  ```

- response:
  ```js
  {
    "code": 200,
    "data": {
            "count": 200,
            "next": "${NEXT_PAGE_PATH}",
            "previous": "${PREVIOUS_PAGE_PATH}",
            "results": [
                {
                    "id": "${UUID}",
                    "job_id": "6513-7666",
                    "title": "Online Data Entry Job in Swedan",
                    "address": "Los Angeles, CA, USA",
                    "city": {
                        ....
                    },
                    "country": {
                        ....
                    },
                    "status": "active",
                    "user": "TCS"
                }
            ]
    }
  }
  ```

## Delete Jobs

This api is used to Delete `Jobs`

- route: `/jobs/:jobId`
- method: `DELETE`
- request:
  ```js
  {
    "params": {
      "jobId": "${UUID}"
    }
  }
  ```

- response:
  ```js
  {
    "code": 200,
    "data": {
      "message": "Deleted Successfully"
    }
  }
  ```

## Restored Job

This api is used to revert `Jobs`

- route: `/jobs/:jobId/revert`
- method: `PATCH`
- request:
  ```js
  {
    "params": {
      "jobId": "${UUID}"
    }
  }
  ```

- response:
  ```js
  {
    "code": 200,
    "data": {
      "message": "Job restored successfully"
    }
  }
  ```

## Active Inactive Jobs

This api is used to inactivate `Jobs`

- route: `/jobs/:jobId`
- method: `PUT`
- request:
  ```js
  {
    "params": {
      "jobId": "${UUID}"
    }
  }
  ```

- response:
  ```js
  {
    "code": 200,
    "data": {
      "message": "This job is inactive" || "This job is active"
    }
  }
  ```

## Get Employers List

This api is used to get all `Employers List `

- route: `/employer`
- method: `GET`
- request:

  ```js
  {
    "query": 
    {
      "search": "search keyword" || ""  // for search data
      "country": "country name" || "",
      "city": "city name" || "",
      "fullTime": true || false || null,
      "partTime": true || false || null,
      "contract": true || false || null,
      "availability": true || false || null,
      "salary_min": 1000,
      "salary_max": 2000,
      "page": 1,
      "limit": 10
    },
  }
  ```

- response:
  ```js
  {
    "code": 200,
    "data": {
      "count": 200,
      "next": "${NEXT_PAGE_PATH}",
      "previous": "${PREVIOUS_PAGE_PATH}",
      "results": [
          {
            "id": "${UUID}",
            "role": "employer",
            "name": "Name",
            "email": "email@email.com",
            "country_code": "+1",
            "mobile_number": "8899887788",
            "is_active": true || false
          }
      ]
    }
  }
  ```

## Get Candidates List

This api is used to get all `Candidates List `

- route: `/candidates`
- method: `GET`
- request:

  ```js
  {
    "query": 
    {
      "search": "search keyword" || ""  // for search data
      "country": "country name" || "",
      "city": "city name" || "",
      "fullTime": true || false || null,
      "partTime": true || false || null,
      "contract": true || false || null,
      "availability": true || false || null,
      "salary_min": 1000,
      "salary_max": 2000,
      "page": 1,
      "limit": 10
    },
  }
  ```

- response:
  ```js
  {
    "code": 200,
    "data": {
        "count": 200,
        "next": "${NEXT_PAGE_PATH}",
        "previous": "${PREVIOUS_PAGE_PATH}",
        "results": [
            {
              "id": "${UUID}",
              "role": "job_seeker",
              "name": "Name",
              "email": "email@email.com",
              "country_code": "+1",
              "mobile_number": "8899887788",
              "is_active": true || false
            }
        ]
    }
  }
  ```

## Delete Users

This api is used to Delete `Users`

- route: `/user/:userId`
- method: `DELETE`
- request:
  ```js
  {
    "params": {
      "userId": "${UUID}",
    }
  }
  ```

- response:
  ```js
  {
    "code": 200,
    "data": {
      "message": "Deleted Successfully"
    }
  }
  ```

## Inactive Users

This api is used to activate or inactivate `Users`

- route: `/user/:userId`
- method: `Patch`

- response:
  ```js
  {
    "code": 200,
    "data": {
      "message": "This user is inactive" || "This user is active"
    }
  }
  ```

## Get User Rights

This api is used to get `User Rights`

- route: `/user-rights`
- method: `GET`

- response:
  ```js
  {
    "code": 200,
    "data": {
        "description": "This is the description of the user rights..."
    }
  }
  ```

## Update User Rights

This api is used to update or create `User Rights` data.

- route: `/user-rights`
- method: `PATCH`
- request:

  ```js
  {
    "body": {
      "description": "This is the new description of the user rights..."
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

## Get Privacy Policy

This api is used to get `Privacy Policy` data.

- route: `/privacy-policy`
- method: `GET`

- response:
  ```js
  {
    "code": 200,
    "data": {
        "description": "This is the description of the privacy policy..."
    }
  }
  ```

## Update Privacy Policy

This api is used to update or create `Privacy Policy`

- route: `/privacy-policy`
- method: `PATCH`
- request:

  ```js
  {
    "body": {
      "description": "This is the new description of the privacy policy..."
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

## Change Password

This api is used to change admin password `Change Password`

- route: `/change-password`
- method: `PATCH`
- request:

  ```js
  {
    "body": {
      "old_password": "oldpassword"
      "new_password": "newpassword"
    }
  }
  ```


- response:
  ```js
  {
    "code": 200,
    "data": {
        "message": "Password update successfully."
    }
  }
  ```


## Create Job Seekers Category

This api is used to `Create Job Seekers Category` from admin.

- route: `/job-seeker-category`
- method: `POST`
- request:

  ```js
  {
    "body": {
      "title": "main category"
    }
  }
  
  {
    "body": {
      "title": "sub category"
      "category":"${mainCategoryId}"
    }
  }
  ```


- response:
  ```js
  {
    "code": 201,
    "data": {
        "id": "681df447-6f75-4316-a921-77bf20f3aba3",
        "title": "Librarians, Curators, and Archivists",
        "category": "b47d9c47-d19e-4bdd-b943-43a7cb75113f" || null
    }
  }

  ```

## Get Job Seekers Category

This api is used to get all `job seekers category`

- route: `/job-seeker-category`
- method: `GET`
- request:

  ```js
  // type one
  {
    "query": 
    {
      "search": "", // show all results
      "page": 1,
      "limit": 10
    },
  }
 

  // type two
  {
    "query": 
    {
      "title": "b" // show only those results whose title includes `b` only
      "page": 1,
      "limit": 10
    },
  }

  ```

- response:
  ```js
  {
    "code": 200,
    "data": {
      "count": 200,
      "next": "${NEXT_PAGE_PATH}",
      "previous": "${PREVIOUS_PAGE_PATH}",
      "results": [{
        "id": "${UUID}",
        "title": "Computer and Mathematica",
        "category": "${UUID}" || null
      }],
    }
  }
  ```

## Delete Job Seekers Category

This api is used to `delete` job seekers categories

- route: `/job-seeker-category/:jobSeekerCategoryId`
- method: `DELETE`
- request:
  ```js
  {
    "params": {
      "jobSeekerCategoryId": ["${UUID}"]
    }
  }
  ```
- response:
  ```js
  {
    "code": 200,
    "data": {
      "message": "Deleted Successfully"
    }
  }
  ```

## Create Tender Category

This api is used to `Create Tender Category` from admin.

- route: `/tender-category`
- method: `POST`
- request:

  ```js
  {
    "body": {
      "title": "Service"
    }
  }
  ```

- response:
  ```js
  {
    "code": 201,
    "data": {
        "id": "681df447-6f75-4316-a921-77bf20f3aba3",
        "title": "Service"
    }
  }

  ```

## Get Tender Category

This api is used to get all `tender category`

- route: `/tender-category`
- method: `GET`
- request:

  ```js
  // type one
  {
    "query": 
    {
      "search": "", // show all results
      "page": 1,
      "limit": 10
    },
  }
 

  // type two
  {
    "query": 
    {
      "title": "b" // show only those results whose title includes `b` only
      "page": 1,
      "limit": 10
    },
  }

  ```

- response:
  ```js
  {
    "code": 200,
    "data": {
      "count": 200,
      "next": "${NEXT_PAGE_PATH}",
      "previous": "${PREVIOUS_PAGE_PATH}",
      "results": [{
        "id": "${UUID}",
        "title": "Auduting"
      }],
    }
  }
  ```

## Delete Tender Category

This api is used to `delete` tender categories

- route: `/tender-category/:tenderCategoryId`
- method: `DELETE`
- request:
  ```js
  {
    "params": {
      "tenderCategoryId": ["${UUID}"]
    }
  }
  ```
- response:
  ```js
  {
    "code": 200,
    "data": {
      "message": "Deleted Successfully"
    }
  }
  ```

## Create Sectors

This api is used to `Create Sectors` from admin.

- route: `/sector`
- method: `POST`
- request:

  ```js
  {
    "body": {
      "title": "Private"
    }
  }
  ```

- response:
  ```js
  {
    "code": 201,
    "data": {
        "title": "Private"
    }
  }

  ```

## Get Sectors

This api is used to get all `sectors`

- route: `/sector`
- method: `GET`
- request:

  ```js
  // type one
  {
    "query": 
    {
      "search": "", // show all results
      "page": 1,
      "limit": 10
    },
  }
 

  // type two
  {
    "query": 
    {
      "title": "b" // show only those results whose title includes `b` only
      "page": 1,
      "limit": 10
    },
  }

  ```

- response:
  ```js
  {
    "code": 200,
    "data": {
      "count": 200,
      "next": "${NEXT_PAGE_PATH}",
      "previous": "${PREVIOUS_PAGE_PATH}",
      "results": [{
        "id": "${UUID}",
        "title": "Private"
      }],
    }
  }
  ```

## Delete Sector

This api is used to `delete` sectors

- route: `/tender-category/:sectorId`
- method: `DELETE`
- request:
  ```js
  {
    "params": {
      "sectorId": ["${UUID}"]
    }
  }
  ```
- response:
  ```js
  {
    "code": 200,
    "data": {
      "message": "Deleted Successfully"
    }
  }
  ```
