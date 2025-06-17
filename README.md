To Set These SSM Parameters:

You can run this once:

aws ssm put-parameter --name "/rundeck/url" --value "http://<YOUR-RUNDECK-URL>" --type String
aws ssm put-parameter --name "/rundeck/project-name" --value "<YOUR-PROJECT-NAME>" --type String
aws ssm put-parameter --name "/rundeck/api-token" --value "<YOUR-RUNDECK-API-TOKEN>" --type SecureString
