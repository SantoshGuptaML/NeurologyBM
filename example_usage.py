#!/usr/bin/env python3
"""
Simple example showing how to use the NeurologyBM downloaders.

This script demonstrates the basic usage of both PMC and PubMed downloaders.
"""

print("=" * 80)
print("NeurologyBM - Example Usage")
print("=" * 80)

print("""
This repository provides tools to download neurology research papers and abstracts
with proper licensing for non-commercial training purposes.

### Quick Start

1. Install dependencies:
   pip install -r requirements.txt

2. Download PubMed abstracts (public domain - free for any use):
   python download_pubmed_abstracts.py \\
       --email your.email@example.com \\
       --query "neurology OR neurological" \\
       --max-results 1000

3. Download PMC papers (Open Access with various licenses):
   python download_pmc_papers.py \\
       --email your.email@example.com \\
       --query "neurology OR neurological" \\
       --max-results 100

### Licensing Summary

PubMed Abstracts:
  ✅ Public Domain
  ✅ No restrictions
  ✅ Perfect for commercial and non-commercial ML training

PMC Open Access Papers:
  ⚠️  Various licenses (CC-BY, CC-BY-NC, etc.)
  ✅ All allow non-commercial use
  ⚠️  Check individual licenses for commercial use
  ✅ License info included in metadata files

### Example Queries for Neurology Research

# Alzheimer's Disease
--query "alzheimer disease[MeSH] OR alzheimer's[Title/Abstract]"

# Parkinson's Disease  
--query "parkinson disease[MeSH] OR parkinsons[Title/Abstract]"

# Epilepsy
--query "epilepsy[MeSH] OR seizure[MeSH]"

# Multiple Sclerosis
--query "multiple sclerosis[MeSH]"

# Brain Imaging
--query "(neurology[MeSH] OR brain[MeSH]) AND (MRI[Title/Abstract] OR neuroimaging[MeSH])"

# Recent papers (last 5 years)
--query "neurology[MeSH] AND 2019:2024[PDAT]"

### Output Structure

After downloading, you'll have:

data/
├── pubmed_abstracts/
│   ├── abstracts_20231224_120000.json  # All abstracts in JSON format
│   ├── abstracts_20231224_120000.csv   # All abstracts in CSV format
│   └── download_summary.json           # Metadata about the download
├── pmc_papers/
│   ├── PMC12345.xml                    # Full-text article
│   ├── PMC12345_metadata.json          # Article metadata with license
│   ├── PMC67890.xml
│   ├── PMC67890_metadata.json
│   └── download_summary.json

### For More Information

- README.md - Full documentation
- LICENSE_INFO.md - Detailed licensing information
- LICENSE - Software license

### Questions?

Open an issue at: https://github.com/SantoshGuptaML/NeurologyBM
""")

print("=" * 80)
