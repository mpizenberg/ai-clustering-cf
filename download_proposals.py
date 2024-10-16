import requests
import json
import os
import time

base_url = 'https://www.lidonation.com/api/catalyst-explorer/proposals'
headers = {
    'accept': 'application/json',
    'X-CSRF-TOKEN': 'your-x-csrf-token'
}

params = {
    'challenge_id': 146, # Fund 13, Open Dev category
    'per_page': 50
}

# Create a directory to store the JSON files
directory = f"catalyst_proposals_f13_open_dev"
os.makedirs(directory, exist_ok=True)

all_proposals = []

for page in range(1, 11):  # This will fetch pages 1 to 10
    print(f"Try downloading for page {page} ...")
    params['page'] = page

    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        proposals = data.get('data', [])
        all_proposals.extend(proposals)
        print(f"Fetched page {page}, got {len(proposals)} proposals")

        # Write the raw JSON response to a file
        filename = os.path.join(directory, f"page_{page}.json")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Saved raw data for page {page} to {filename}")

        # waiting 5s to not overload the server
        time.sleep(5.0)
    else:
        print(f"Failed to fetch page {page}. Status code: {response.status_code}")
        break

# all_proposals_filename = os.path.join(directory, "all_proposals.json")
# with open(all_proposals_filename, 'w', encoding='utf-8') as f:
#     json.dump(all_proposals, f, ensure_ascii=False, indent=2)

print(f"Total proposals fetched: {len(all_proposals)}")
print(f"Raw JSON responses saved in directory: {directory}")

# You can now work with the 'all_proposals' list, which contains all the fetched proposals
# The raw JSON responses are saved in individual files for each page
