import json
import re
from datetime import datetime

def extract_product_id_from_name(product_name):
    """Extract or generate product ID from product name"""
    # Remove special characters and convert to uppercase
    clean_name = re.sub(r'[^\w\s]', '', product_name.upper())
    # Take first 3-4 words and create ID
    words = clean_name.split()[:3]
    return '-'.join(words)

def clean_text(text):
    """Clean and format text fields"""
    if not text:
        return ""
    # Remove extra whitespace and normalize
    return ' '.join(text.split())

def extract_tags_from_data(product_name, medicine_name, crop, pest):
    """Generate tags from available data"""
    tags = []
    
    if product_name:
        tags.append(product_name.lower())
    if medicine_name:
        tags.append(medicine_name.lower())
    if crop:
        tags.append(crop.lower())
    if pest:
        tags.append(pest.lower())
    
    return list(set(tags))  # Remove duplicates

def convert_kb_to_products():
    # Read the kb.json file
    with open('kb.json', 'r', encoding='utf-8') as f:
        kb_data = json.load(f)
    
    products = []
    product_id_counter = 1
    
    for crop_name, crop_data in kb_data.items():
        if isinstance(crop_data, list):
            for pest_entry in crop_data:
                pest_name = pest_entry.get('pest', '')
                symptoms = pest_entry.get('symptoms', '')
                causes = pest_entry.get('causes', '')
                
                if 'products' in pest_entry:
                    for product in pest_entry['products']:
                        product_name = product.get('product_name', '')
                        medicine_name = product.get('medicine_name', '')
                        application_rates = product.get('application_rates', '')
                        frequency_of_use = product.get('frequency_of_use', '')
                        safety_precautions = product.get('safety_precautions', '')
                        
                        # Generate product ID
                        product_id = f"KB-{product_id_counter:03d}"
                        product_id_counter += 1
                        
                        # Create product entry
                        product_entry = {
                            "product_id": product_id,
                            "product_name": clean_text(product_name),
                            "product_image": "",  # Empty for now
                            "common_name": clean_text(medicine_name),
                            "category_name": "",  # Will need to be determined based on medicine type
                            "description": "",  # Empty for now
                            "application_rates": clean_text(application_rates),
                            "frequency_of_use": clean_text(frequency_of_use),
                            "side_effect": clean_text(safety_precautions),
                            "crops_pests": clean_text(f"{crop_name} - {pest_name}"),
                            "crops": clean_text(crop_name),
                            "pest": clean_text(pest_name),
                            "symptoms": clean_text(symptoms),
                            "causes": clean_text(causes),
                            "product_tags": extract_tags_from_data(product_name, medicine_name, crop_name, pest_name),
                            "product_price": "",  # Empty for now
                            "reg_no": "",  # Empty for now
                            "serial_no": str(product_id_counter - 1),
                            "product_url": "",  # Empty for now
                            "origin": "",  # Empty for now
                            "isActive": "true",
                            "Stocks": "3654",
                            "extraction_date": datetime.now().isoformat()
                        }
                        
                        products.append(product_entry)
    
    # Write to new file
    with open('kb_converted_products.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"Converted {len(products)} products from kb.json to kb_converted_products.json")
    return products

if __name__ == "__main__":
    convert_kb_to_products()
