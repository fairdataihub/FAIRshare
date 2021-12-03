---
sidebar_position: 5
---

# Environment variables

Within the developer environment, we use a few environment variable to ensure that any test datasets created aren't going to be made permenant. At the current stage of the application a few data repositories provide a test environment for developers to test on. You will have to use a `.env` file to add these environment variables directly into the application.

```yml title=".env"
# zenodo
VUE_APP_ZENODO_SERVER_URL=https://sandbox.zenodo.org/api/
VUE_APP_ZENODO_ACCESS_TOKEN=YOUR_ACCESS_TOKEN #sign up at sandbox.zenodo.org for a key
```

For developers at Fair Data Innovations Hub, you may use the environment variables provided in this repository: [https://github.com/fairdataihub/env-files](https://github.com/fairdataihub/env-files/blob/main/SODA-for-COVID-19-Research)
