import json
from google.cloud import bigquery
f3 = open("unifi_cat_app.json","r")

apps = json.load(f3)

categories = []
applications = []

for key,value in apps["categories"].items():
    value["_id"] = key
    categories.append(value)

for key,value in apps["applications"].items():
    value["_id"] = key
    applications.append(value)

client = bigquery.Client(project="internet-schedule")

job_config = bigquery.LoadJobConfig(
    autodetect=True, source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
)

load_job = client.load_table_from_json(categories,
 "internet-schedule.unifi.categories", job_config=job_config
)  # Make an API request.
load_job.result()  # Waits for the job to complete.
destination_table = client.get_table("internet-schedule.unifi.categories")
print("Loaded {} rows.".format(destination_table.num_rows))

load_job = client.load_table_from_json(applications,
 "internet-schedule.unifi.applications", job_config=job_config
)  # Make an API request.
load_job.result()  # Waits for the job to complete.
destination_table = client.get_table("internet-schedule.unifi.applications")
print("Loaded {} rows.".format(destination_table.num_rows))