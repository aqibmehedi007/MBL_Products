import os
import shutil
from PIL import Image
import glob

def process_images():
    """
    Process images by:
    1. Removing '.jpg' from filenames
    2. Resizing to 512x512 pixels
    3. Saving to a new folder
    """
    
    # Create output directory
    output_dir = "processed_images"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    
    # Get all PNG files in current directory
    image_files = glob.glob("*.png")
    
    if not image_files:
        print("No PNG files found in the current directory.")
        return
    
    print(f"Found {len(image_files)} PNG files to process...")
    
    processed_count = 0
    
    for image_file in image_files:
        try:
            # Remove '.jpg' from filename if it exists
            new_filename = image_file.replace('.jpg', '')
            
            # Open the image
            with Image.open(image_file) as img:
                # Convert to RGB if necessary (for PNG with transparency)
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Create a white background
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize to 512x512
                resized_img = img.resize((512, 512), Image.Resampling.LANCZOS)
                
                # Save to output directory
                output_path = os.path.join(output_dir, new_filename)
                resized_img.save(output_path, 'PNG', quality=95)
                
                print(f"Processed: {image_file} -> {new_filename} (512x512)")
                processed_count += 1
                
        except Exception as e:
            print(f"Error processing {image_file}: {str(e)}")
    
    print(f"\nProcessing complete! {processed_count} images processed and saved to '{output_dir}' folder.")

if __name__ == "__main__":
    process_images()
