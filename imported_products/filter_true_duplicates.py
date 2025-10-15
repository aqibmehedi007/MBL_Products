import json
import re
from collections import defaultdict

def normalize_text(text):
    """Normalize text for comparison - remove special characters, convert to lowercase"""
    if not text:
        return ""
    # Remove special characters and extra spaces
    normalized = re.sub(r'[^\w\s]', ' ', text.lower())
    # Remove extra whitespace
    normalized = ' '.join(normalized.split())
    return normalized

def is_english_bangla_variant(text1, text2):
    """Check if two texts are English-Bangla variants of the same product"""
    # Common patterns that might indicate English-Bangla variants
    # This is a basic check - you might need to refine this based on actual data
    
    # Remove common suffixes/prefixes for comparison
    suffixes_to_remove = ['ec', 'wp', 'sl', 'sp', 'wg', 'sc', 'gr', 'df', 'se', 'wdg']
    
    def clean_for_variant_check(text):
        text = text.lower()
        for suffix in suffixes_to_remove:
            text = text.replace(suffix, '')
        return text.strip()
    
    clean1 = clean_for_variant_check(text1)
    clean2 = clean_for_variant_check(text2)
    
    # If one is significantly shorter and contained in the other, might be variant
    if len(clean1) > len(clean2) * 2 or len(clean2) > len(clean1) * 2:
        return False
    
    # Check if they share significant common words (at least 60% similarity)
    words1 = set(clean1.split())
    words2 = set(clean2.split())
    
    if not words1 or not words2:
        return False
    
    common_words = words1.intersection(words2)
    similarity = len(common_words) / max(len(words1), len(words2))
    
    # If similarity is high but not identical, might be English-Bangla variant
    return 0.6 <= similarity < 1.0

def filter_true_duplicates():
    # Read the converted products
    with open('kb_converted_products.json', 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    print(f"Analyzing {len(products)} products for true duplicates...")
    
    # Create a composite key for each product (product_name + common_name)
    product_groups = defaultdict(list)
    true_duplicates = []
    unique_products = []
    
    for product in products:
        product_name = product.get('product_name', '')
        common_name = product.get('common_name', '')
        
        # Create composite key
        composite_key = f"{normalize_text(product_name)}|{normalize_text(common_name)}"
        product_groups[composite_key].append(product)
    
    # Process each group
    for composite_key, product_list in product_groups.items():
        if len(product_list) > 1:
            # These are true duplicates (same product name AND common name)
            true_duplicates.append({
                'composite_key': composite_key,
                'count': len(product_list),
                'products': product_list
            })
            
            # Keep only the first occurrence (or you could choose based on other criteria)
            unique_products.append(product_list[0])
        else:
            # Single product, no duplicates
            unique_products.append(product_list[0])
    
    # Print results
    print(f"\n=== TRUE DUPLICATES FOUND ===")
    print(f"Total duplicate groups: {len(true_duplicates)}")
    
    total_duplicate_products = 0
    for dup_group in true_duplicates:
        total_duplicate_products += dup_group['count']
        print(f"\nDuplicate Group: '{dup_group['composite_key']}' ({dup_group['count']} products)")
        for i, product in enumerate(dup_group['products']):
            status = "KEEP" if i == 0 else "REMOVE"
            print(f"  {status} - ID: {product['product_id']}, Name: '{product['product_name']}', Common: '{product['common_name']}'")
    
    print(f"\n=== SUMMARY ===")
    print(f"Original products: {len(products)}")
    print(f"True duplicate groups: {len(true_duplicates)}")
    print(f"Total duplicate products: {total_duplicate_products}")
    print(f"Unique products after filtering: {len(unique_products)}")
    print(f"Products removed: {total_duplicate_products - len(true_duplicates)}")
    
    # Save filtered products
    with open('kb_filtered_products.json', 'w', encoding='utf-8') as f:
        json.dump(unique_products, f, indent=2, ensure_ascii=False)
    
    # Save duplicate report
    duplicate_report = {
        'summary': {
            'original_products': len(products),
            'true_duplicate_groups': len(true_duplicates),
            'total_duplicate_products': total_duplicate_products,
            'unique_products_after_filtering': len(unique_products),
            'products_removed': total_duplicate_products - len(true_duplicates)
        },
        'true_duplicates': true_duplicates
    }
    
    with open('true_duplicates_report.json', 'w', encoding='utf-8') as f:
        json.dump(duplicate_report, f, indent=2, ensure_ascii=False)
    
    print(f"\nFiltered products saved to 'kb_filtered_products.json'")
    print(f"Duplicate report saved to 'true_duplicates_report.json'")
    
    return unique_products, true_duplicates

if __name__ == "__main__":
    filter_true_duplicates()
