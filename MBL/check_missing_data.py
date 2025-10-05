#!/usr/bin/env python3
"""
Product Data Completeness Check
Checks all products for missing values in key fields and identifies what needs to be filled.
"""

import json
from pathlib import Path

def check_missing_data():
    """Check all products for missing data fields."""
    
    # Load products data
    products_file = Path("data/products_data.json")
    if not products_file.exists():
        print(f"❌ Error: {products_file} not found!")
        return
    
    with open(products_file, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    print("🔍 CHECKING PRODUCT DATA COMPLETENESS")
    print("=" * 60)
    
    # Track missing data
    missing_description = []
    missing_indication = []
    missing_side_effect = []
    missing_dosage = []
    missing_crops_pests = []
    
    # Check each product
    for product in products:
        product_id = product.get('product_id', '')
        product_name = product.get('product_name', '')
        description = product.get('description', '').strip()
        indication = product.get('indication', '').strip()
        side_effect = product.get('side_effect', '').strip()
        dosage = product.get('dosage', '').strip()
        crops_pests = product.get('crops_pests', '').strip()
        
        if not description:
            missing_description.append({'id': product_id, 'name': product_name})
        
        if not indication:
            missing_indication.append({'id': product_id, 'name': product_name})
        
        if not side_effect:
            missing_side_effect.append({'id': product_id, 'name': product_name})
        
        if not dosage:
            missing_dosage.append({'id': product_id, 'name': product_name})
        
        if not crops_pests:
            missing_crops_pests.append({'id': product_id, 'name': product_name})
    
    # Print results
    print(f"📊 MISSING DATA SUMMARY:")
    print(f"Total products: {len(products)}")
    print(f"Missing descriptions: {len(missing_description)}")
    print(f"Missing indications: {len(missing_indication)}")
    print(f"Missing side effects: {len(missing_side_effect)}")
    print(f"Missing dosage: {len(missing_dosage)}")
    print(f"Missing crops & pests: {len(missing_crops_pests)}")
    print()
    
    # Show missing descriptions
    if missing_description:
        print("❌ MISSING DESCRIPTIONS:")
        print("-" * 40)
        for item in missing_description:
            print(f"{item['id']} - {item['name']}")
        print()
    
    # Show missing indications
    if missing_indication:
        print("❌ MISSING INDICATIONS:")
        print("-" * 40)
        for item in missing_indication:
            print(f"{item['id']} - {item['name']}")
        print()
    
    # Show missing side effects
    if missing_side_effect:
        print("❌ MISSING SIDE EFFECTS:")
        print("-" * 40)
        for item in missing_side_effect:
            print(f"{item['id']} - {item['name']}")
        print()
    
    # Show missing dosage
    if missing_dosage:
        print("❌ MISSING DOSAGE:")
        print("-" * 40)
        for item in missing_dosage:
            print(f"{item['id']} - {item['name']}")
        print()
    
    # Show missing crops & pests
    if missing_crops_pests:
        print("❌ MISSING CROPS & PESTS:")
        print("-" * 40)
        for item in missing_crops_pests:
            print(f"{item['id']} - {item['name']}")
        print()
    
    return {
        'missing_description': missing_description,
        'missing_indication': missing_indication,
        'missing_side_effect': missing_side_effect,
        'missing_dosage': missing_dosage,
        'missing_crops_pests': missing_crops_pests
    }

def show_product_details(product_id):
    """Show detailed information for a specific product."""
    
    products_file = Path("data/products_data.json")
    with open(products_file, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    for product in products:
        if product.get('product_id') == product_id:
            print(f"\n📋 PRODUCT DETAILS: {product_id}")
            print("=" * 50)
            print(f"Product Name: {product.get('product_name', 'N/A')}")
            print(f"Medicine Name: {product.get('medicine_name', 'N/A')}")
            print(f"Category: {product.get('category_name', 'N/A')}")
            print(f"Description: {product.get('description', 'N/A')}")
            print(f"Indication: {product.get('indication', 'N/A')}")
            print(f"Dosage: {product.get('dosage', 'N/A')}")
            print(f"Side Effect: {product.get('side_effect', 'N/A')}")
            print(f"Crops & Pests: {product.get('crops_pests', 'N/A')}")
            print(f"Origin: {product.get('origin', 'N/A')}")
            return product
    
    print(f"❌ Product {product_id} not found!")
    return None

if __name__ == "__main__":
    missing_data = check_missing_data()
    
    print("📈 COMPLETENESS SUMMARY:")
    print("=" * 40)
    total_fields = 5  # description, indication, side_effect, dosage, crops_pests
    total_products = 81
    
    for field, missing_list in missing_data.items():
        field_name = field.replace('missing_', '').replace('_', ' ').title()
        completeness = ((total_products - len(missing_list)) / total_products) * 100
        print(f"{field_name}: {completeness:.1f}% complete ({len(missing_list)} missing)")
    
    print(f"\n💡 NEXT STEPS:")
    print("1. Review products with missing data")
    print("2. Fill missing descriptions, indications, and side effects")
    print("3. Use product details to generate appropriate content")
    print("4. Update the JSON file with complete information")
