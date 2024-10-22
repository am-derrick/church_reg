import json
from datetime import datetime

def format_date(date_str):
    """Convert date string to Django's datetime format with microseconds"""
    try:
        # Parse the date and add time with microseconds
        dt = datetime.strptime(date_str, "%d/%m/%Y")
        return dt.strftime("%Y-%m-%d %H:%M:%S.%f")
    except ValueError as e:
        print(f"Error parsing date: {date_str} - {e}")
        return None

def clean_value(value):
    """Handle empty or null values appropriately"""
    if value in ['', None]:
        return None
    return value

# Load the original JSON data
with open('MOCK_DATA.json', 'r') as file:
    data = json.load(file)

# Process and convert the data
converted_data = []
pk_counter = 22  # Starting primary key

for entry in data:
    converted_entry = {
        "model": "members.Registration",  # Include the app name
        "pk": pk_counter,
        "fields": {
            "first_name": entry["first_name"],
            "last_name": entry["last_name"],
            "gender": entry["gender"],
            "phone_number": entry["phone_number"],
            "residence": entry["residence"],
            "is_student": entry["is_student"],
            "institution_name": clean_value(entry["institution_name"]),
            "institution_location": clean_value(entry["institution_location"]),
            "occupation": clean_value(entry["occupation"]),
            "is_first_time": entry["is_first_time"],
            "consent": entry["consent"],
            "created_at": format_date(entry["created_at"]),
            "last_updated": format_date(entry["last_updated"])
        }
    }
    
    # Remove any None values for fields that shouldn't be null
    fields_to_check = ["first_name", "last_name", "gender", "phone_number", 
                      "residence", "is_student", "is_first_time", "consent"]
    
    if all(converted_entry["fields"].get(field) is not None for field in fields_to_check):
        converted_data.append(converted_entry)
        pk_counter += 1

# Save the converted data
with open('converted_MOCK_DATA.json', 'w') as outfile:
    json.dump(converted_data, outfile, indent=2)

print("Conversion completed and saved to converted_MOCK_DATA.json")