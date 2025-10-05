#!/usr/bin/env python3
"""
Script to download McDonald Bangladesh products page
URL: https://www.mcdonaldbd.com/our-products/
"""

import requests
import os
from datetime import datetime
from urllib.parse import urljoin, urlparse
import time

def download_page(url, output_dir="downloaded_content"):
    """
    Download a webpage and save it to a local file
    
    Args:
        url (str): The URL to download
        output_dir (str): Directory to save the downloaded content
    
    Returns:
        str: Path to the downloaded file
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Headers to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        print(f"Downloading: {url}")
        print("Please wait...")
        
        # Make the request
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Generate filename based on URL and timestamp
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.replace('www.', '')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{domain}_products_page_{timestamp}.html"
        filepath = os.path.join(output_dir, filename)
        
        # Save the content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"✅ Successfully downloaded!")
        print(f"📁 Saved to: {filepath}")
        print(f"📊 File size: {len(response.text):,} characters")
        print(f"🌐 Status code: {response.status_code}")
        
        return filepath
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error downloading the page: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def main():
    """Main function to download the McDonald Bangladesh products page"""
    url = "https://www.mcdonaldbd.com/our-products/"
    
    print("=" * 60)
    print("McDonald Bangladesh Products Page Downloader")
    print("=" * 60)
    
    # Download the page
    downloaded_file = download_page(url)
    
    if downloaded_file:
        print("\n" + "=" * 60)
        print("Download completed successfully!")
        print(f"File location: {downloaded_file}")
        print("=" * 60)
        
        # Ask if user wants to view the file
        try:
            view_file = input("\nWould you like to view the downloaded content? (y/n): ").lower().strip()
            if view_file in ['y', 'yes']:
                print("\n" + "-" * 60)
                print("FILE CONTENT PREVIEW (first 1000 characters):")
                print("-" * 60)
                with open(downloaded_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print(content[:1000])
                    if len(content) > 1000:
                        print("\n... (content truncated)")
                print("-" * 60)
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
    else:
        print("\n❌ Download failed. Please check the URL and try again.")

if __name__ == "__main__":
    main()
