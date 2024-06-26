import json

# Sample JSON output for demonstration (replace with actual data)
json_output = '''
[
    {"row_7": "Hello my self rohit", "row_10": "Hey what did you do"}, 
    {"row_18": "the dog was done some waste", "row_22": "loading"}, 
    {"row_67": "Kohli is the worlds best batsmen"}
]
'''

# Parse the JSON output
interpretations = json.loads(json_output)

# Sample Final_Output JSON data for demonstration (replace with actual data)
Final_out = {
    "Per LPA": [
        {
            "page_number": 55,
            "text": "Subject to Sections 8.3(6) and 8.3(7), the Management Fee shall be payable by the fund semi-annually in arrears."
        }
    ],
    "DEFINITIONS": [
        {
            "page_number": 42,
            "text": "Closing Date shall mean the date the Insurer is admitted to the Fund as a Limited Partner in accordance with Section 1.5."
        },
        {
            "page_number": 28,
            "text": "10.2. Related Funds. The General Partner, or other members of the Management Group or any Related Party, may at any time or from time to time..."
        }
    ]
}

# Function to transform the JSON and include interpretations correctly
def transform_json(old_json, interpretations):
    new_json = {
        "mfeesRelated": [],
        "KeyTermDefinitionRelated": []
    }

    # Function to create new entry
    def create_new_entry(item, interpretation_text):
        return {
            "Extracts": [item["text"]],
            "Metadata": {
                "Page no": item.get("page_number", None),
                "Found in pdf": not ("No Match Found" in item["text"])
            },
            "Interpretation": [interpretation_text]
        }

    # Transform Per LPA section
    for item in old_json.get("Per LPA", []):
        for interp in interpretations:
            for key, value in interp.items():
                new_json["mfeesRelated"].append(create_new_entry(item, {key: value}))

    # Transform Definitions section
    for item in old_json.get("DEFINITIONS", []):
        for interp in interpretations:
            for key, value in interp.items():
                new_json["KeyTermDefinitionRelated"].append(create_new_entry(item, {key: value}))

    return new_json

# Transform the original JSON data
new_json = transform_json(Final_out, interpretations)

# Define your dynamic filename (replace 'final_dynamic_name' with the actual variable or string)
final_dynamic_name = "output"
output_filename = f"{final_dynamic_name}_ground_truths_extracts.json"

# Write the transformed JSON data to a file
with open(output_filename, 'w', encoding='utf-8') as f:
    json.dump(new_json, f, ensure_ascii=False, indent=4)

# Output the new JSON structure
print(json.dumps(new_json, ensure_ascii=False, indent=4))
