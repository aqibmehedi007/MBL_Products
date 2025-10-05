#!/usr/bin/env python3
"""
Test script for Enhanced McDonald Bangladesh Products Enhancement V2
Tests the improved enhancement process with proper HTML structure parsing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.enhance_product_details_v2 import EnhancedProductExtractor

def test_enhancement_v2():
    """Test enhanced extraction on sample products"""
    print("🧪 Testing McDonald Bangladesh Products Enhancement V2")
    print("="*60)
    
    # Initialize extractor
    extractor = EnhancedProductExtractor()
    
    # Load existing products
    if not extractor.load_products():
        print("❌ Failed to load products")
        return
    
    # Test on first 3 products
    print(f"🔍 Testing enhanced extraction on first 3 products...")
    
    # Show current status of first 3 products
    print("\n📋 Current Status of First 3 Products:")
    for i, product in enumerate(extractor.products[:3]):
        print(f"\n{i+1}. {product['product_name']}")
        print(f"   Category: {product['category_name']}")
        print(f"   Description: {product['description'][:50]}..." if product['description'] else "   Description: Empty")
        print(f"   Dosage: {product['dosage'][:30]}..." if product['dosage'] else "   Dosage: Empty")
        print(f"   Crops & Pests: {product['crops_pests'][:30]}..." if product['crops_pests'] else "   Crops & Pests: Empty")
        print(f"   Image: {product['product_image']}")
        print(f"   URL: {product['product_url']}")
    
    # Enhance first 3 products
    extractor.enhance_products(max_products=3, start_index=0)
    
    # Show enhanced status
    print("\n📋 Enhanced Status of First 3 Products:")
    for i, product in enumerate(extractor.products[:3]):
        print(f"\n{i+1}. {product['product_name']}")
        print(f"   Category: {product['category_name']}")
        print(f"   Description: {product['description'][:50]}..." if product['description'] else "   Description: Empty")
        print(f"   Dosage: {product['dosage'][:50]}..." if product['dosage'] else "   Dosage: Empty")
        print(f"   Crops & Pests: {product['crops_pests'][:50]}..." if product['crops_pests'] else "   Crops & Pests: Empty")
        print(f"   Primary Image: {product['product_image']}")
        if product.get('additional_images'):
            print(f"   Additional Images: {len(product['additional_images'])} images")
            for j, img in enumerate(product['additional_images']):
                print(f"     - {img}")
        print(f"   Tags: {product['product_tags']}")
    
    # Save test results
    extractor.save_products()
    
    print("\n✅ Test completed! Check the enhanced data and images folder.")
    print("📁 Check the 'images' folder for downloaded product images.")

if __name__ == "__main__":
    test_enhancement_v2()
