# Vendor

These APIs are for the `CRUD` of an `tenders`

> **NOTE:** The prefix of every `api`' s stated as `api/v1/tenders`
>
## Table Of Content

- **[Tenders Search With Advance Filter](#tenders-search-with-advance-filter)**
- **[Get Tender Detail With Tender Id](#get-tender-detail-with-tender-id)**
- **[Save Advanced Filter for Tenders](#save-advanced-filter-for-tenders)**
- **[Get Advanced Filter for Tenders](#get-advanced-filter-for-tenders)**
- **[Update Advanced Filter for Tender](#update-advanced-filter-for-tender)**
- **[Delete Advanced Filter for Tender](#delete-advanced-filter-for-tender)**


## Tenders Search With Advance Filter:

### Summary

This API is used to search `tenders`

- route: ` `
- method: `GET`
- request:

  ```js
  {
    "query": {
      "country":  "India" || null ,
      "city": "Bhopal" || null ,
      "search": "ab" || null ,
      "opportunityType": "government" || "ngo" || "business" ,
      "budget_min":  1000 || null ,
      "budget_max":  2000 || null ,
      "deadline":  "yyyy-MM-dd" || null,
      "tenderCategory": ["Multiple", "Insurance"] || null ,
      "tag": ["Backend"] || null ,
      "sector":  "ngo" || "private" || "public"
    }
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
                "description": "",
                "tender_category": [
                    ....
                ],
                "sector": "ngo",
                "created": "2023-04-12T10:32:25",
                "is_applied": false,
                "is_saved": false,
                "user": {
                    ....
                },
                "vendor": 0,
                "status": "active"
            },
        ]
    }
  }
  ```

## Get Tender Detail With Tender Id:

### Summary:

From this API we get `tender` detail using `tenderId`.

- route: `/:tenderId`
- method: `GET`
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
        "id": "${UUID}",
        "title": "test data",
        "tender_id": "9727-3847",
        "budget_currency": "KES",
        "budget_amount": null,
        "description": "",
        "country": {
            ....
        },
        "city": {
            ....
        },
        "tag": [
            {
                ....
            }
        ],
        "tender_category": [
            {
               ....
            }
        ],
        "tender_type": "business",
        "sector": "ngo",
        "deadline": "yyyy-MM-dd",
        "start_date": "yyyy-MM-dd",
        "status": "active",
        "user": {
            ....
        },
        "attachments": [],
        "created": "yyyy-MM-dd HH:mm:ss",
        "vendor": 0,
        "is_applied": false,
        "is_saved": false
    }
  }
  ```

## Save Advanced Filter for Tenders:

### Summary:

From this API we save advanced filter for `tender` search.

- route: `/filter`
- method: `POST`
- request:
  ```js
  {
    "body": {
        "title": "test data",
        "country":  "${UUID}" || null ,
        "city": "${UUID}" || null ,
        "search": "ab" || null ,
        "opportunity_type": "government" || "ngo" || "business" ,
        "budget_min":  1000 || null ,
        "budget_max":  2000 || null ,
        "deadline":  "yyyy-MM-dd" || null,
        "tender_category": ["${UUID}", "${UUID}"] || null ,
        "tag": ["${UUID}"] || null ,
        "sector":  "ngo" || "private" || "public",
        "is_notification": true || false || null
    }
  }

  ```

- response:

  ```js
  {
    "code": 200,
    "data": {
        "id": "${UUID}",
        "title": "second tenders filter",
        "country": "${UUID}",
        "city": "${UUID}",
        "opportunity_type": null,
        "sector": null,
        "deadline": null,
        "budget_min": null,
        "budget_max": null,
        "tender_category": [],
        "tag": [],
        "is_notification": false
    }
  }
  ```

## Get Advanced Filter for Tenders:

### Summary:

From this API we get all saved advanced filter for `tender` search.

- route: `/filter`
- method: `GET`

- response:

  ```js
  {
    "code": 200,
    "data": [
        {
            "id": "${UUID}",
            "title": "first tenders filter",
            "country": {
                ....
            },
            "city": {
                ....
            },
            "opportunity_type": null,
            "sector": null,
            "deadline": null,
            "budget_min": null,
            "budget_max": null,
            "tender_category": [],
            "tag": [],
            "is_notification": false
        },
        {
            "id": "${UUID}",
            "title": "second tenders filter",
            "country": {
                ....
            },
            "city": {
                ....
            },
            "opportunity_type": null,
            "sector": null,
            "deadline": null,
            "budget_min": null,
            "budget_max": null,
            "tender_category": [],
            "tag": [],
            "is_notification": false
        }
    ]
  }
  ```

## Update Advanced Filter for Tender:

### Summary:

From this API we get all saved advanced filter for `tender` search.

- route: `/filter/:filterId`
- method: `PUT`
- request:
  ```js
  {
    "params": {
        "filterId":  "${UUID}"
    },
    "body": {
        "title": "test data",
        "country":  "${UUID}" || null ,
        "city": "${UUID}" || null ,
        "search": "ab" || null ,
        "opportunity_type": "government" || "ngo" || "business" ,
        "budget_min":  1000 || null ,
        "budget_max":  2000 || null ,
        "deadline":  "yyyy-MM-dd" || null,
        "tender_category": ["${UUID}", "${UUID}"] || null ,
        "tag": ["${UUID}"] || null ,
        "sector":  "ngo" || "private" || "public",
        "is_notification": true || false || null
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

## Delete Advanced Filter for Tender:

### Summary:

From this API we get all saved advanced filter for `tender` search.

- route: `/filter/:filterId`
- method: `DELETE`
- request:
  ```js
  {
    "params": {
        "filterId":  "${UUID}"
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
