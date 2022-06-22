from google.cloud import bigquery

import json
f = open("unifi_trafficrules.json","r")
f2 = open("unifi_networkconf.json","r")
f3 = open("unifi_cat_app.json","r")

rules = json.load(f)
networks = json.load(f2)
apps = json.load(f3)

client = bigquery.Client(project="internet-schedule")

# TODO(developer): Set table_id to the ID of the table to create.
table_id = "internet-schedule.unifi.networkconf"

# Set the encryption key to use for the destination.
# TODO: Replace this key with a key you have created in KMS.
# kms_key_name = "projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}".format(
#     "cloud-samples-tests", "us", "test", "test"
# )
job_config = bigquery.LoadJobConfig(
    autodetect=True, source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
)

load_job = client.load_table_from_json(networks["data"],
 table_id, job_config=job_config
)  # Make an API request.
load_job.result()  # Waits for the job to complete.
destination_table = client.get_table(table_id)
print("Loaded {} rows.".format(destination_table.num_rows))