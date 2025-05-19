
**Article**

```json
{
  "articles": [
    {
      "title": "string",
      "subtitle": "string",
      "month": "string",             // e.g. "April", "February"
      "preface": "string",
      "artwork": "string",           // If artwork/description is provided at the top
      "author": "string",
      "sections": [
        {
          "title": "string",         // E.g. "Introduction", "History and Significance"
          "content": "string",
          "photoDescriptions": [
            "string"
          ]
        }
        // ... more sections
      ],
      "roles": [
        {
          "roleType": "string",      // e.g. "Historian", "Editor"
          "skills": [
            "string"
          ]
        }
        // ... more roles
      ],
      "ratingCriteria": [
        {
          "criteria": "string",
          "scale": [
            "string"
          ]
        }
        // ... more criteria
      ],
      "articleRatings": {
        "criteria": "score (number or string)" // Only if present, otherwise omit
      },
      "references": [
        "string"
      ]
    }
    // ...more articles
  ]
}
```