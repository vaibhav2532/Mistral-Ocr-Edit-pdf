import json
import base64
import os

# Load JSON data from file
with open("repose.json", "r",  encoding="utf-8", errors="ignore") as f:
    document = json.load(f)

# Create a directory for images if it doesn't exist
image_dir = "images"
os.makedirs(image_dir, exist_ok=True)

# Initialize an empty string for the Markdown content
markdown_content = ""

# Process each page in the document
for page in document["pages"]:
    # Append the markdown text
    markdown_content += page["markdown"] + "\n\n"

    # Process images
    for image in page.get("images", []):
        image_filename = os.path.join(image_dir, image["id"])
        
        # Decode and save the image file
        image_data = base64.b64decode(image["image_base64"].split(",")[1])  # Extracting base64 content
        with open(image_filename, "wb") as img_file:
            img_file.write(image_data)
        
        # Embed image in markdown
        markdown_content += f"![{image['id']}]({image_filename})\n\n"

# Save the reconstructed Markdown file
with open("document.md", "w", encoding="utf-8") as f:
    f.write(markdown_content)

print("Markdown file 'document.md' successfully created!")
