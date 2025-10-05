#!/usr/bin/env python3
"""
McDonald Bangladesh Products Data Extraction Script
Extracts product information from the downloaded HTML file and individual product pages
"""

import json
import re
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
from datetime import datetime

class McDonaldProductsExtractor:
    def __init__(self, html_file_path, base_url="https://www.mcdonaldbd.com"):
        self.html_file_path = html_file_path
        self.base_url = base_url
        self.products = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    def load_html_file(self):
        """Load the downloaded HTML file"""
        try:
            with open(self.html_file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading HTML file: {e}")
            return None
    
    def extract_product_tables(self, html_content):
        """Extract all product tables from the HTML content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all tables
        tables = soup.find_all('table')
        product_tables = []
        
        for table in tables:
            # Check if this table contains product information
            rows = table.find_all('tr')
            if len(rows) > 1:  # Has header and data rows
                first_row = rows[0]
                headers = [th.get_text(strip=True) for th in first_row.find_all(['th', 'td'])]
                
                # Check if this looks like a product table
                if any(keyword in ' '.join(headers).lower() for keyword in ['product', 'name', 'common', 'reg']):
                    product_tables.append(table)
        
        return product_tables
    
    def extract_category_from_context(self, table):
        """Extract category information from the context around the table"""
        # Look for headings before the table
        current = table
        category = "Unknown"
        
        # Go up the DOM tree to find category headings
        for _ in range(10):  # Limit search depth
            current = current.previous_sibling
            if current is None:
                break
            
            if hasattr(current, 'get_text'):
                text = current.get_text(strip=True)
                if text and len(text) < 100:  # Likely a heading
                    # Check if it matches known categories
                    categories = [
                        'Herbicides / Weedicides',
                        'Insecticides', 
                        'Fungicides',
                        'Antibacterial Antibiotic',
                        'Acaricides / Miticides',
                        'Plant Growth Regulator (PGR)',
                        'Fertilizers (Macro & Micro)',
                        'Public Health Product (PHP)'
                    ]
                    
                    for cat in categories:
                        if cat.lower() in text.lower():
                            category = cat
                            break
                    
                    if category != "Unknown":
                        break
        
        return category
    
    def extract_products_from_table(self, table, category):
        """Extract product information from a single table"""
        products = []
        rows = table.find_all('tr')
        
        if len(rows) < 2:
            return products
        
        # Skip header row
        for row in rows[1:]:
            cells = row.find_all('td')
            if len(cells) >= 4:  # Ensure we have enough columns
                try:
                    # Extract data from each cell
                    serial_no = cells[0].get_text(strip=True)
                    
                    # Product name and link
                    product_link = cells[1].find('a')
                    if product_link:
                        product_name = product_link.get_text(strip=True)
                        product_url = product_link.get('href', '')
                    else:
                        product_name = cells[1].get_text(strip=True)
                        product_url = ''
                    
                    common_name = cells[2].get_text(strip=True)
                    reg_no = cells[3].get_text(strip=True)
                    origin = cells[4].get_text(strip=True) if len(cells) > 4 else ""
                    
                    # Create product ID
                    product_id = f"MBL-{serial_no.zfill(3)}"
                    
                    product = {
                        "product_id": product_id,
                        "product_name": product_name,
                        "product_image": "",  # Will be filled from individual page
                        "medicine_name": common_name,
                        "category_name": category,
                        "description": "",  # Will be filled from individual page
                        "indication": "",  # Will be filled from individual page
                        "dosage": "",  # Will be filled from individual page
                        "side_effect": "",  # Will be filled from individual page
                        "crops_pests": "",  # Will be filled from individual page
                        "product_tags": [],  # Will be generated
                        "product_price": "",  # Will be filled from individual page
                        "reg_no": reg_no,
                        "serial_no": serial_no,
                        "product_url": product_url,
                        "origin": origin,
                        "extraction_date": datetime.now().isoformat()
                    }
                    
                    products.append(product)
                    
                except Exception as e:
                    print(f"Error processing row: {e}")
                    continue
        
        return products
    
    def extract_all_products(self):
        """Extract all products from the HTML file"""
        html_content = self.load_html_file()
        if not html_content:
            return []
        
        print("🔍 Extracting product tables from HTML...")
        tables = self.extract_product_tables(html_content)
        print(f"📊 Found {len(tables)} product tables")
        
        all_products = []
        
        for i, table in enumerate(tables):
            category = self.extract_category_from_context(table)
            print(f"📋 Processing table {i+1}: {category}")
            
            products = self.extract_products_from_table(table, category)
            all_products.extend(products)
            print(f"   ✅ Extracted {len(products)} products")
        
        self.products = all_products
        return all_products
    
    def get_product_page_content(self, product_url):
        """Download individual product page content"""
        if not product_url:
            return None
        
        try:
            response = requests.get(product_url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"❌ Error downloading {product_url}: {e}")
            return None
    
    def extract_detailed_info(self, product_html):
        """Extract detailed information from individual product page"""
        soup = BeautifulSoup(product_html, 'html.parser')
        
        details = {
            "description": "",
            "indication": "",
            "dosage": "",
            "side_effect": "",
            "crops_pests": "",
            "product_image": "",
            "product_price": ""
        }
        
        # Look for common patterns in product pages
        # This is a basic implementation - can be enhanced based on actual page structure
        
        # Try to find description in content area
        content_area = soup.find('div', class_='entry-content') or soup.find('div', class_='content')
        if content_area:
            paragraphs = content_area.find_all('p')
            if paragraphs:
                details["description"] = paragraphs[0].get_text(strip=True)
        
        # Look for images
        img_tags = soup.find_all('img')
        for img in img_tags:
            src = img.get('src', '')
            if src and 'product' in src.lower():
                details["product_image"] = urljoin(self.base_url, src)
                break
        
        return details
    
    def enhance_products_with_details(self, max_products=None):
        """Enhance products with detailed information from individual pages"""
        if not self.products:
            print("❌ No products to enhance. Run extract_all_products() first.")
            return
        
        products_to_process = self.products[:max_products] if max_products else self.products
        
        print(f"🔍 Enhancing {len(products_to_process)} products with detailed information...")
        
        for i, product in enumerate(products_to_process):
            print(f"📄 Processing {i+1}/{len(products_to_process)}: {product['product_name']}")
            
            if product['product_url']:
                product_html = self.get_product_page_content(product['product_url'])
                if product_html:
                    details = self.extract_detailed_info(product_html)
                    
                    # Update product with detailed information
                    product.update(details)
                    
                    # Generate tags based on available information
                    tags = []
                    if product['medicine_name']:
                        tags.append(product['medicine_name'].lower())
                    if product['category_name']:
                        tags.append(product['category_name'].lower().split('/')[0].strip())
                    product['product_tags'] = tags
                
                # Be respectful with requests
                time.sleep(1)
            else:
                print(f"   ⚠️ No URL available for {product['product_name']}")
    
    def save_to_json(self, filename="products_data.json"):
        """Save extracted products to JSON file"""
        if not self.products:
            print("❌ No products to save. Run extract_all_products() first.")
            return
        
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        filepath = os.path.join("data", filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.products, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Saved {len(self.products)} products to {filepath}")
            
            # Also save by category
            self.save_by_category()
            
        except Exception as e:
            print(f"❌ Error saving to JSON: {e}")
    
    def save_by_category(self):
        """Save products grouped by category"""
        if not self.products:
            return
        
        categories = {}
        for product in self.products:
            category = product['category_name']
            if category not in categories:
                categories[category] = []
            categories[category].append(product)
        
        for category, products in categories.items():
            # Clean category name for filename
            safe_category = re.sub(r'[^\w\s-]', '', category).strip()
            safe_category = re.sub(r'[-\s]+', '_', safe_category)
            
            filename = f"{safe_category.lower()}.json"
            filepath = os.path.join("data", filename)
            
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(products, f, indent=2, ensure_ascii=False)
                print(f"💾 Saved {len(products)} {category} products to {filepath}")
            except Exception as e:
                print(f"❌ Error saving {category}: {e}")
    
    def print_summary(self):
        """Print a summary of extracted products"""
        if not self.products:
            print("❌ No products extracted yet.")
            return
        
        print("\n" + "="*60)
        print("📊 EXTRACTION SUMMARY")
        print("="*60)
        print(f"Total Products: {len(self.products)}")
        
        # Count by category
        categories = {}
        for product in self.products:
            category = product['category_name']
            categories[category] = categories.get(category, 0) + 1
        
        print("\n📋 Products by Category:")
        for category, count in sorted(categories.items()):
            print(f"  {category}: {count} products")
        
        print(f"\n🔗 Products with URLs: {sum(1 for p in self.products if p['product_url'])}")
        print(f"🖼️ Products with Images: {sum(1 for p in self.products if p['product_image'])}")
        print("="*60)

def main():
    """Main function to run the extraction process"""
    print("🚀 McDonald Bangladesh Products Data Extraction")
    print("="*60)
    
    # Find the downloaded HTML file
    html_files = []
    downloaded_dir = "downloaded_content"
    
    if os.path.exists(downloaded_dir):
        for file in os.listdir(downloaded_dir):
            if file.endswith('.html'):
                html_files.append(os.path.join(downloaded_dir, file))
    
    if not html_files:
        print("❌ No HTML files found in downloaded_content directory")
        return
    
    # Use the most recent HTML file
    html_file = max(html_files, key=os.path.getmtime)
    print(f"📄 Using HTML file: {html_file}")
    
    # Initialize extractor
    extractor = McDonaldProductsExtractor(html_file)
    
    # Extract all products
    products = extractor.extract_all_products()
    
    if not products:
        print("❌ No products extracted. Check the HTML file structure.")
        return
    
    # Print summary
    extractor.print_summary()
    
    # Ask user if they want to enhance with detailed information
    try:
        enhance = input("\n🔍 Do you want to enhance products with detailed information from individual pages? (y/n): ").lower().strip()
        if enhance in ['y', 'yes']:
            max_products = input("📊 How many products to enhance? (press Enter for all): ").strip()
            max_products = int(max_products) if max_products.isdigit() else None
            
            extractor.enhance_products_with_details(max_products)
            extractor.print_summary()
    except KeyboardInterrupt:
        print("\n⏹️ Enhancement cancelled by user.")
    
    # Save to JSON
    extractor.save_to_json()
    
    print("\n✅ Extraction completed!")

if __name__ == "__main__":
    main()
