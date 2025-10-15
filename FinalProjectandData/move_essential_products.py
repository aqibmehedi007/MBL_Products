#!/usr/bin/env python3
"""
Script to move products with isActive=true and essential fields filled
Ignores optional fields like reg_no, serial_no, product_url, origin
"""

import os
import json
import shutil

def move_essential_complete_products(products_dir, active_dir):
    """
    Move products that are active (isActive=true) and have essential fields filled
    Ignores optional fields: reg_no, serial_no, product_url, origin
    """
    if not os.path.exists(active_dir):
        os.makedirs(active_dir)
        print(f"Created directory: {active_dir}")
    
    product_files = [f for f in os.listdir(products_dir) if f.endswith('.json')]
    print(f"Found {len(product_files)} product files to check...\n")
    
    moved_count = 0
    kept_count = 0
    moved_files = []
    kept_files = []
    incomplete_details = []
    
    # Define ESSENTIAL fields only (ignoring optional fields)
    essential_fields = [
        "product_id", "product_name", "product_image", "medicine_name", "category_name",
        "description", "application_rates", "frequency_of_use", "side_effect",
        "crops_pests", "crops", "pest", "symptoms", "causes", "product_tags",
        "isActive", "Stocks", "extraction_date"
    ]
    
    # Fields to ignore (optional fields)
    ignored_fields = ["reg_no", "serial_no", "product_url", "origin", "product_price"]
    
    print(f"Checking ESSENTIAL fields only: {', '.join(essential_fields)}")
    print(f"Ignoring optional fields: {', '.join(ignored_fields)}\n")
    
    for filename in product_files:
        file_path = os.path.join(products_dir, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                product_data = json.load(f)
            
            # Check if isActive is true
            if product_data.get('isActive') != 'true':
                print(f"[KEPT] {filename} (isActive: {product_data.get('isActive')})")
                kept_count += 1
                kept_files.append(filename)
                continue
            
            # Check if all ESSENTIAL fields are filled (not empty or None)
            missing_fields = []
            for field in essential_fields:
                if field == "product_price":  # Skip product_price as it's allowed to be empty
                    continue
                
                value = product_data.get(field)
                if value is None or (isinstance(value, str) and not value.strip()) or (isinstance(value, list) and not value):
                    missing_fields.append(field)
            
            if missing_fields:
                print(f"[KEPT] {filename} (Missing essential fields: {', '.join(missing_fields)})")
                kept_count += 1
                kept_files.append(filename)
                incomplete_details.append({'filename': filename, 'missing_fields': missing_fields})
            else:
                # Move to active_products folder
                destination = os.path.join(active_dir, filename)
                shutil.move(file_path, destination)
                print(f"[MOVED] {filename} -> {active_dir}/")
                moved_count += 1
                moved_files.append(filename)
                
        except json.JSONDecodeError:
            print(f"[ERROR] Could not decode JSON from {filename}. Skipping.")
            kept_count += 1
            kept_files.append(filename)
        except Exception as e:
            print(f"[ERROR] An unexpected error occurred with {filename}: {e}. Skipping.")
            kept_count += 1
            kept_files.append(filename)
    
    print("\n" + "="*70)
    print("SUMMARY:")
    print("="*70)
    print(f"Total files processed: {len(product_files)}")
    print(f"Essential-complete & active products moved: {moved_count}")
    print(f"Incomplete/inactive products remaining: {kept_count}")
    print(f"Active products folder now contains: {len(os.listdir(active_dir))} files")
    print(f"Remaining products folder: {products_dir}/")
    
    if moved_files:
        print(f"\nFiles moved to active_products/ ({len(moved_files)}):")
        for f in moved_files:
            print(f"  [OK] {f}")
    
    if kept_files:
        print(f"\nFiles remaining in products/ ({len(kept_files)}):")
        for f in kept_files:
            print(f"  [KEPT] {f}")
    
    if incomplete_details:
        print(f"\nDetailed breakdown of incomplete products:")
        for detail in incomplete_details:
            print(f"  • {detail['filename']}: Missing {', '.join(detail['missing_fields'])}")
    
    print(f"\nNote: This script only checks ESSENTIAL fields.")
    print(f"Ignored optional fields: {', '.join(ignored_fields)}")
    
    if kept_files:
        print(f"\nYou can now work on the remaining products in the 'products/' folder.")
    if moved_files:
        print("Products in 'active_products/' have essential fields complete and are ready for use!")

if __name__ == "__main__":
    products_directory = 'products'
    active_products_directory = 'active_products'
    move_essential_complete_products(products_directory, active_products_directory)
