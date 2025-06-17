## 🔐 Setting AWS SSM Parameters for Rundeck Access

Before running the script, make sure you store the required Rundeck configuration values in **AWS Systems Manager Parameter Store**.

You can do this with the following AWS CLI commands:

```bash
# Set the Rundeck base URL (e.g., http://rundeck.example.com)
aws ssm put-parameter \
  --name "/rundeck/url" \
  --value "http://<YOUR-RUNDECK-URL>" \
  --type String

# Set the Rundeck project name (e.g., MyProject)
aws ssm put-parameter \
  --name "/rundeck/project-name" \
  --value "<YOUR-PROJECT-NAME>" \
  --type String

# Set the Rundeck API token (stored securely)
aws ssm put-parameter \
  --name "/rundeck/api-token" \
  --value "<YOUR-RUNDECK-API-TOKEN>" \
  --type SecureString
