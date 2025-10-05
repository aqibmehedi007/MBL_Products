#!/usr/bin/env python3
"""
Simple Primary Image Check
Checks if primary images exist in the images folder for all products.
"""

import json
import os
from pathlib import Path

def check_primary_images():
    """Check if primary images exist for all products."""
    
    # Load products data
    products_file = Path("data/products_data.json")
    if not products_file.exists():
        print(f"❌ Error: {products_file} not found!")
        return
    
    with open(products_file, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    print("🔍 CHECKING PRIMARY IMAGES")
    print("=" * 40)
    
    # Check images folder
    images_folder = Path("images")
    if not images_folder.exists():
        print(f"❌ Error: {images_folder} folder not found!")
        return
    
    # Get list of all image files in the images folder
    image_files = set()
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp']:
        image_files.update([f.name for f in images_folder.glob(ext)])
    
    missing_images = []
    found_images = []
    
    # Check each product's primary image
    for product in products:
        product_id = product.get('product_id', '')
        product_name = product.get('product_name', '')
        product_image = product.get('product_image', '')
        
        # Extract filename from product_image path
        if product_image:
            image_filename = os.path.basename(product_image)
        else:
            image_filename = f"{product_id}.jpg"  # Default expected filename
        
        # Check if image exists
        if image_filename in image_files:
            found_images.append(product_id)
        else:
            missing_images.append({
                'id': product_id,
                'name': product_name,
                'expected': image_filename
            })
    
    # Print results
    print(f"📊 RESULTS:")
    print(f"Total products: {len(products)}")
    print(f"Primary images found: {len(found_images)}")
    print(f"Primary images missing: {len(missing_images)}")
    print()
    
    if missing_images:
        print("❌ MISSING PRIMARY IMAGES:")
        print("-" * 30)
        for item in missing_images:
            print(f"{item['id']} - {item['name']}")
            print(f"   Expected: {item['expected']}")
            print()
    else:
        print("✅ ALL PRIMARY IMAGES ARE AVAILABLE!")
    
    return len(found_images), len(missing_images)

if __name__ == "__main__":
    found, missing = check_primary_images()
    
    print("📈 SUMMARY:")
    print("=" * 20)
    print(f"Found: {found}")
    print(f"Missing: {missing}")
    
    if missing == 0:
        print("🎉 Perfect! All primary images are available.")
    else:
        print(f"⚠️  {missing} primary images are missing.")
