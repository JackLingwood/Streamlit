import pytesseract
from PIL import Image
import re

# Load image
image_path = "certification_sample.jpg"
image = Image.open(image_path)

# Run OCR
text = pytesseract.image_to_string(image)

# Print full OCR text (for debugging)
print("Full OCR Text:\n", text)

# Extract fields using regex or string matching
def extract_field(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else None

worker_name = extract_field(r"SUPERVISOR\s+([A-Za-z\.\s]+)", text)
cert_name = "SITE SAFETY TRAINING"
cert_id = extract_field(r"ID[:\s]*([A-Z0-9]+)", text)
issue_date = extract_field(r"ISSUED[:\s]*(\d{2}/\d{2}/\d{4})", text)
expiry_date = extract_field(r"EXPIRY[:\s]*(\d{2}/\d{2}/\d{4})", text)

# Output results
print("\nExtracted Information:")
print("Worker Name:", worker_name)
print("Certification Name:", cert_name)
print("Certification ID:", cert_id)
print("Issue Date:", issue_date)
print("Expiry Date:", expiry_date)
