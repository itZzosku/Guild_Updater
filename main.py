import requests
import time

# Setup for the POST request
post_url = 'https://raider.io/api/crawler/guilds'
payload = {
    "realmId": 631,
    "realm": "Kazzak",
    "region": "eu",
    "guild": "Pohjoinen",
    "numMembers": 0
}

# Sending the POST request to initiate the job
post_response = requests.post(post_url, json=payload)

if post_response.status_code == 200:
    post_response_data = post_response.json()
    # Dynamically extract the batch_id from the POST response
    batch_id = post_response_data.get('jobData', {}).get('batchId', "")
    if batch_id:
        print(f"Job submitted successfully. Batch ID: {batch_id}")

        monitor_url = f'https://raider.io/api/crawler/monitor?batchId={batch_id}'

        # Loop to monitor the job status
        while True:
            response = requests.get(monitor_url)
            if response.status_code == 200:
                response_data = response.json()
                batch_status = response_data.get('batchInfo', {}).get('status', "")
                if 'jobs' in response_data.get('batchInfo', {}) and len(response_data['batchInfo']['jobs']) > 0:
                    position_in_queue = response_data['batchInfo']['jobs'][0].get('positionInQueue', "N/A")
                    print(f"Job Status: {batch_status}, Current position in queue: {position_in_queue}")
                else:
                    print(f"Job Status: {batch_status}, No job information available.")

                # Check for "complete" status instead of "done"
                if batch_status == "complete":
                    print("Monitoring complete. Job status is complete.")
                    break
                else:
                    # print("Job is still active, waiting, or queued. Waiting for the next check...")
                    time.sleep(30)  # Adjust the sleep time as necessary
            else:
                print(f"Failed to get monitoring info. Status code: {response.status_code}")
                break
    else:
        print("Failed to extract batchId from the POST response.")
else:
    print(f"Failed to submit job. Status code: {post_response.status_code}")
