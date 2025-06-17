import requests
import csv
import time

# Config
rundeck_url = "http://<YOUR-RUNDECK-HOST>:4440"
api_token = "<YOUR-API-TOKEN>"
project_name = "<YOUR-PROJECT-NAME>"

headers = {
    "X-Rundeck-Auth-Token": api_token,
    "Accept": "application/json"
}

jobs_endpoint = f"{rundeck_url}/api/36/project/{project_name}/jobs"
execution_endpoint_template = f"{rundeck_url}/api/36/job/{{job_id}}/executions?max=1"

output_csv = f"{project_name}_rundeck_jobs_with_status.csv"

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
                time.sleep(0.1)  # to avoid hitting rate limits

        print(f"✅ Jobs with status written to {output_csv}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    export_jobs_with_status()
