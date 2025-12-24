#!/usr/bin/env python3
"""
PMC Paper Downloader for Neurology Research

This script downloads full-text papers from PubMed Central (PMC) Open Access Subset.
The PMC Open Access Subset contains articles that are licensed for reuse, including 
for non-commercial purposes like model training.

License Information:
- PMC Open Access articles are available under various Creative Commons licenses
- All downloaded articles include license information in their metadata
- This script respects NCBI's usage guidelines and rate limits

Usage:
    python download_pmc_papers.py --query "neurology OR neurological" --max-results 100

Author: NeurologyBM Project
"""

import argparse
import json
import os
import time
from pathlib import Path
from typing import List, Dict, Optional
from xml.etree import ElementTree as ET

try:
    from Bio import Entrez
    import requests
    from tqdm import tqdm
except ImportError:
    print("Error: Required packages not installed.")
    print("Please install dependencies: pip install -r requirements.txt")
    exit(1)


class PMCDownloader:
    """Downloads papers from PubMed Central Open Access Subset."""
    
    def __init__(self, email: str, api_key: Optional[str] = None, output_dir: str = "data/pmc_papers"):
        """
        Initialize the PMC downloader.
        
        Args:
            email: Your email address (required by NCBI)
            api_key: Optional NCBI API key for higher rate limits
            output_dir: Directory to save downloaded papers
        """
        self.email = email
        self.api_key = api_key
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Configure Entrez
        Entrez.email = email
        if api_key:
            Entrez.api_key = api_key
        
        # Rate limiting: 3 requests/second without API key, 10/second with API key
        self.request_delay = 0.34 if not api_key else 0.11
        
    def search_pmc(self, query: str, max_results: int = 100) -> List[str]:
        """
        Search PMC for papers matching the query.
        
        Args:
            query: Search query (e.g., "neurology[MeSH] AND free fulltext[filter]")
            max_results: Maximum number of results to return
            
        Returns:
            List of PMC IDs
        """
        print(f"Searching PMC with query: {query}")
        
        # Add filter for Open Access articles
        full_query = f"{query} AND open access[filter]"
        
        try:
            handle = Entrez.esearch(
                db="pmc",
                term=full_query,
                retmax=max_results,
                sort="relevance"
            )
            record = Entrez.read(handle)
            handle.close()
            
            pmc_ids = record.get("IdList", [])
            print(f"Found {len(pmc_ids)} open access articles")
            return pmc_ids
            
        except Exception as e:
            print(f"Error searching PMC: {e}")
            return []
    
    def get_article_metadata(self, pmc_id: str) -> Optional[Dict]:
        """
        Fetch metadata for a PMC article.
        
        Args:
            pmc_id: PMC ID (without 'PMC' prefix if numeric)
            
        Returns:
            Dictionary with article metadata including license info
        """
        time.sleep(self.request_delay)
        
        try:
            handle = Entrez.efetch(
                db="pmc",
                id=pmc_id,
                rettype="xml",
                retmode="xml"
            )
            xml_content = handle.read()
            handle.close()
            
            # Parse XML to extract metadata
            root = ET.fromstring(xml_content)
            
            metadata = {
                "pmc_id": pmc_id,
                "title": "",
                "abstract": "",
                "license": "Unknown",
                "license_url": "",
                "authors": [],
                "journal": "",
                "year": "",
                "doi": ""
            }
            
            # Extract article metadata from XML
            article = root.find(".//article")
            if article is not None:
                # Title
                title_elem = article.find(".//article-title")
                if title_elem is not None:
                    metadata["title"] = "".join(title_elem.itertext()).strip()
                
                # Abstract
                abstract_elem = article.find(".//abstract")
                if abstract_elem is not None:
                    metadata["abstract"] = "".join(abstract_elem.itertext()).strip()
                
                # License information
                license_elem = article.find(".//license")
                if license_elem is not None:
                    license_type = license_elem.get("license-type", "")
                    license_url = license_elem.get("{http://www.w3.org/1999/xlink}href", "")
                    license_text = "".join(license_elem.itertext()).strip()
                    
                    metadata["license"] = license_type or license_text
                    metadata["license_url"] = license_url
                
                # Authors
                contrib_group = article.find(".//contrib-group")
                if contrib_group is not None:
                    for contrib in contrib_group.findall(".//contrib[@contrib-type='author']"):
                        surname = contrib.find(".//surname")
                        given_names = contrib.find(".//given-names")
                        if surname is not None:
                            author = surname.text or ""
                            if given_names is not None:
                                author = f"{given_names.text} {author}"
                            metadata["authors"].append(author.strip())
                
                # Journal
                journal_elem = article.find(".//journal-title")
                if journal_elem is not None:
                    metadata["journal"] = journal_elem.text or ""
                
                # Year
                year_elem = article.find(".//pub-date/year")
                if year_elem is not None:
                    metadata["year"] = year_elem.text or ""
                
                # DOI
                doi_elem = article.find(".//article-id[@pub-id-type='doi']")
                if doi_elem is not None:
                    metadata["doi"] = doi_elem.text or ""
            
            return metadata
            
        except Exception as e:
            print(f"Error fetching metadata for PMC{pmc_id}: {e}")
            return None
    
    def download_paper(self, pmc_id: str, format: str = "xml") -> bool:
        """
        Download a single paper from PMC.
        
        Args:
            pmc_id: PMC ID
            format: Format to download ('xml' or 'pdf')
            
        Returns:
            True if successful, False otherwise
        """
        time.sleep(self.request_delay)
        
        # First get metadata
        metadata = self.get_article_metadata(pmc_id)
        if not metadata:
            return False
        
        # Save metadata
        metadata_file = self.output_dir / f"PMC{pmc_id}_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        # Download full text
        try:
            if format == "xml":
                handle = Entrez.efetch(
                    db="pmc",
                    id=pmc_id,
                    rettype="xml",
                    retmode="xml"
                )
                content = handle.read()
                handle.close()
                
                output_file = self.output_dir / f"PMC{pmc_id}.xml"
                if isinstance(content, bytes):
                    with open(output_file, 'wb') as f:
                        f.write(content)
                else:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                        
            elif format == "pdf":
                # Try to download PDF from PMC
                # Ensure we have the numeric ID without PMC prefix
                pmc_id_clean = pmc_id.replace("PMC", "")
                pdf_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmc_id_clean}/pdf/"
                response = requests.get(pdf_url, timeout=30)
                
                if response.status_code == 200 and response.headers.get('content-type') == 'application/pdf':
                    output_file = self.output_dir / f"PMC{pmc_id}.pdf"
                    with open(output_file, 'wb') as f:
                        f.write(response.content)
                else:
                    print(f"PDF not available for PMC{pmc_id}, saved XML instead")
                    return self.download_paper(pmc_id, format="xml")
            
            return True
            
        except Exception as e:
            print(f"Error downloading PMC{pmc_id}: {e}")
            return False
    
    def download_papers(self, query: str, max_results: int = 100, format: str = "xml"):
        """
        Search and download multiple papers.
        
        Args:
            query: Search query
            max_results: Maximum number of papers to download
            format: Format to download ('xml' or 'pdf')
        """
        pmc_ids = self.search_pmc(query, max_results)
        
        if not pmc_ids:
            print("No papers found")
            return
        
        print(f"\nDownloading {len(pmc_ids)} papers...")
        
        success_count = 0
        for pmc_id in tqdm(pmc_ids, desc="Downloading papers"):
            if self.download_paper(pmc_id, format):
                success_count += 1
        
        print(f"\nSuccessfully downloaded {success_count}/{len(pmc_ids)} papers")
        print(f"Papers saved to: {self.output_dir.absolute()}")
        
        # Create a summary file
        summary = {
            "query": query,
            "total_found": len(pmc_ids),
            "successfully_downloaded": success_count,
            "format": format,
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "license_info": "All papers are from PMC Open Access subset and include license information in metadata files"
        }
        
        summary_file = self.output_dir / "download_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\nSummary saved to: {summary_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Download papers from PubMed Central Open Access Subset",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download neurology papers
  python download_pmc_papers.py --email user@example.com --query "neurology OR neurological"
  
  # Download with API key for higher rate limits
  python download_pmc_papers.py --email user@example.com --api-key YOUR_KEY --query "neurology"
  
  # Download specific disease papers
  python download_pmc_papers.py --email user@example.com --query "alzheimer OR parkinson"
        """
    )
    
    parser.add_argument(
        "--email",
        required=True,
        help="Your email address (required by NCBI)"
    )
    
    parser.add_argument(
        "--api-key",
        help="NCBI API key for higher rate limits (optional)"
    )
    
    parser.add_argument(
        "--query",
        default="neurology OR neurological OR neuroscience",
        help="Search query for papers (default: neurology-related)"
    )
    
    parser.add_argument(
        "--max-results",
        type=int,
        default=100,
        help="Maximum number of papers to download (default: 100)"
    )
    
    parser.add_argument(
        "--format",
        choices=["xml", "pdf"],
        default="xml",
        help="Download format (default: xml)"
    )
    
    parser.add_argument(
        "--output-dir",
        default="data/pmc_papers",
        help="Output directory for downloaded papers (default: data/pmc_papers)"
    )
    
    args = parser.parse_args()
    
    # Create downloader
    downloader = PMCDownloader(
        email=args.email,
        api_key=args.api_key,
        output_dir=args.output_dir
    )
    
    # Download papers
    downloader.download_papers(
        query=args.query,
        max_results=args.max_results,
        format=args.format
    )


if __name__ == "__main__":
    main()
