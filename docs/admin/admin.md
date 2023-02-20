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
  - [Create City](#create-city)
  - [Get City](#get-city)
  - [Delete Cities](#delete-cities)
  - [Create Job Category](#create-job-category)
  - [Get Job Category](#get-job-category)

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
    "code": 200,
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
    "searchfilter": {
      "title": "" // show all results
    },
    "page": 1,
    "limit": 10,
  }

  // type two
  {
    "searchfilter": {
      "title": "b" // show only those results whose title includes `b` only
    },
    "page": 1,
    "limit": 10,
  }
  ```

- response:
  ```js
  {
    "code": 200,
    "data": {
      "tags": [{
        "id": "${UUID}"
        "title": "Backend"
      }],
      "total": 200, // total number of skills available
      "current_page": 1, // current page of which data is fetched
      "current_limit": 10 // maximum number of data can be in `tags` list
    }
  }
  ```

## Delete Tags

This api is used to `delete` tag

- route: `/tag`
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
      "title": "" // show all results
    },
  }

  // type two
  {
    "query": {
      "title": "b" // show only those results whose title includes `b` only
    },
  }
  ```

- response:
  ```js
  {
    "code": 200,
    "data": {
      "results": [{
        "id": "${UUID}"
        "title": "Backend"
      }],
    }
  }
  ```

## Delete Language

This api is used to delete `language`.

- route: `/languages`
- method: `DELETE`
- request:
  ```js
  {
    "query": {
      "languageIds": ["${UUID}"]
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
      "title": "" // show all results
    },
  }

  // type two
  {
    "query": {
      "title": "p" // show only those results whose title includes `p` only
    },
  }
  ```

- response:
  ```js
  {
    "code": 200,
    "data": {
      "results": [{
        "id": "${UUID}"
        "title": "Python"
      }],
    }
  }
  ```

## Delete Skills

- route: `/skills`
- method: `DELETE`
- request:
  ```js
  {
    "query": {
      "skillsIds": ["${UUID}"]
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
      "title": "" // show all results
    },
  }

  // type two
  {
    "query": {
      "title": "b" // show only those results whose title includes `p` only
    },
  }
  ```

- response:
  ```js
  {
    "code": 200,
    "data": {
      "results": [{
        "id": "${UUID}"
        "title": "Bachelors"
      }],
    }
  }
  ```

## Delete Education Level

- route: `/skills`
- method: `DELETE`
- request:
  ```js
  {
    "query": {
      "educationLevelIds": ["${UUID}"]
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
    },
  }
 

  // type two
  {
    "query": 
    {
      "title": "b" // show only those results whose title includes `b` only
    },
  }

  ```

- response:
  ```js
  {
    "code": 200,
    "data": {
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
      "countryId":"${UUID}"
    },
  }
 

  // type two
  {
    "query": 
    {
      "title": "b" // show only those results whose title includes `b` only
      "countryId":"${UUID}"
    },
  }

  ```

- response:
  ```js
  {
    "code": 200,
    "data": {
      "results": [{
        "id": "${UUID}",
        "title": "Gwalior",
        "country": "${UUID}"
      }],
    }
  }
  ```

## Delete Cities

This api is used to `delete` tag

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
    },
  }
 

  // type two
  {
    "query": 
    {
      "title": "b" // show only those results whose title includes `b` only
    },
  }

  ```

- response:
  ```js
  {
    "code": 200,
    "data": {
      "results": [{
        "id": "${UUID}",
        "title": "Teacher"
      }],
    }
  }
  ```
