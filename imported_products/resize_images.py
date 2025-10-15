#!/usr/bin/env python3
"""
Image Resizer Script
Resizes all images in the product-image folder to 512x512 pixels
and saves them in a new 'images' folder.
"""

import os
import sys
from PIL import Image
import glob

def resize_image(input_path, output_path, size=(512, 512)):
    """
    Resize an image to the specified size while maintaining aspect ratio.
    
    Args:
        input_path (str): Path to the input image
        output_path (str): Path to save the resized image
        size (tuple): Target size (width, height)
    """
    try:
        # Open the image
        with Image.open(input_path) as img:
            # Convert to RGB if necessary (handles RGBA, P mode, etc.)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize with high-quality resampling
            resized_img = img.resize(size, Image.Resampling.LANCZOS)
            
            # Save the resized image
            resized_img.save(output_path, 'JPEG', quality=95, optimize=True)
            
        return True
    except Exception as e:
        print(f"Error processing {input_path}: {str(e)}")
        return False

def main():
    # Define paths
    input_folder = "product-image"
    output_folder = "images"
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")
    
    # Supported image extensions
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.tif']
    
    # Find all image files in the input folder and subfolders
    image_files = []
    for ext in image_extensions:
        # Search in main folder
        image_files.extend(glob.glob(os.path.join(input_folder, ext)))
        # Search in subfolders
        image_files.extend(glob.glob(os.path.join(input_folder, "**", ext), recursive=True))
    
    if not image_files:
        print(f"No image files found in {input_folder}")
        return
    
    print(f"Found {len(image_files)} image files to process...")
    
    # Process each image
    successful = 0
    failed = 0
    
    for input_path in image_files:
        # Get relative path from input folder
        rel_path = os.path.relpath(input_path, input_folder)
        
        # Create output path, maintaining folder structure
        output_path = os.path.join(output_folder, rel_path)
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Change extension to .jpg for consistency
        name, _ = os.path.splitext(output_path)
        output_path = name + '.jpg'
        
        print(f"Processing: {rel_path}")
        
        if resize_image(input_path, output_path):
            successful += 1
            print(f"  ✓ Resized and saved to: {output_path}")
        else:
            failed += 1
            print(f"  ✗ Failed to process: {rel_path}")
    
    print(f"\nProcessing complete!")
    print(f"Successfully processed: {successful} images")
    print(f"Failed to process: {failed} images")
    print(f"All resized images saved in: {output_folder}/")

if __name__ == "__main__":
    main()
