#!/usr/bin/env python3
"""
Fix duplicate product IDs and regenerate unique IDs for all products
"""

import json
import os
from pathlib import Path

def fix_product_ids():
    """Fix duplicate product IDs and create unique sequential IDs"""
    print("🔧 Fixing duplicate product IDs...")
    
    # Load existing products
    with open('data/products_data.json', 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    print(f"📊 Found {len(products)} products")
    
    # Create unique sequential IDs
    for i, product in enumerate(products, 1):
        old_id = product['product_id']
        new_id = f"MBL-{i:03d}"
        product['product_id'] = new_id
        
        # Update image paths if they exist
        if product.get('product_image') and product['product_image'].startswith('images/'):
            old_filename = product['product_image'].split('/')[-1]
            new_filename = f"{new_id}.{old_filename.split('.')[-1]}"
            product['product_image'] = f"images/{new_filename}"
        
        # Update additional images if they exist
        if product.get('additional_images'):
            new_additional_images = []
            for j, img_path in enumerate(product['additional_images']):
                if img_path.startswith('images/'):
                    old_filename = img_path.split('/')[-1]
                    file_ext = old_filename.split('.')[-1]
                    new_filename = f"{new_id}_({j+1}).{file_ext}"
                    new_additional_images.append(f"images/{new_filename}")
                else:
                    new_additional_images.append(img_path)
            product['additional_images'] = new_additional_images
        
        print(f"   {old_id} → {new_id}: {product['product_name']}")
    
    # Save updated products
    with open('data/products_data.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Fixed {len(products)} product IDs")
    print("💾 Updated products_data.json with unique IDs")
    
    return products

def clean_images_folder():
    """Clean the images folder and prepare for fresh download"""
    print("\n🧹 Cleaning images folder...")
    
    images_dir = Path("images")
    if images_dir.exists():
        # Count existing images
        existing_images = list(images_dir.glob("*"))
        print(f"📁 Found {len(existing_images)} existing images")
        
        # Ask if user wants to clean
        clean = input("🗑️ Do you want to delete existing images and start fresh? (y/n): ").lower().strip()
        if clean in ['y', 'yes']:
            for img_file in existing_images:
                img_file.unlink()
            print(f"🗑️ Deleted {len(existing_images)} existing images")
        else:
            print("📁 Keeping existing images")
    else:
        images_dir.mkdir(exist_ok=True)
        print("📁 Created images folder")

def main():
    """Main function to fix product IDs"""
    print("🚀 McDonald Bangladesh Products - ID Fix")
    print("="*60)
    
    # Fix product IDs
    products = fix_product_ids()
    
    # Clean images folder
    clean_images_folder()
    
    print("\n✅ Product ID fix completed!")
    print("🔄 Now you can run the enhancement script again to download images with correct IDs")

if __name__ == "__main__":
    main()
