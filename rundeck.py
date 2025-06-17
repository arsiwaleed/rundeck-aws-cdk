import requests
import csv
import time
import boto3

# === CONFIG ===
aws_region = "us-east-1"  # Change to your AWS region

# === LOAD PARAMETERS FROM AWS PARAMETER STORE ===
def get_parameter(name, with_decryption=True, region='us-east-1'):
    ssm = boto3.client('ssm', region_name=region)
    response = ssm.get_parameter(
        Name=name,
        WithDecryption=with_decryption
    )
    return response['Parameter']['Value']

# Load Rundeck config from SSM
rundeck_url = get_parameter("/rundeck/url", region=aws_region)
project_name = get_parameter("/rundeck/project-name", region=aws_region)
api_token = get_parameter("/rundeck/api-token", region=aws_region)

# === API SETUP ===
headers = {
    "X-Rundeck-Auth-Token": api_token,
    "Accept": "application/json"
}
jobs_endpoint = f"{rundeck_url}/api/36/project/{project_name}/jobs"
execution_endpoint_template = f"{rundeck_url}/api/36/job/{{job_id}}/executions?max=1"

# === FILE OUTPUT ===
output_csv = f"{project_name}_rundeck_jobs_with_status.csv"

# === GET LATEST EXECUTION STATUS ===
def get_latest_execution_status(job_id):
    url = execution_endpoint_template.format(job_id=job_id)
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        executions = response.json().get("executions", [])
        if executions:
            return executions[0].get("status", "unknown")
        else:
            return "no executions"
    except requests.exceptions.RequestException:
        return "error"

# === EXPORT TO CSV ===
def export_jobs_with_status():
    try:
        response = requests.get(jobs_endpoint, headers=headers)
        response.raise_for_status()
        jobs = response.json()

        fieldnames = ["id", "name", "group", "description", "project", "href", "permalink", "latest_status"]
        with open(output_csv, mode="w", newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for job in jobs:
                job_id = job.get("id")
                status = get_latest_execution_status(job_id)
                writer.writerow({
                    "id": job_id,
                    "name": job.get("name"),
                    "group": job.get("group", ""),
                    "description": job.get("description", ""),
                    "project": job.get("project", ""),
                    "href": job.get("href", ""),
                    "permalink": job.get("permalink", ""),
                    "latest_status": status
                })
                time.sleep(0.1)

        print(f"✅ Jobs with status written to {output_csv}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")

# === MAIN ===
if __name__ == "__main__":
    export_jobs_with_status()
