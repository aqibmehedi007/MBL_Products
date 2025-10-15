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

def find_duplicate_products():
    # Read the converted products
    with open('kb_converted_products.json', 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    print(f"Analyzing {len(products)} products for duplicates...")
    
    # Group products by normalized names
    product_name_groups = defaultdict(list)
    common_name_groups = defaultdict(list)
    
    for product in products:
        product_name = product.get('product_name', '')
        common_name = product.get('common_name', '')
        
        # Normalize for grouping
        norm_product_name = normalize_text(product_name)
        norm_common_name = normalize_text(common_name)
        
        if norm_product_name:
            product_name_groups[norm_product_name].append(product)
        if norm_common_name:
            common_name_groups[norm_common_name].append(product)
    
    # Find duplicates by product name
    print("\n=== DUPLICATES BY PRODUCT NAME ===")
    product_name_duplicates = []
    for norm_name, product_list in product_name_groups.items():
        if len(product_list) > 1:
            # Check if these are English-Bangla variants
            is_variant = False
            for i in range(len(product_list)):
                for j in range(i + 1, len(product_list)):
                    if is_english_bangla_variant(
                        product_list[i]['product_name'], 
                        product_list[j]['product_name']
                    ):
                        is_variant = True
                        break
                if is_variant:
                    break
            
            if not is_variant:
                product_name_duplicates.append({
                    'normalized_name': norm_name,
                    'products': product_list
                })
    
    for dup_group in product_name_duplicates:
        print(f"\nDuplicate Product Name: '{dup_group['normalized_name']}'")
        for product in dup_group['products']:
            print(f"  - ID: {product['product_id']}, Name: '{product['product_name']}', Common: '{product['common_name']}'")
    
    # Find duplicates by common name
    print(f"\n=== DUPLICATES BY COMMON NAME ===")
    common_name_duplicates = []
    for norm_name, product_list in common_name_groups.items():
        if len(product_list) > 1:
            # Check if these are English-Bangla variants
            is_variant = False
            for i in range(len(product_list)):
                for j in range(i + 1, len(product_list)):
                    if is_english_bangla_variant(
                        product_list[i]['common_name'], 
                        product_list[j]['common_name']
                    ):
                        is_variant = True
                        break
                if is_variant:
                    break
            
            if not is_variant:
                common_name_duplicates.append({
                    'normalized_name': norm_name,
                    'products': product_list
                })
    
    for dup_group in common_name_duplicates:
        print(f"\nDuplicate Common Name: '{dup_group['normalized_name']}'")
        for product in dup_group['products']:
            print(f"  - ID: {product['product_id']}, Name: '{product['product_name']}', Common: '{product['common_name']}'")
    
    # Summary
    print(f"\n=== SUMMARY ===")
    print(f"Total products analyzed: {len(products)}")
    print(f"Duplicate product names (excluding variants): {len(product_name_duplicates)}")
    print(f"Duplicate common names (excluding variants): {len(common_name_duplicates)}")
    
    # Save detailed report
    report = {
        'summary': {
            'total_products': len(products),
            'duplicate_product_names': len(product_name_duplicates),
            'duplicate_common_names': len(common_name_duplicates)
        },
        'product_name_duplicates': product_name_duplicates,
        'common_name_duplicates': common_name_duplicates
    }
    
    with open('duplicate_products_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\nDetailed report saved to 'duplicate_products_report.json'")
    
    return report

if __name__ == "__main__":
    find_duplicate_products()
