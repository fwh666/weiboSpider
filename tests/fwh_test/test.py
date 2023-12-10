import json

def is_valid_json(json_str):
    try:
        json.loads(json_str)
        return True
    except ValueError:
        return False

# Example usage
json_str = '{"name": "John", "age": 30, "city": "New York"}'
if is_valid_json(json_str):
    print("Valid JSON format")
else:
    print("Invalid JSON format")
