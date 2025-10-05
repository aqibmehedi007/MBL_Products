# McDonald Bangladesh Products Data Collection Project

## Project Overview

This project aims to collect, organize, and enhance product information from McDonald Bangladesh's agricultural products catalog. The goal is to create a comprehensive database of agricultural products including herbicides, insecticides, fungicides, and other agricultural solutions.

## Data Source

**Primary Source:** [McDonald Bangladesh Products Page](https://www.mcdonaldbd.com/our-products/)

The website contains detailed product information organized into the following categories:
- Herbicides / Weedicides
- Insecticides  
- Fungicides
- Antibacterial Antibiotic
- Acaricides / Miticides
- Plant Growth Regulator (PGR)
- Fertilizers (Macro & Micro)
- Public Health Product (PHP)

## Project Goals

1. **Data Collection**: Extract all product information from the McDonald Bangladesh website
2. **Data Enhancement**: Use advanced AI and deep internet research to fill missing information
3. **Data Organization**: Structure the data in a standardized JSON format
4. **Continuous Improvement**: Keep polishing and updating the collected data

## Data Structure

The project will maintain product information in the following table structure:

| Field | Description | Example |
|-------|-------------|---------|
| `product_id` | Unique identifier for each product | "MBL-001" |
| `product_name` | Commercial product name | "Activar 25EC" |
| `product_image` | URL or path to product image | "https://..." |
| `medicine_name` | Active ingredient/common name | "Oxadiazon" |
| `category_name` | Product category | "Herbicides / Weedicides" |
| `description` | Detailed product description | "Pre-emergence herbicide..." |
| `indication` | What the product treats/prevents | "Broadleaf weeds control" |
| `dosage` | Application instructions | "2-3 ml per liter" |
| `side_effect` | Potential side effects | "May cause skin irritation" |
| `crops_pests` | Target crops and pests | "Rice, Wheat, Corn" |
| `product_tags` | Searchable tags | ["herbicide", "pre-emergence", "rice"] |
| `product_price` | Price information | "$25.50" |
| `reg_no` | Registration number | "AP - 698" |
| `serial_no` | Serial number from website | "1" |
| `product_price` | Additional price field | "$25.50" |

## Data Storage

- **Format**: JSON files (no SQL database initially)
- **Structure**: Organized by product categories
- **Updates**: Continuous data polishing and enhancement

## Project Structure

```
MBL/
├── README.md                           # This file
├── download_products_page.py          # Script to download website content
├── requirements.txt                    # Python dependencies
├── downloaded_content/                 # Downloaded HTML files
│   └── mcdonaldbd.com_products_page_*.html
├── data/                              # JSON data files (to be created)
│   ├── herbicides.json
│   ├── insecticides.json
│   ├── fungicides.json
│   └── all_products.json
├── scripts/                           # Data processing scripts (to be created)
│   ├── extract_products.py
│   ├── enhance_data.py
│   └── generate_missing_info.py
└── docs/                              # Documentation (to be created)
    ├── data_schema.md
    └── enhancement_guidelines.md
```

## Current Status

✅ **Completed:**
- Project setup and README creation
- Website download script
- Initial data source identification

🔄 **In Progress:**
- Data extraction from downloaded HTML
- JSON structure implementation

📋 **Next Steps:**
- Extract product tables from HTML
- Create JSON data structure
- Implement AI-powered data enhancement
- Generate missing product information

## Technology Stack

- **Python**: Primary programming language
- **Requests**: Web scraping and downloading
- **BeautifulSoup**: HTML parsing
- **JSON**: Data storage format
- **AI Integration**: For data enhancement and missing information generation

## Usage

1. **Download Website Content:**
   ```bash
   python download_products_page.py
   ```

2. **Extract Product Data:** (Coming soon)
   ```bash
   python scripts/extract_products.py
   ```

3. **Enhance Data with AI:** (Coming soon)
   ```bash
   python scripts/enhance_data.py
   ```

## Data Enhancement Strategy

The project will use advanced AI and deep internet research to:

1. **Fill Missing Information**: Generate descriptions, indications, dosage instructions
2. **Validate Data**: Cross-reference information with multiple sources
3. **Enhance Details**: Add comprehensive product information
4. **Standardize Format**: Ensure consistent data structure across all products

## Contributing

This project focuses on agricultural product data collection and enhancement. All contributions should maintain data accuracy and follow the established JSON schema.

## License

This project is for educational and research purposes. Please respect McDonald Bangladesh's website terms of use.

---

**Last Updated:** January 5, 2025  
**Project Status:** Active Development  
**Data Source:** [McDonald Bangladesh Products](https://www.mcdonaldbd.com/our-products/)
