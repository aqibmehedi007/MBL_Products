#!/usr/bin/env python3
"""
Product Image Verification Script
Verifies that all products in products_data.json have their corresponding images
in the images folder.
"""

import json
import os
from pathlib import Path

def verify_product_images():
    """Verify that all products have their corresponding images."""
    
    # Load products data
    products_file = Path("data/products_data.json")
    if not products_file.exists():
        print(f"❌ Error: {products_file} not found!")
        return
    
    with open(products_file, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    print(f"📊 Total products in database: {len(products)}")
    print("=" * 60)
    
    # Check images folder
    images_folder = Path("images")
    if not images_folder.exists():
        print(f"❌ Error: {images_folder} folder not found!")
        return
    
    # Get list of all image files in the images folder
    image_files = set()
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp']:
        image_files.update([f.name for f in images_folder.glob(ext)])
    
    print(f"📁 Total image files in images folder: {len(image_files)}")
    print("=" * 60)
    
    # Track statistics
    missing_images = []
    found_images = []
    placeholder_images = []
    
    # Check each product
    for product in products:
        product_id = product.get('product_id', 'Unknown')
        product_name = product.get('product_name', 'Unknown')
        product_image = product.get('product_image', '')
        
        # Extract filename from product_image path
        if product_image:
            image_filename = os.path.basename(product_image)
        else:
            image_filename = f"{product_id}.jpg"  # Default expected filename
        
        # Check if image exists
        if image_filename in image_files:
            found_images.append({
                'id': product_id,
                'name': product_name,
                'image': image_filename
            })
        else:
            # Check if it's a placeholder image
            if 'product-image.jpg' in product_image or 'product-image.png' in product_image:
                placeholder_images.append({
                    'id': product_id,
                    'name': product_name,
                    'image': product_image
                })
            else:
                missing_images.append({
                    'id': product_id,
                    'name': product_name,
                    'image': product_image or 'No image path'
                })
    
    # Print results
    print(f"✅ Products with images: {len(found_images)}")
    print(f"⚠️  Products with placeholder images: {len(placeholder_images)}")
    print(f"❌ Products missing images: {len(missing_images)}")
    print("=" * 60)
    
    # Show missing images
    if missing_images:
        print("🚨 MISSING IMAGES:")
        print("-" * 40)
        for item in missing_images:
            print(f"ID: {item['id']} | {item['name']}")
            print(f"   Expected: {item['image']}")
            print()
    
    # Show placeholder images
    if placeholder_images:
        print("⚠️  PLACEHOLDER IMAGES:")
        print("-" * 40)
        for item in placeholder_images:
            print(f"ID: {item['id']} | {item['name']}")
            print(f"   Placeholder: {item['image']}")
            print()
    
    # Show summary
    print("📈 SUMMARY:")
    print("-" * 40)
    print(f"Total products: {len(products)}")
    print(f"With actual images: {len(found_images)} ({len(found_images)/len(products)*100:.1f}%)")
    print(f"With placeholder images: {len(placeholder_images)} ({len(placeholder_images)/len(products)*100:.1f}%)")
    print(f"Missing images: {len(missing_images)} ({len(missing_images)/len(products)*100:.1f}%)")
    
    # Check for orphaned images (images without corresponding products)
    expected_image_names = set()
    for product in products:
        product_id = product.get('product_id', '')
        if product_id:
            # Check for various possible image extensions
            for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                expected_image_names.add(f"{product_id}{ext}")
    
    orphaned_images = image_files - expected_image_names
    if orphaned_images:
        print(f"\n🔍 ORPHANED IMAGES (images without corresponding products): {len(orphaned_images)}")
        print("-" * 40)
        for img in sorted(orphaned_images):
            print(f"   {img}")
    
    return {
        'total_products': len(products),
        'found_images': len(found_images),
        'placeholder_images': len(placeholder_images),
        'missing_images': len(missing_images),
        'orphaned_images': len(orphaned_images),
        'missing_list': missing_images,
        'placeholder_list': placeholder_images
    }

if __name__ == "__main__":
    print("🔍 PRODUCT IMAGE VERIFICATION")
    print("=" * 60)
    results = verify_product_images()
    
    if results['missing_images'] == 0 and results['placeholder_images'] == 0:
        print("\n🎉 SUCCESS: All products have proper images!")
    else:
        print(f"\n⚠️  ATTENTION: {results['missing_images']} products missing images, {results['placeholder_images']} with placeholders")
