#!/usr/bin/env python3
"""
Update Product Images Script
Updates the products_data.json file to use locally generated images
instead of placeholder URLs.
"""

import json
import os
from pathlib import Path

def update_product_images():
    """Update product images to use local files instead of placeholders."""
    
    # Load products data
    products_file = Path("data/products_data.json")
    if not products_file.exists():
        print(f"❌ Error: {products_file} not found!")
        return
    
    with open(products_file, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    print("🔄 UPDATING PRODUCT IMAGES")
    print("=" * 50)
    
    # Check images folder
    images_folder = Path("images")
    if not images_folder.exists():
        print(f"❌ Error: {images_folder} folder not found!")
        return
    
    # Get list of all image files in the images folder
    image_files = set()
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp']:
        image_files.update([f.name for f in images_folder.glob(ext)])
    
    updated_count = 0
    not_found_count = 0
    
    # Update products with placeholder images
    for product in products:
        product_id = product.get('product_id', '')
        product_image = product.get('product_image', '')
        
        # Check if it's a placeholder image
        if 'product-image.jpg' in product_image or 'product-image.png' in product_image:
            # Look for corresponding local image
            possible_names = [
                f"{product_id}.jpg",
                f"{product_id}.jpeg", 
                f"{product_id}.png",
                f"{product_id}.gif",
                f"{product_id}.bmp"
            ]
            
            found_image = None
            for name in possible_names:
                if name in image_files:
                    found_image = name
                    break
            
            if found_image:
                # Update the product image path
                old_image = product_image
                product['product_image'] = f"images/{found_image}"
                updated_count += 1
                print(f"✅ {product_id}: {old_image} → images/{found_image}")
            else:
                not_found_count += 1
                print(f"❌ {product_id}: No local image found for {product_image}")
    
    # Save updated data
    if updated_count > 0:
        # Create backup
        backup_file = Path("data/products_data_backup.json")
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(products, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Backup saved to: {backup_file}")
        
        # Save updated file
        with open(products_file, 'w', encoding='utf-8') as f:
            json.dump(products, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Updated {updated_count} product images")
        print(f"❌ {not_found_count} products still need images")
        print(f"💾 Updated file saved to: {products_file}")
    else:
        print("ℹ️  No updates needed - all images are already local")
    
    return updated_count, not_found_count

def verify_updates():
    """Verify that the updates were successful."""
    
    products_file = Path("data/products_data.json")
    with open(products_file, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    print(f"\n🔍 VERIFICATION:")
    print("-" * 30)
    
    placeholder_count = 0
    local_count = 0
    
    for product in products:
        product_image = product.get('product_image', '')
        if 'product-image.jpg' in product_image or 'product-image.png' in product_image:
            placeholder_count += 1
        elif product_image.startswith('images/'):
            local_count += 1
    
    print(f"Products with local images: {local_count}")
    print(f"Products with placeholder images: {placeholder_count}")
    
    if placeholder_count == 0:
        print("🎉 All products now use local images!")
    else:
        print(f"⚠️  {placeholder_count} products still need local images")

if __name__ == "__main__":
    updated, not_found = update_product_images()
    verify_updates()
    
    print(f"\n📊 SUMMARY:")
    print("=" * 30)
    print(f"Updated: {updated}")
    print(f"Still need images: {not_found}")
    
    if not_found == 0:
        print("🎉 All product images are now local!")
    else:
        print(f"💡 Generate {not_found} more images to complete the database")
