# Employer

These APIs are for the `CRUD` of an `employer`

> **NOTE:** The prefix of every `api`' s stated as `api/v1/user/employer`
>
> **NOTE:** The user’s `id` can be accessed through this `token` only.
>
> **NOTE:** All these API’s are protected and only can be access by the employer.

## Table Of Content

- **[Update About](#update-about)**

## Update About

### Summary

This API is used to update `employer`'s about section

- route: `about-me`
- method: `PATCH`
- request:

  ```js
  {
    "headers": {
      "Content-Type": "multipart/form-data"
    },
    "body": {
      "organizationName": "Digimonk Technologies",
      "typeOfOrganization": "business" || "ngo" || "government",
      "mobileNumber": "1234567890",
      "countryCode": "+91",
      "licenseId": "LAS001TA",
      "license": File
    }
  }
  ```

- response:

  ```js
  {
    "code": 204,
    "data": {
      "message": "Updated Successfully"
    }
  }
  ```
