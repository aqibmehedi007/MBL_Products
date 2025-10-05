#!/usr/bin/env python3
"""
Script to identify missing primary product images and generate AI prompts
"""

import json
import os

def find_missing_images():
    # Load products data
    with open('MBL/data/products_data.json', 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    # Get existing images
    images_dir = 'MBL/images'
    existing_images = set()
    
    if os.path.exists(images_dir):
        for filename in os.listdir(images_dir):
            if filename.startswith('MBL-') and filename.endswith('.jpg') and not '(' in filename:
                existing_images.add(filename)
    
    # Find missing primary images
    missing_images = []
    
    for product in products:
        product_id = product['product_id']
        expected_filename = f"{product_id}.jpg"
        
        if expected_filename not in existing_images:
            missing_images.append({
                'product_id': product_id,
                'product_name': product['product_name'],
                'medicine_name': product['medicine_name'],
                'category_name': product['category_name'],
                'filename': expected_filename
            })
    
    return missing_images

def generate_image_prompt(product):
    """Generate AI image prompt for a product"""
    
    # Base prompt structure
    base_prompt = "Professional agricultural product bottle, white plastic container with label"
    
    # Category-specific styling
    category_styles = {
        "Herbicides / Weedicides": "green and orange color scheme, weed control theme",
        "Insecticides": "blue and red color scheme, pest control theme", 
        "Fungicides": "purple and yellow color scheme, disease control theme",
        "Fertilizers (Macro & Micro)": "brown and gold color scheme, plant nutrition theme",
        "Plant Growth Regulator (PGR)": "pink and green color scheme, plant growth theme",
        "Bactericides": "teal and white color scheme, bacterial control theme",
        "Acaricides": "orange and black color scheme, mite control theme"
    }
    
    # Get category style
    category = product['category_name']
    style = category_styles.get(category, "professional agricultural theme")
    
    # Create detailed prompt
    prompt = f"{base_prompt}, {style}, "
    prompt += f"product name '{product['product_name']}' prominently displayed, "
    prompt += f"active ingredient '{product['medicine_name']}' shown, "
    prompt += "McDonald Bangladesh branding, "
    prompt += "clean white background, "
    prompt += "professional product photography, "
    prompt += "square format, "
    prompt += "high quality, detailed label design"
    
    return prompt

if __name__ == "__main__":
    missing_images = find_missing_images()
    
    print(f"Found {len(missing_images)} missing primary images:")
    
    # Create the text file with missing image prompts
    with open('MBL/missing_image_prompts.txt', 'w', encoding='utf-8') as f:
        f.write("MISSING PRIMARY PRODUCT IMAGES - AI GENERATION PROMPTS\n")
        f.write("=" * 60 + "\n\n")
        f.write("Instructions:\n")
        f.write("- Generate square format images (1024x1024 or 512x512 pixels)\n")
        f.write("- Use professional agricultural product photography style\n")
        f.write("- Ensure clear, readable text on labels\n")
        f.write("- Maintain consistent branding with McDonald Bangladesh\n\n")
        f.write("=" * 60 + "\n\n")
        
        for i, product in enumerate(missing_images, 1):
            prompt = generate_image_prompt(product)
            
            f.write(f"{i}. {product['filename']}\n")
            f.write(f"   Product: {product['product_name']}\n")
            f.write(f"   Active Ingredient: {product['medicine_name']}\n")
            f.write(f"   Category: {product['category_name']}\n")
            f.write(f"   AI Prompt: {prompt}\n\n")
    
    print(f"Created missing_image_prompts.txt with {len(missing_images)} missing images")
