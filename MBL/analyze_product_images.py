#!/usr/bin/env python3
"""
Detailed Product Image Analysis Script
Provides comprehensive analysis of the product image database.
"""

import json
import os
from pathlib import Path
from collections import defaultdict

def analyze_product_images():
    """Analyze the product image database in detail."""
    
    # Load products data
    products_file = Path("data/products_data.json")
    if not products_file.exists():
        print(f"❌ Error: {products_file} not found!")
        return
    
    with open(products_file, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    print("🔍 DETAILED PRODUCT IMAGE ANALYSIS")
    print("=" * 70)
    
    # Check images folder
    images_folder = Path("images")
    if not images_folder.exists():
        print(f"❌ Error: {images_folder} folder not found!")
        return
    
    # Get list of all image files in the images folder
    image_files = set()
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp']:
        image_files.update([f.name for f in images_folder.glob(ext)])
    
    # Categorize products
    categories = defaultdict(list)
    placeholder_products = []
    actual_image_products = []
    
    for product in products:
        product_id = product.get('product_id', 'Unknown')
        product_name = product.get('product_name', 'Unknown')
        category = product.get('category_name', 'Unknown')
        product_image = product.get('product_image', '')
        
        # Categorize by image status
        if 'product-image.jpg' in product_image or 'product-image.png' in product_image:
            placeholder_products.append(product)
        else:
            actual_image_products.append(product)
        
        categories[category].append(product)
    
    # Print category analysis
    print("📊 PRODUCTS BY CATEGORY:")
    print("-" * 50)
    for category, prods in sorted(categories.items()):
        placeholder_count = sum(1 for p in prods if 'product-image.jpg' in p.get('product_image', ''))
        actual_count = len(prods) - placeholder_count
        print(f"{category}: {len(prods)} products ({actual_count} with images, {placeholder_count} placeholders)")
    
    print("\n" + "=" * 70)
    
    # Detailed analysis
    print("📈 DETAILED IMAGE STATUS:")
    print("-" * 50)
    
    # Products with actual images
    print(f"✅ Products with actual images: {len(actual_image_products)}")
    for product in actual_image_products[:10]:  # Show first 10
        print(f"   {product['product_id']} - {product['product_name']}")
    if len(actual_image_products) > 10:
        print(f"   ... and {len(actual_image_products) - 10} more")
    
    print(f"\n⚠️  Products with placeholder images: {len(placeholder_products)}")
    for product in placeholder_products:
        print(f"   {product['product_id']} - {product['product_name']}")
    
    # Additional images analysis
    print(f"\n📁 ADDITIONAL IMAGES ANALYSIS:")
    print("-" * 50)
    
    additional_images_count = 0
    products_with_additional = 0
    
    for product in products:
        additional_images = product.get('additional_images', [])
        if additional_images:
            products_with_additional += 1
            additional_images_count += len(additional_images)
    
    print(f"Products with additional images: {products_with_additional}")
    print(f"Total additional images: {additional_images_count}")
    
    # Image file analysis
    print(f"\n🖼️  IMAGE FILE ANALYSIS:")
    print("-" * 50)
    
    # Count by extension
    ext_counts = defaultdict(int)
    for img_file in image_files:
        ext = Path(img_file).suffix.lower()
        ext_counts[ext] += 1
    
    print("Images by file extension:")
    for ext, count in sorted(ext_counts.items()):
        print(f"   {ext}: {count} files")
    
    # Primary vs Additional images
    primary_images = [f for f in image_files if not '(' in f and not f.startswith('MBL-') == False]
    additional_images = [f for f in image_files if '(' in f]
    
    print(f"\nPrimary product images: {len(primary_images)}")
    print(f"Additional product images: {len(additional_images)}")
    
    # Coverage statistics
    print(f"\n📊 COVERAGE STATISTICS:")
    print("-" * 50)
    total_products = len(products)
    actual_coverage = len(actual_image_products) / total_products * 100
    placeholder_coverage = len(placeholder_products) / total_products * 100
    
    print(f"Total products: {total_products}")
    print(f"With actual images: {len(actual_image_products)} ({actual_coverage:.1f}%)")
    print(f"With placeholder images: {len(placeholder_products)} ({placeholder_coverage:.1f}%)")
    print(f"Total image files: {len(image_files)}")
    print(f"Average images per product: {len(image_files) / total_products:.1f}")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    print("-" * 50)
    if placeholder_products:
        print(f"• Generate {len(placeholder_products)} product images to replace placeholders")
        print(f"• Focus on products: {', '.join([p['product_id'] for p in placeholder_products[:5]])}")
        if len(placeholder_products) > 5:
            print(f"  ... and {len(placeholder_products) - 5} more")
    
    if additional_images_count > 0:
        print(f"• Consider organizing {additional_images_count} additional images")
    
    print(f"• Current image database is {actual_coverage:.1f}% complete")
    
    return {
        'total_products': total_products,
        'actual_images': len(actual_image_products),
        'placeholder_images': len(placeholder_products),
        'total_image_files': len(image_files),
        'additional_images': additional_images_count,
        'coverage_percentage': actual_coverage
    }

if __name__ == "__main__":
    results = analyze_product_images()
    
    print(f"\n🎯 FINAL SUMMARY:")
    print("=" * 70)
    print(f"✅ Image database is {results['coverage_percentage']:.1f}% complete")
    print(f"📊 {results['actual_images']}/{results['total_products']} products have actual images")
    print(f"🖼️  {results['total_image_files']} total image files available")
    print(f"📁 {results['additional_images']} additional product images")
    
    if results['coverage_percentage'] >= 90:
        print("🎉 Excellent image coverage!")
    elif results['coverage_percentage'] >= 70:
        print("👍 Good image coverage!")
    else:
        print("⚠️  Consider improving image coverage")
