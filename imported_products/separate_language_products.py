import json
import re

def contains_bengali_script(text):
    """Check if text contains Bengali script characters"""
    if not text:
        return False
    # Bengali Unicode range: U+0980 to U+09FF
    bengali_pattern = re.compile(r'[\u0980-\u09FF]')
    return bool(bengali_pattern.search(text))

def separate_english_bengali_products():
    # Read the filtered products
    with open('kb_filtered_products.json', 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    print(f"Processing {len(products)} filtered products...")
    
    english_products = []
    bengali_products = []
    
    for product in products:
        # Check if product name contains Bengali script
        product_name = product.get('product_name', '')
        
        if contains_bengali_script(product_name):
            # This is a Bengali product
            bengali_products.append(product)
        else:
            # This is an English product
            english_products.append(product)
    
    # Update field name from "common_name" to "medicine_name" for both lists
    def update_field_names(product_list):
        for product in product_list:
            if 'common_name' in product:
                product['medicine_name'] = product.pop('common_name')
        return product_list
    
    english_products = update_field_names(english_products)
    bengali_products = update_field_names(bengali_products)
    
    # Save English products
    with open('kb_english_products.json', 'w', encoding='utf-8') as f:
        json.dump(english_products, f, indent=2, ensure_ascii=False)
    
    # Save Bengali products
    with open('kb_bengali_products.json', 'w', encoding='utf-8') as f:
        json.dump(bengali_products, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print(f"\n=== LANGUAGE SEPARATION RESULTS ===")
    print(f"Total products processed: {len(products)}")
    print(f"English products: {len(english_products)}")
    print(f"Bengali products: {len(bengali_products)}")
    
    # Show some examples
    print(f"\n=== ENGLISH PRODUCTS EXAMPLES ===")
    for i, product in enumerate(english_products[:5]):
        print(f"{i+1}. ID: {product['product_id']}, Name: '{product['product_name']}', Medicine: '{product.get('medicine_name', '')}'")
    
    print(f"\n=== BENGALI PRODUCTS EXAMPLES ===")
    for i, product in enumerate(bengali_products[:5]):
        print(f"{i+1}. ID: {product['product_id']}, Name: '{product['product_name']}', Medicine: '{product.get('medicine_name', '')}'")
    
    print(f"\n=== FILES CREATED ===")
    print(f"English products saved to: 'kb_english_products.json'")
    print(f"Bengali products saved to: 'kb_bengali_products.json'")
    
    return english_products, bengali_products

if __name__ == "__main__":
    separate_english_bengali_products()
