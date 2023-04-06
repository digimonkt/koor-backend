# Vendor

These APIs are for the `CRUD` of an `vendor`

> **NOTE:** The prefix of every `api`' s stated as `api/v1/users/vendor`
>
> **NOTE:** The user’s `id` can be accessed through this `token` only.
>
> **NOTE:** All these API’s are protected and only can be access by the employer.

## Table Of Content

- **[Update About](#update-about)**


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
