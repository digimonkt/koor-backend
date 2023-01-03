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

## Create Tag

This API is used to create `tags`.

- route: `/tag`
- method: `POST`
- request:
  ```json
  {
    "body": {
      "title": "Backend"
    }
  }
  ```
- response:
  ```json
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

  ```json
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
  ```json
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
  ```json
  {
    "params": {
      "tagId": ["${tagId}"]
    }
  }
  ```
- response:
  ```json
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
  ```json
  {
    "body": {
      "title": "Hindi"
    }
  }
  ```
- response:
  ```json
  {
    "code": 200,
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

  ```json
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
  ```json
  {
    "code": 200,
    "data": {
      "languages": [{
        "id": "${UUID}"
        "title": "Backend"
      }],
      "total": 200, // total number of skills available
      "current_page": 1, // current page of which data is fetched
      "current_limit": 10 // maximum number of data can be in `languages` list
    }
  }
  ```

## Delete Language

This api is used to delete `language`.

- route: `/languages`
- method: `DELETE`
- request:
  ```json
  {
    "query": {
      "languageIds": ["${UUID}"]
    }
  }
  ```
- response:
  ```json
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
  ```json
  {
    "body": {
      "title": "Python"
    }
  }
  ```
- response:
  ```json
  {
    "code": 200,
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

  ```json
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
      "title": "p" // show only those results whose title includes `p` only
    },
    "page": 1,
    "limit": 10,
  }
  ```

- response:
  ```json
  {
    "code": 200,
    "data": {
      "skills": [{
        "id": "${UUID}"
        "title": "Python"
      }],
      "total": 200, // total number of skills available
      "current_page": 1, // current page of which data is fetched
      "current_limit": 10 // maximum number of data can be in `skills` list
    }
  }
  ```

## Delete Skills

- route: `/skills`
- method: `DELETE`
- request:
  ```json
  {
    "query": {
      "skillsIds": ["${UUID}"]
    }
  }
  ```
- response:
  ```json
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
  ```json
  {
    "body": {
      "title": "Bachelors"
    }
  }
  ```
- response:
  ```json
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

  ```json
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
      "title": "b" // show only those results whose title includes `p` only
    },
    "page": 1,
    "limit": 10,
  }
  ```

- response:
  ```json
  {
    "code": 200,
    "data": {
      "education_level": [{
        "id": "${UUID}"
        "title": "Bachelors"
      }],
      "total": 200, // total number of skills available
      "current_page": 1, // current page of which data is fetched
      "current_limit": 10 // maximum number of data can be in `education_level` list
    }
  }
  ```

## Delete Education Level

- route: `/skills`
- method: `DELETE`
- request:
  ```json
  {
    "query": {
      "educationLevelIds": ["${UUID}"]
    }
  }
  ```
- response:
  ```json
  {
    "code": 200,
    "data": {
      "message": "Deleted Successfully"
    }
  }
  ```
