#!/usr/bin/env python3
"""
Enhanced McDonald Bangladesh Products Data Extraction Script
Extracts detailed information from individual product pages including dosage, crops & pests, and images
Updated to handle proper HTML structure
"""

import json
import re
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
from datetime import datetime
from pathlib import Path

class EnhancedProductExtractor:
    def __init__(self, json_file_path="data/products_data.json", base_url="https://www.mcdonaldbd.com"):
        self.json_file_path = json_file_path
        self.base_url = base_url
        self.products = []
        self.images_dir = Path("images")
        self.images_dir.mkdir(exist_ok=True)
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        # Enhanced category mapping based on active ingredients and product names
        self.category_mapping = {
            'herbicide': 'Herbicides / Weedicides',
            'weedicide': 'Herbicides / Weedicides',
            'weed': 'Herbicides / Weedicides',
            'oxadiazon': 'Herbicides / Weedicides',
            'glyphosate': 'Herbicides / Weedicides',
            'paraquat': 'Herbicides / Weedicides',
            'pendimethalin': 'Herbicides / Weedicides',
            'pyrazosulfuran': 'Herbicides / Weedicides',
            'bensulfuron': 'Herbicides / Weedicides',
            'acetachlor': 'Herbicides / Weedicides',
            'quizalofop': 'Herbicides / Weedicides',
            'carfentrazone': 'Herbicides / Weedicides',
            'isoproturon': 'Herbicides / Weedicides',
            'insecticide': 'Insecticides',
            'imidacloprid': 'Insecticides',
            'abamectin': 'Insecticides',
            'fipronil': 'Insecticides',
            'cartap': 'Insecticides',
            'carbaryl': 'Insecticides',
            'diazinon': 'Insecticides',
            'cypermethrin': 'Insecticides',
            'pymetrozine': 'Insecticides',
            'thiamethoxam': 'Insecticides',
            'lufenuron': 'Insecticides',
            'emamectin': 'Insecticides',
            'acetamiprid': 'Insecticides',
            'indoxacarb': 'Insecticides',
            'profenoso': 'Insecticides',
            'lambda-cyhalothrin': 'Insecticides',
            'beta-cyfluthrin': 'Insecticides',
            'fungicide': 'Fungicides',
            'carbendazim': 'Fungicides',
            'mancozeb': 'Fungicides',
            'hexaconazole': 'Fungicides',
            'copper': 'Fungicides',
            'sulphur': 'Fungicides',
            'cymoxanil': 'Fungicides',
            'azoxystrobin': 'Fungicides',
            'difenoconazole': 'Fungicides',
            'tebuconazole': 'Fungicides',
            'trifloxystrobin': 'Fungicides',
            'iprodion': 'Fungicides',
            'propiconazole': 'Fungicides',
            'kasugamycin': 'Fungicides',
            'boscalid': 'Fungicides',
            'fenoxanil': 'Fungicides',
            'tricyclazole': 'Fungicides',
            'cyprodinil': 'Fungicides',
            'fludioxonil': 'Fungicides',
            'carboxin': 'Fungicides',
            'thiram': 'Fungicides',
            'antibacterial': 'Antibacterial Antibiotic',
            'antibiotic': 'Antibacterial Antibiotic',
            'streptomycin': 'Antibacterial Antibiotic',
            'tetracycline': 'Antibacterial Antibiotic',
            'acaricide': 'Acaricides / Miticides',
            'miticide': 'Acaricides / Miticides',
            'propergite': 'Acaricides / Miticides',
            'fenpyroximate': 'Acaricides / Miticides',
            'fenazaquin': 'Acaricides / Miticides',
            'pgr': 'Plant Growth Regulator (PGR)',
            'growth regulator': 'Plant Growth Regulator (PGR)',
            'triacontanol': 'Plant Growth Regulator (PGR)',
            'brassinolide': 'Plant Growth Regulator (PGR)',
            'fertilizer': 'Fertilizers (Macro & Micro)',
            'zinc': 'Fertilizers (Macro & Micro)',
            'magnesium': 'Fertilizers (Macro & Micro)',
            'boron': 'Fertilizers (Macro & Micro)',
            'sulphate': 'Fertilizers (Macro & Micro)',
            'chelated': 'Fertilizers (Macro & Micro)',
            'public health': 'Public Health Product (PHP)'
        }
    
    def load_products(self):
        """Load existing products from JSON file"""
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                self.products = json.load(f)
            print(f"✅ Loaded {len(self.products)} products from {self.json_file_path}")
            return True
        except Exception as e:
            print(f"❌ Error loading products: {e}")
            return False
    
    def save_products(self):
        """Save enhanced products to JSON file"""
        try:
            with open(self.json_file_path, 'w', encoding='utf-8') as f:
                json.dump(self.products, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved {len(self.products)} enhanced products to {self.json_file_path}")
            return True
        except Exception as e:
            print(f"❌ Error saving products: {e}")
            return False
    
    def get_product_page_content(self, product_url):
        """Download individual product page content"""
        if not product_url:
            return None
        
        try:
            print(f"📄 Downloading: {product_url}")
            response = requests.get(product_url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"❌ Error downloading {product_url}: {e}")
            return None
    
    def extract_structured_info(self, soup):
        """Extract structured information from the HTML"""
        details = {
            "dosage": "",
            "crops_pests": ""
        }
        
        # Extract dosage information from structured lists
        dosage_section = soup.find('div', class_='dosage-rate')
        if dosage_section:
            dosage_list = dosage_section.find('ul')
            if dosage_list:
                dosage_items = dosage_list.find_all('li')
                dosage_texts = [item.get_text(strip=True) for item in dosage_items]
                details["dosage"] = "; ".join(dosage_texts)
        
        # Extract crops & pests information from structured lists
        crops_section = soup.find('div', class_='crops-pests')
        if crops_section:
            crops_list = crops_section.find('ul')
            if crops_list:
                crops_items = crops_list.find_all('li')
                crops_texts = [item.get_text(strip=True) for item in crops_items]
                details["crops_pests"] = "; ".join(crops_texts)
        
        return details
    
    def extract_all_images(self, soup, product_id):
        """Extract all images from the product page"""
        images = []
        
        # Extract primary product image (main product photo)
        primary_img = soup.find('img', class_='wp-post-image')
        if primary_img:
            src = primary_img.get('src', '')
            if src:
                # Get the highest resolution version
                srcset = primary_img.get('srcset', '')
                if srcset:
                    # Parse srcset to get the highest resolution
                    srcset_parts = srcset.split(',')
                    highest_res = srcset_parts[-1].strip().split(' ')[0]
                    if highest_res:
                        src = highest_res
                
                local_path = self.download_product_image(src, product_id)
                if local_path:
                    images.append(local_path)
        
        # Extract additional images from entry-content
        content_area = soup.find('div', class_='entry-content')
        if content_area:
            additional_imgs = content_area.find_all('img')
            for i, img in enumerate(additional_imgs):
                src = img.get('src', '')
                if src and 'wp-content/uploads' in src:
                    # Create filename with index for additional images
                    filename = f"{product_id}_({i+1})"
                    local_path = self.download_product_image(src, filename)
                    if local_path:
                        images.append(local_path)
        
        return images
    
    def download_product_image(self, image_url, product_id):
        """Download product image and save locally"""
        try:
            response = requests.get(image_url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            # Determine file extension
            content_type = response.headers.get('content-type', '')
            if 'jpeg' in content_type or 'jpg' in content_type:
                ext = 'jpg'
            elif 'png' in content_type:
                ext = 'png'
            elif 'webp' in content_type:
                ext = 'webp'
            else:
                # Try to determine from URL
                if image_url.lower().endswith('.png'):
                    ext = 'png'
                elif image_url.lower().endswith('.webp'):
                    ext = 'webp'
                else:
                    ext = 'jpg'  # Default
            
            # Create filename
            filename = f"{product_id}.{ext}"
            filepath = self.images_dir / filename
            
            # Save image
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"🖼️ Downloaded image: {filename}")
            return f"images/{filename}"
            
        except Exception as e:
            print(f"❌ Error downloading image {image_url}: {e}")
            return None
    
    def classify_category(self, product):
        """Classify product category based on name and active ingredient"""
        product_name = product.get('product_name', '').lower()
        medicine_name = product.get('medicine_name', '').lower()
        
        # Check for category keywords
        text_to_check = f"{product_name} {medicine_name}"
        
        for keyword, category in self.category_mapping.items():
            if keyword in text_to_check:
                return category
        
        return "Unknown"
    
    def enhance_products(self, max_products=None, start_index=0):
        """Enhance products with detailed information from individual pages"""
        if not self.products:
            print("❌ No products to enhance. Load products first.")
            return
        
        products_to_process = self.products[start_index:]
        if max_products:
            products_to_process = products_to_process[:max_products]
        
        print(f"🔍 Enhancing {len(products_to_process)} products with detailed information...")
        
        enhanced_count = 0
        for i, product in enumerate(products_to_process):
            current_index = start_index + i
            print(f"\n📄 Processing {current_index + 1}/{len(self.products)}: {product['product_name']}")
            
            # Classify category
            category = self.classify_category(product)
            if category != "Unknown":
                product['category_name'] = category
                print(f"   📋 Category: {category}")
            
            if product.get('product_url'):
                product_html = self.get_product_page_content(product['product_url'])
                if product_html:
                    soup = BeautifulSoup(product_html, 'html.parser')
                    
                    # Extract structured information
                    structured_info = self.extract_structured_info(soup)
                    product.update(structured_info)
                    
                    # Extract description
                    content_area = soup.find('div', class_='entry-content')
                    if content_area:
                        paragraphs = content_area.find_all('p')
                        if paragraphs:
                            product['description'] = paragraphs[0].get_text(strip=True)
                    
                    # Extract and download all images
                    images = self.extract_all_images(soup, product['product_id'])
                    if images:
                        product['product_image'] = images[0]  # Primary image
                        if len(images) > 1:
                            product['additional_images'] = images[1:]
                    
                    # Generate enhanced tags
                    tags = []
                    if product['medicine_name']:
                        tags.append(product['medicine_name'].lower())
                    if product['category_name']:
                        tags.append(product['category_name'].lower().split('/')[0].strip())
                    if product['crops_pests']:
                        crops = product['crops_pests'].lower().split(';')
                        tags.extend([crop.strip() for crop in crops[:3]])
                    
                    product['product_tags'] = list(set(tags))  # Remove duplicates
                    
                    enhanced_count += 1
                    print(f"   ✅ Enhanced with: {len([k for k, v in structured_info.items() if v])} fields")
                    if images:
                        print(f"   🖼️ Downloaded {len(images)} images")
                
                # Be respectful with requests
                time.sleep(2)
            else:
                print(f"   ⚠️ No URL available for {product['product_name']}")
        
        print(f"\n🎉 Enhanced {enhanced_count} products successfully!")
    
    def print_enhancement_summary(self):
        """Print summary of enhanced products"""
        if not self.products:
            print("❌ No products to summarize.")
            return
        
        print("\n" + "="*60)
        print("📊 ENHANCEMENT SUMMARY")
        print("="*60)
        
        # Count by category
        categories = {}
        for product in self.products:
            category = product['category_name']
            categories[category] = categories.get(category, 0) + 1
        
        print(f"Total Products: {len(self.products)}")
        print("\n📋 Products by Category:")
        for category, count in sorted(categories.items()):
            print(f"  {category}: {count} products")
        
        # Count enhanced fields
        enhanced_fields = {
            'description': sum(1 for p in self.products if p.get('description')),
            'dosage': sum(1 for p in self.products if p.get('dosage')),
            'crops_pests': sum(1 for p in self.products if p.get('crops_pests')),
            'product_image': sum(1 for p in self.products if p.get('product_image')),
            'additional_images': sum(1 for p in self.products if p.get('additional_images'))
        }
        
        print(f"\n🔍 Enhanced Fields:")
        for field, count in enhanced_fields.items():
            percentage = (count / len(self.products)) * 100
            print(f"  {field}: {count}/{len(self.products)} ({percentage:.1f}%)")
        
        print("="*60)

def main():
    """Main function to run the enhancement process"""
    print("🚀 McDonald Bangladesh Products Enhancement")
    print("="*60)
    
    # Initialize extractor
    extractor = EnhancedProductExtractor()
    
    # Load existing products
    if not extractor.load_products():
        return
    
    # Print current status
    extractor.print_enhancement_summary()
    
    # Ask user for enhancement options
    try:
        enhance_all = input("\n🔍 Do you want to enhance all products? (y/n): ").lower().strip()
        
        if enhance_all in ['y', 'yes']:
            max_products = input("📊 How many products to enhance? (press Enter for all): ").strip()
            max_products = int(max_products) if max_products.isdigit() else None
            
            start_index = input("📊 Start from which product? (press Enter for 0): ").strip()
            start_index = int(start_index) if start_index.isdigit() else 0
            
            extractor.enhance_products(max_products, start_index)
            
            # Print final summary
            extractor.print_enhancement_summary()
            
            # Save enhanced data
            extractor.save_products()
            
        else:
            print("⏹️ Enhancement cancelled by user.")
            
    except KeyboardInterrupt:
        print("\n⏹️ Enhancement cancelled by user.")
        # Save partial progress
        extractor.save_products()
    
    print("\n✅ Enhancement process completed!")

if __name__ == "__main__":
    main()
