# NeurologyBM

A toolkit for downloading neurology-related research papers and abstracts from PubMed Central (PMC) and PubMed, with proper licensing for non-commercial training purposes.

## Overview

This repository provides tools to download:
- **PMC Papers**: Full-text articles from PubMed Central Open Access Subset
- **PubMed Abstracts**: Abstracts from PubMed database

All downloaded data includes proper licensing information and is suitable for training machine learning models for non-commercial purposes.

## Features

- ✅ Downloads from PMC Open Access Subset (licensed for reuse)
- ✅ Downloads PubMed abstracts (public domain)
- ✅ Respects NCBI API rate limits
- ✅ Includes metadata and license information
- ✅ Multiple output formats (JSON, CSV, XML, TXT)
- ✅ Batch downloading with progress tracking
- ✅ Neurology-focused by default

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/SantoshGuptaML/NeurologyBM.git
cd NeurologyBM
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Downloading PMC Papers

PMC Open Access papers are full-text articles with various Creative Commons licenses that allow reuse.

```bash
# Basic usage
python download_pmc_papers.py --email your.email@example.com --query "neurology OR neurological"

# Download more papers
python download_pmc_papers.py --email your.email@example.com --query "neurology" --max-results 500

# Use API key for higher rate limits (10 req/sec vs 3 req/sec)
python download_pmc_papers.py --email your.email@example.com --api-key YOUR_NCBI_API_KEY --query "neurology"

# Download specific topics
python download_pmc_papers.py --email your.email@example.com --query "alzheimer OR parkinson OR epilepsy"

# Download as PDF (when available)
python download_pmc_papers.py --email your.email@example.com --query "neurology" --format pdf
```

### Downloading PubMed Abstracts

PubMed abstracts are in the public domain and can be freely used for any purpose.

```bash
# Basic usage
python download_pubmed_abstracts.py --email your.email@example.com --query "neurology OR neurological"

# Download more abstracts
python download_pubmed_abstracts.py --email your.email@example.com --query "neurology" --max-results 5000

# Use API key for faster downloads
python download_pubmed_abstracts.py --email your.email@example.com --api-key YOUR_NCBI_API_KEY --query "neurology"

# Save in multiple formats
python download_pubmed_abstracts.py --email your.email@example.com --query "neurology" --formats json csv txt

# Search with MeSH terms
python download_pubmed_abstracts.py --email your.email@example.com --query "neurology[MeSH] OR brain diseases[MeSH]"
```

### Getting an NCBI API Key (Optional but Recommended)

An API key allows for higher rate limits (10 requests/second instead of 3).

1. Create an NCBI account at https://www.ncbi.nlm.nih.gov/account/
2. Go to Settings → API Key Management
3. Create a new API key
4. Use the key with `--api-key YOUR_KEY` parameter

## Output Structure

### PMC Papers

```
data/pmc_papers/
├── PMC12345.xml              # Full-text article in XML format
├── PMC12345_metadata.json    # Article metadata with license info
├── PMC67890.xml
├── PMC67890_metadata.json
└── download_summary.json     # Summary of download session
```

### PubMed Abstracts

```
data/pubmed_abstracts/
├── abstracts_20231224_120000.json    # All abstracts in JSON
├── abstracts_20231224_120000.csv     # All abstracts in CSV
├── txt_20231224_120000/              # Individual text files
│   ├── PMID_12345678.txt
│   └── PMID_87654321.txt
└── download_summary.json             # Summary of download session
```

## License Information

### PMC Open Access Papers
- Papers downloaded from PMC Open Access Subset include license information in their metadata
- Most use Creative Commons licenses (CC-BY, CC-BY-NC, etc.)
- License details are included in each paper's metadata file
- **Generally allowed**: Non-commercial research, education, and training
- See individual paper licenses for specific terms

### PubMed Abstracts
- **Public Domain**: PubMed abstracts are NOT copyrighted
- Can be freely used for ANY purpose (commercial or non-commercial)
- No attribution required (though recommended for academic use)
- Reference: https://www.ncbi.nlm.nih.gov/home/about/policies/

## NCBI Usage Guidelines

This tool respects NCBI's usage guidelines:
- Rate limiting: 3 requests/second (or 10/second with API key)
- Email required for API access
- No unauthorized bulk downloading outside of the tools provided

For more information: https://www.ncbi.nlm.nih.gov/home/about/policies/

## Example Queries

### Neurology Topics
```bash
# General neurology
--query "neurology[MeSH] OR neurological diseases[MeSH]"

# Alzheimer's disease
--query "alzheimer disease[MeSH] OR alzheimer's[Title/Abstract]"

# Parkinson's disease
--query "parkinson disease[MeSH] OR parkinsons[Title/Abstract]"

# Epilepsy
--query "epilepsy[MeSH] OR seizure[MeSH]"

# Multiple Sclerosis
--query "multiple sclerosis[MeSH] OR MS[Title]"

# Brain imaging
--query "(neurology[MeSH] OR brain[MeSH]) AND (MRI[Title/Abstract] OR neuroimaging[MeSH])"

# Recent papers (last 5 years)
--query "neurology[MeSH] AND 2019:2024[PDAT]"
```

## Troubleshooting

### Rate Limiting Errors
If you encounter rate limiting errors:
1. Get an NCBI API key (see above)
2. Reduce `--max-results` to download in smaller batches
3. Wait a few minutes before retrying

### Connection Issues
If downloads fail:
1. Check your internet connection
2. Verify your email address is correct
3. Try reducing batch size or number of results
4. Check NCBI service status at https://www.ncbi.nlm.nih.gov/

### No Abstracts Found
If searches return no results:
1. Try broader search terms
2. Verify query syntax with PubMed web interface
3. Remove special characters or filters

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Citation

If you use this tool in your research, please cite:
```
NeurologyBM: A toolkit for downloading neurology research data
GitHub: https://github.com/SantoshGuptaML/NeurologyBM
```

## Disclaimer

This tool is for research and educational purposes. Users are responsible for:
- Complying with NCBI usage policies
- Respecting individual paper licenses
- Proper attribution in publications
- Not violating copyright or terms of service

## Contact

For questions or issues, please open a GitHub issue.

## Acknowledgments

- Data provided by NCBI's PubMed and PMC databases
- Built using BioPython and NCBI E-utilities API
