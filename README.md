# resumePdfGenerator

Google Cloud Function that generates PDF resumes from JSON input using Jinja2 templates and WeasyPrint. The resulting PDF is uploaded to a Google Cloud Storage bucket.

## Deployment

1. Set the environment variable `BUCKET_NAME` to the destination Cloud Storage bucket.
2. Deploy the function:

```bash
gcloud functions deploy generate_resume_pdf \
    --runtime python311 \
    --trigger-http \
    --allow-unauthenticated \
    --set-env-vars BUCKET_NAME=your-bucket
```

## JSON Payload Example

```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "555-0100",
  "summary": "Experienced software engineer...",
  "experience": ["Company A - Engineer", "Company B - Developer"],
  "education": ["BSc Computer Science"],
  "skills": ["Python", "GCP"],
  "template": "modern"
}
```

Choose a template from `modern`, `double_column`, or `creative`.
