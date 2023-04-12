# Vendor

These APIs are for the `CRUD` of an `vendor`

> **NOTE:** The prefix of every `api`' s stated as `api/v1/users/vendor`
>
> **NOTE:** The user’s `id` can be accessed through this `token` only.
>
> **NOTE:** All these API’s are protected and only can be access by the employer.

## Table Of Content

- **[Update About](#update-about)**
- **[Save Tenders](#save-tenders)**
- **[Get Tenders](#get-tenders)**


## Update About:

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
      "organization_name": "Digimonk Technologies Vendor",
      "organization_type": "business" || "ngo" || "government",
      "market_information_notification":true,
      "other_notification":true,
      "license_id": "LAS001TA",
      "license": File,
      "registration_number": "RN001TA",
      "registration_certificate": File,
      "operating_years": 10,
      "jobs_experience": 5
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

## Save Tenders:

### Summary:

From this API `vendor` will be able to save `tender`.

- route: `/tender/save/:tenderId`
- method: `POST`
- request:

  ```js
  {
    "params": {
      "tenderId": "${UUID}"
    }
  }
  ```

- response:

  ```js
  {
    "code": 200,
    "data": {
      "message": "Saved Successfully"
    }
  }
  ```

## Get Tenders:

### Summary:

From this API `vendor` will be able to get saved `tender`.

- route: `/tender/save`
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
                "tender": {
                    .....
                }
            }
        ]
    }
  }
  ```
