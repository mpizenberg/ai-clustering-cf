import json
import os
from typing import List, Dict

def read_json_file(file_path: str) -> Dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def extract_fields(proposal: Dict, fields: List[str]) -> Dict:
    return {field: proposal.get(field) for field in fields}

def process_directory(directory: str, output_file: str, fields: List[str]):
    all_data = []

    # Iterate through all JSON files in the directory
    for filename in sorted(os.listdir(directory)):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            json_data = read_json_file(file_path)

            # Extract the 'data' field from each file
            proposals = json_data.get('data', [])

            # Extract specified fields from each proposal
            extracted_proposals = [extract_fields(proposal, fields) for proposal in proposals]

            all_data.extend(extracted_proposals)

    # Write the aggregated and extracted data to a new JSON file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(all_data, outfile, ensure_ascii=False, indent=2)

    print(f"Processed {len(all_data)} proposals.")
    print(f"Aggregated data saved to {output_file}")

# Specify the directory containing the JSON files
input_directory = "catalyst_proposals_f13_open_dev"

# Specify the output file name
output_file = "aggregated_catalyst_data.json"

# Specify the fields you're interested in
fields_of_interest = [
    'id', 'user_id', 'title', 'ideascale_user', 'ideascale_id',
    'ideascale_link', 'amount_requested', 'problem'
]

# Run the process
process_directory(input_directory, output_file, fields_of_interest)
