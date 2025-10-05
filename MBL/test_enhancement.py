#!/usr/bin/env python3
"""
Test script for McDonald Bangladesh Products Enhancement
Tests the enhancement process on a few sample products
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.enhance_product_details import EnhancedProductExtractor

def test_enhancement():
    """Test enhancement on sample products"""
    print("🧪 Testing McDonald Bangladesh Products Enhancement")
    print("="*60)
    
    # Initialize extractor
    extractor = EnhancedProductExtractor()
    
    # Load existing products
    if not extractor.load_products():
        print("❌ Failed to load products")
        return
    
    # Test on first 3 products
    print(f"🔍 Testing enhancement on first 3 products...")
    
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
        print(f"   Dosage: {product['dosage'][:30]}..." if product['dosage'] else "   Dosage: Empty")
        print(f"   Crops & Pests: {product['crops_pests'][:30]}..." if product['crops_pests'] else "   Crops & Pests: Empty")
        print(f"   Image: {product['product_image']}")
        print(f"   Tags: {product['product_tags']}")
    
    # Save test results
    extractor.save_products()
    
    print("\n✅ Test completed! Check the enhanced data and images folder.")

if __name__ == "__main__":
    test_enhancement()
