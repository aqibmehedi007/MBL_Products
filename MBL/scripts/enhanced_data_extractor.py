#!/usr/bin/env python3
"""
Enhanced Data Extractor for McDonald Bangladesh Products
Improved version with better pattern matching and comprehensive data extraction
"""

import requests
import json
import re
import os
from bs4 import BeautifulSoup
from pathlib import Path
import time
from urllib.parse import urljoin, urlparse
from PIL import Image
import io

class EnhancedDataExtractor:
    def __init__(self, json_file_path="data/products_data.json"):
        self.json_file_path = json_file_path
        self.products = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Enhanced patterns for better data extraction
        self.dosage_patterns = [
            # Standard dosage patterns
            r'(\d+)\s*ml/\s*(\d+)\s*L(?:it)?\s*(?:of\s*water)?[,\s]*(\d+)\s*ml/acre',
            r'(\d+)\s*ml/\s*(\d+)\s*L(?:it)?\s*(?:of\s*water)?',
            r'(\d+)\s*ml/acre',
            r'(\d+)\s*gm/\s*(\d+)\s*L(?:it)?',
            r'(\d+)\s*kg/acre',
            r'(\d+)\s*gm/acre',
            r'(\d+)\s*ml/\s*(\d+)\s*L',
            r'(\d+)\s*gm/\s*(\d+)\s*L\s*water',
            r'(\d+)\s*ml/\s*(\d+)\s*L\s*water',
            # Specific patterns
            r'(\d+)\s*gm/\s*(\d+)\s*L\s*water[,\s]*(\d+)\s*gm/acre',
            r'(\d+)\s*ml/\s*(\d+)\s*L\s*water[,\s]*(\d+)\s*ml/acre',
            r'(\d+)\s*ml/\s*(\d+)\s*L\s*water[,\s]*(\d+)\s*gm/acre',
            # Spray patterns
            r'(\d+)\s*gm/\s*(\d+)\s*L\s*of\s*water',
            r'(\d+)\s*ml/\s*(\d+)\s*L\s*of\s*water',
            # Area-based patterns
            r'(\d+)\s*ml/\s*(\d+)\s*L\s*water[,\s]*(\d+)\s*ml/ha',
            r'(\d+)\s*gm/\s*(\d+)\s*L\s*water[,\s]*(\d+)\s*gm/ha',
            # Tree/fruit patterns
            r'(\d+)\s*gm/\s*(\d+)\s*L\s*water[,\s]*(\d+)\s*gm/tree',
            r'(\d+)\s*ml/\s*(\d+)\s*L\s*water[,\s]*(\d+)\s*ml/tree',
        ]
        
        self.crops_pests_patterns = [
            # Direct crop/pest mentions
            r'(?:for|target|crops?|pests?)[:\s]*([^,\n]+)',
            r'(?:weeds?\s+of|pests?\s+of|diseases?\s+of)\s+([^,\n]+)',
            r'(?:against|control|treat)\s+([^,\n]+)',
            # Specific patterns
            r'(?:rice|wheat|maize|cotton|tea|potato|tomato|brinjal|mango|banana|onion|garlic|chili|sugarcane|mustard|bean|bathua|helopeltis|bph|glh|ysb|hispa|bsfb|cut\s+worm|termites|aphid|jassid|bollworm|fruit\s+borer|pod\s+borer|shoot\s+borer|stem\s+borer|gall\s+midge|mosquito\s+bug|hairy\s+caterpillar|hopper|mite|spider|rust|blight|anthracnose|powdery\s+mildew|purple\s+blotch|red\s+rot|wilt|dieback|sigatoga|leaf\s+spot|sheath\s+blight)',
        ]

    def load_products(self):
        """Load products from JSON file"""
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                self.products = json.load(f)
            print(f"✅ Loaded {len(self.products)} products from {self.json_file_path}")
        except FileNotFoundError:
            print(f"❌ File {self.json_file_path} not found")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {e}")
            return False
        return True

    def save_products(self):
        """Save products to JSON file"""
        try:
            with open(self.json_file_path, 'w', encoding='utf-8') as f:
                json.dump(self.products, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved {len(self.products)} products to {self.json_file_path}")
            return True
        except Exception as e:
            print(f"❌ Error saving products: {e}")
            return False

    def extract_dosage_info(self, soup):
        """Enhanced dosage extraction with better patterns"""
        dosage_texts = []
        text_content = soup.get_text()
        
        # Look for dosage rate sections first
        dosage_sections = re.findall(r'dosage\s+rate[:\s]*([^\n]+)', text_content, re.IGNORECASE)
        for section in dosage_sections:
            if section.strip():
                dosage_texts.append(section.strip())
        
        # Look for specific dosage patterns
        for pattern in self.dosage_patterns:
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    if len(match) == 2:
                        dosage_texts.append(f"{match[0]} ml/{match[1]} L")
                    elif len(match) == 3:
                        dosage_texts.append(f"{match[0]} ml/{match[1]} L, {match[2]} ml/acre")
                else:
                    dosage_texts.append(match)
        
        # Look for list items in dosage sections
        dosage_lists = soup.find_all('div', class_='dosage-rate')
        for dosage_list in dosage_lists:
            ul = dosage_list.find('ul')
            if ul:
                for li in ul.find_all('li'):
                    dosage_text = li.get_text().strip()
                    if dosage_text and len(dosage_text) < 200:
                        dosage_texts.append(dosage_text)
        
        # Clean and return the best dosage
        cleaned_dosages = []
        for dosage in dosage_texts:
            dosage = dosage.strip()
            if dosage and len(dosage) < 200 and dosage not in cleaned_dosages:
                cleaned_dosages.append(dosage)
        
        return "; ".join(cleaned_dosages[:3])  # Return up to 3 dosage entries

    def extract_crops_pests_info(self, soup):
        """Enhanced crops and pests extraction"""
        crops_pests = []
        text_content = soup.get_text()
        
        # Look for crops and pests sections first
        crops_sections = re.findall(r'crops?\s*[&]\s*pests?[:\s]*([^\n]+)', text_content, re.IGNORECASE)
        for section in crops_sections:
            if section.strip():
                crops_pests.append(section.strip())
        
        # Look for list items in crops-pests sections
        crops_lists = soup.find_all('div', class_='crops-pests')
        for crops_list in crops_lists:
            ul = crops_list.find('ul')
            if ul:
                for li in ul.find_all('li'):
                    crop_text = li.get_text().strip()
                    if crop_text and len(crop_text) < 100:
                        crops_pests.append(crop_text)
        
        # Use enhanced patterns
        for pattern in self.crops_pests_patterns:
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            for match in matches:
                if match.strip() and len(match.strip()) < 100:
                    crops_pests.append(match.strip())
        
        # Clean and deduplicate
        cleaned_crops = []
        for crop in crops_pests:
            crop = crop.strip()
            if crop and crop not in cleaned_crops and len(crop) < 100:
                cleaned_crops.append(crop)
        
        return "; ".join(cleaned_crops[:5])  # Return up to 5 crop/pest entries

    def extract_description(self, soup):
        """Extract product description"""
        # Look for entry-content
        entry_content = soup.find('div', class_='entry-content')
        if entry_content:
            # Get first paragraph
            p = entry_content.find('p')
            if p:
                description = p.get_text().strip()
                if description and len(description) < 500:
                    return description
        
        # Look for general information
        general_info = soup.find('div', class_='general-information')
        if general_info:
            # Look for description in the general info
            text = general_info.get_text()
            if 'description' in text.lower():
                lines = text.split('\n')
                for line in lines:
                    if 'description' in line.lower() and len(line.strip()) > 20:
                        return line.strip()
        
        return ""

    def enhance_product(self, product):
        """Enhanced product data extraction"""
        product_url = product.get('product_url', '')
        if not product_url:
            return product
        
        print(f"📄 Processing: {product['product_name']}")
        
        try:
            response = self.session.get(product_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            enhanced_fields = []
            
            # Extract dosage if missing
            if not product.get('dosage'):
                dosage = self.extract_dosage_info(soup)
                if dosage:
                    product['dosage'] = dosage
                    enhanced_fields.append('dosage')
            
            # Extract crops_pests if missing
            if not product.get('crops_pests'):
                crops_pests = self.extract_crops_pests_info(soup)
                if crops_pests:
                    product['crops_pests'] = crops_pests
                    enhanced_fields.append('crops_pests')
            
            # Extract description if missing
            if not product.get('description'):
                description = self.extract_description(soup)
                if description:
                    product['description'] = description
                    enhanced_fields.append('description')
            
            if enhanced_fields:
                print(f"   ✅ Enhanced with: {', '.join(enhanced_fields)}")
            else:
                print(f"   ⚠️ No additional data found")
            
            # Small delay to be respectful
            time.sleep(0.5)
            
        except requests.RequestException as e:
            print(f"   ❌ Error fetching {product_url}: {e}")
        except Exception as e:
            print(f"   ❌ Error processing {product['product_name']}: {e}")
        
        return product

    def enhance_products_with_missing_data(self):
        """Enhance products that have missing dosage or crops_pests data"""
        print(f"\n🔍 Enhancing products with missing data...")
        
        products_to_enhance = []
        for product in self.products:
            if not product.get('dosage') or not product.get('crops_pests'):
                products_to_enhance.append(product)
        
        print(f"📊 Found {len(products_to_enhance)} products with missing data")
        
        for i, product in enumerate(products_to_enhance, 1):
            print(f"\n📄 Processing {i}/{len(products_to_enhance)}: {product['product_name']}")
            self.enhance_product(product)
        
        return len(products_to_enhance)

    def print_enhancement_summary(self):
        """Print summary of enhanced data"""
        print("\n" + "="*60)
        print("📊 ENHANCEMENT SUMMARY")
        print("="*60)
        print(f"Total Products: {len(self.products)}")
        
        # Count products with data
        with_dosage = sum(1 for p in self.products if p.get('dosage'))
        with_crops_pests = sum(1 for p in self.products if p.get('crops_pests'))
        with_description = sum(1 for p in self.products if p.get('description'))
        with_images = sum(1 for p in self.products if p.get('product_image') and 'images/' in p.get('product_image', ''))
        
        print(f"\n🔍 Enhanced Fields:")
        print(f"  dosage: {with_dosage}/{len(self.products)} ({with_dosage/len(self.products)*100:.1f}%)")
        print(f"  crops_pests: {with_crops_pests}/{len(self.products)} ({with_crops_pests/len(self.products)*100:.1f}%)")
        print(f"  description: {with_description}/{len(self.products)} ({with_description/len(self.products)*100:.1f}%)")
        print(f"  product_image: {with_images}/{len(self.products)} ({with_images/len(self.products)*100:.1f}%)")
        print("="*60)

def main():
    """Main function to run enhanced data extraction"""
    print("🚀 Enhanced McDonald Bangladesh Products Data Extractor")
    print("="*60)
    
    extractor = EnhancedDataExtractor()
    
    # Load products
    if not extractor.load_products():
        return
    
    # Print current status
    print("\n📊 Current Status:")
    extractor.print_enhancement_summary()
    
    # Enhance products with missing data
    enhanced_count = extractor.enhance_products_with_missing_data()
    
    # Print final summary
    print("\n📊 Final Enhancement Summary:")
    extractor.print_enhancement_summary()
    
    # Save enhanced products
    if extractor.save_products():
        print(f"\n✅ Enhanced {enhanced_count} products successfully!")
        print("📄 Check 'data/products_data.json' for the enhanced dataset.")
    else:
        print("\n❌ Failed to save enhanced products.")

if __name__ == "__main__":
    main()
