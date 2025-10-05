#!/usr/bin/env python3
"""
Non-interactive McDonald Bangladesh Products Enhancement Script
Processes all products automatically without user input
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.enhance_product_details_v2 import EnhancedProductExtractor

def process_all_products():
    """Process all products automatically"""
    print("🚀 McDonald Bangladesh Products - Full Enhancement")
    print("="*60)
    
    # Initialize extractor
    extractor = EnhancedProductExtractor()
    
    # Load existing products
    if not extractor.load_products():
        print("❌ Failed to load products")
        return False
    
    # Print current status
    print("\n📊 Current Status:")
    extractor.print_enhancement_summary()
    
    # Process all products from the beginning
    print(f"\n🔍 Processing all products from the beginning...")
    print("⏱️ This will take approximately 10-15 minutes...")
    
    try:
        extractor.enhance_products(max_products=None, start_index=0)
        
        # Print final summary
        print("\n📊 Final Enhancement Summary:")
        extractor.print_enhancement_summary()
        
        # Save enhanced data
        extractor.save_products()
        
        print("\n✅ Full enhancement completed successfully!")
        return True
        
    except KeyboardInterrupt:
        print("\n⏹️ Enhancement interrupted by user.")
        # Save partial progress
        extractor.save_products()
        return False
    except Exception as e:
        print(f"\n❌ Error during enhancement: {e}")
        # Save partial progress
        extractor.save_products()
        return False

if __name__ == "__main__":
    success = process_all_products()
    if success:
        print("\n🎉 All products have been enhanced successfully!")
        print("📁 Check the 'images' folder for all downloaded product images.")
        print("📄 Check 'data/products_data.json' for the complete enhanced dataset.")
    else:
        print("\n⚠️ Enhancement completed with some issues. Check the logs above.")
