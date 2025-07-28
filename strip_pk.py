import json

with open("products.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Remove all 'pk' fields to allow Django to auto-assign IDs
for item in data:
    item.pop("pk", None)

with open("products_clean.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ Cleaned JSON saved as products_clean.json")
