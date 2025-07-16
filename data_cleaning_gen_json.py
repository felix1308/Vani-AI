import json
import re

def clean_body(text):
    # 1. Remove header junk before the actual letter
    text = re.sub(
        r"BhaktivedantaVedabaseSettings.*?Letter to:.*?\d{2}-\d{2}-\d{2}",
        "",
        text,
        flags=re.DOTALL
    )

    # 2. Remove long "DonateThanks to..." block at the end
    text = re.sub(
        r"DonateThanks to.*?supportingthis site\.",
        "",
        text,
        flags=re.DOTALL
    )

    # 3. Remove exact duplicate lines
    lines = text.splitlines()
    seen = set()
    deduped_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped and stripped not in seen:
            deduped_lines.append(stripped)
            seen.add(stripped)

    return "\n".join(deduped_lines)

# Load the letters.json file
with open("letters.json", "r", encoding="utf-8") as f:
    letters = json.load(f)

# Clean each letter's body
for letter in letters:
    if "body" in letter:
        letter["body"] = clean_body(letter["body"])

# Save the cleaned letters
with open("letters_cleaned.json", "w", encoding="utf-8") as f:
    json.dump(letters, f, indent=2, ensure_ascii=False)

print("✅ Cleaned letters saved to letters_cleaned.json")
