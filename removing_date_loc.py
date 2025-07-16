import json

# Load the original data
with open("letters_cleaned.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Remove 'date_location' and keep only title + body
cleaned_data = [{"title": item["title"], "body": item["body"]} for item in data]

# Save the cleaned data
with open("data/letters_no_date.json", "w", encoding="utf-8") as f:
    json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

print(f"✅ Cleaned {len(cleaned_data)} letters. Saved to data/letters_no_date.json.")