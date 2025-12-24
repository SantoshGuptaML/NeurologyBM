#!/usr/bin/env python3
"""
PubMed Abstract Downloader for Neurology Research

This script downloads abstracts from PubMed. PubMed abstracts and their associated 
metadata are in the public domain and can be freely used for any purpose, including 
commercial and non-commercial applications like model training.

License Information:
- PubMed abstracts are in the public domain (no copyright restrictions)
- Can be freely used for research, training, and commercial purposes
- This script respects NCBI's usage guidelines and rate limits

Reference: https://www.ncbi.nlm.nih.gov/home/about/policies/

Usage:
    python download_pubmed_abstracts.py --query "neurology OR neurological" --max-results 1000

Author: NeurologyBM Project
"""

import argparse
import csv
import json
import os
import time
from pathlib import Path
from typing import List, Dict, Optional

try:
    from Bio import Entrez, Medline
    from tqdm import tqdm
except ImportError:
    print("Error: Required packages not installed.")
    print("Please install dependencies: pip install -r requirements.txt")
    exit(1)


class PubMedDownloader:
    """Downloads abstracts from PubMed."""
    
    def __init__(self, email: str, api_key: Optional[str] = None, output_dir: str = "data/pubmed_abstracts"):
        """
        Initialize the PubMed downloader.
        
        Args:
            email: Your email address (required by NCBI)
            api_key: Optional NCBI API key for higher rate limits
            output_dir: Directory to save downloaded abstracts
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
        
    def search_pubmed(self, query: str, max_results: int = 1000) -> List[str]:
        """
        Search PubMed for papers matching the query.
        
        Args:
            query: Search query (e.g., "neurology[MeSH] OR neurological disorders[MeSH]")
            max_results: Maximum number of results to return
            
        Returns:
            List of PubMed IDs (PMIDs)
        """
        print(f"Searching PubMed with query: {query}")
        
        try:
            handle = Entrez.esearch(
                db="pubmed",
                term=query,
                retmax=max_results,
                sort="relevance",
                usehistory="y"
            )
            record = Entrez.read(handle)
            handle.close()
            
            pmids = record.get("IdList", [])
            count = int(record.get("Count", 0))
            
            print(f"Found {count} total articles, retrieving up to {len(pmids)}")
            return pmids
            
        except Exception as e:
            print(f"Error searching PubMed: {e}")
            return []
    
    def fetch_abstracts_batch(self, pmids: List[str], batch_size: int = 200) -> List[Dict]:
        """
        Fetch abstracts in batches for efficiency.
        
        Args:
            pmids: List of PubMed IDs
            batch_size: Number of abstracts to fetch per request
            
        Returns:
            List of abstract records
        """
        all_records = []
        
        num_batches = (len(pmids) + batch_size - 1) // batch_size
        
        for i in tqdm(range(0, len(pmids), batch_size), total=num_batches, desc="Fetching batches"):
            batch = pmids[i:i + batch_size]
            time.sleep(self.request_delay)
            
            try:
                handle = Entrez.efetch(
                    db="pubmed",
                    id=batch,
                    rettype="medline",
                    retmode="text"
                )
                records = Medline.parse(handle)
                batch_records = list(records)
                handle.close()
                
                all_records.extend(batch_records)
                
            except Exception as e:
                print(f"Error fetching batch {i//batch_size + 1}: {e}")
                continue
        
        return all_records
    
    def process_abstract(self, record: Dict) -> Dict:
        """
        Process a Medline record into a structured format.
        
        Args:
            record: Medline record dictionary
            
        Returns:
            Processed abstract dictionary
        """
        processed = {
            "pmid": record.get("PMID", ""),
            "title": record.get("TI", ""),
            "abstract": record.get("AB", ""),
            "authors": record.get("AU", []),
            "journal": record.get("TA", ""),
            "publication_date": record.get("DP", ""),
            "doi": record.get("AID", [""])[0] if record.get("AID") else "",
            "mesh_terms": record.get("MH", []),
            "keywords": record.get("OT", []),
            "publication_types": record.get("PT", []),
            "language": record.get("LA", [""])[0] if record.get("LA") else "eng",
            "copyright": record.get("CI", ""),
            "license": "Public Domain - PubMed abstracts are not copyrighted"
        }
        
        return processed
    
    def save_abstracts(self, abstracts: List[Dict], formats: List[str] = ["json", "csv"]):
        """
        Save abstracts in multiple formats.
        
        Args:
            abstracts: List of processed abstract dictionaries
            formats: List of formats to save ('json', 'csv', 'txt')
        """
        if not abstracts:
            print("No abstracts to save")
            return
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        # Save as JSON
        if "json" in formats:
            json_file = self.output_dir / f"abstracts_{timestamp}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(abstracts, f, indent=2, ensure_ascii=False)
            print(f"Saved JSON to: {json_file}")
        
        # Save as CSV
        if "csv" in formats:
            csv_file = self.output_dir / f"abstracts_{timestamp}.csv"
            
            # Define CSV columns
            fieldnames = [
                "pmid", "title", "abstract", "authors", "journal", 
                "publication_date", "doi", "mesh_terms", "keywords"
            ]
            
            with open(csv_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for abstract in abstracts:
                    row = {
                        "pmid": abstract.get("pmid", ""),
                        "title": abstract.get("title", ""),
                        "abstract": abstract.get("abstract", ""),
                        "authors": "; ".join(abstract.get("authors", [])),
                        "journal": abstract.get("journal", ""),
                        "publication_date": abstract.get("publication_date", ""),
                        "doi": abstract.get("doi", ""),
                        "mesh_terms": "; ".join(abstract.get("mesh_terms", [])),
                        "keywords": "; ".join(abstract.get("keywords", []))
                    }
                    writer.writerow(row)
            
            print(f"Saved CSV to: {csv_file}")
        
        # Save as plain text (one abstract per file)
        if "txt" in formats:
            txt_dir = self.output_dir / f"txt_{timestamp}"
            txt_dir.mkdir(exist_ok=True)
            
            for abstract in abstracts:
                pmid = abstract.get("pmid", "unknown")
                txt_file = txt_dir / f"PMID_{pmid}.txt"
                
                with open(txt_file, 'w', encoding='utf-8') as f:
                    f.write(f"PMID: {abstract.get('pmid', '')}\n")
                    f.write(f"Title: {abstract.get('title', '')}\n")
                    f.write(f"Authors: {', '.join(abstract.get('authors', []))}\n")
                    f.write(f"Journal: {abstract.get('journal', '')}\n")
                    f.write(f"Date: {abstract.get('publication_date', '')}\n")
                    f.write(f"DOI: {abstract.get('doi', '')}\n\n")
                    f.write("Abstract:\n")
                    f.write(abstract.get('abstract', 'No abstract available') + "\n\n")
                    f.write("MeSH Terms:\n")
                    f.write(", ".join(abstract.get('mesh_terms', [])) + "\n\n")
                    f.write("License: Public Domain (PubMed abstracts are not copyrighted)\n")
            
            print(f"Saved {len(abstracts)} text files to: {txt_dir}")
    
    def download_abstracts(
        self, 
        query: str, 
        max_results: int = 1000,
        formats: List[str] = ["json", "csv"]
    ):
        """
        Search and download multiple abstracts.
        
        Args:
            query: Search query
            max_results: Maximum number of abstracts to download
            formats: List of output formats
        """
        # Search PubMed
        pmids = self.search_pubmed(query, max_results)
        
        if not pmids:
            print("No abstracts found")
            return
        
        print(f"\nDownloading {len(pmids)} abstracts...")
        
        # Fetch abstracts in batches
        records = self.fetch_abstracts_batch(pmids, batch_size=200)
        
        # Process abstracts
        abstracts = []
        for record in tqdm(records, desc="Processing abstracts"):
            processed = self.process_abstract(record)
            # Only include records with abstracts
            if processed.get("abstract"):
                abstracts.append(processed)
        
        print(f"\nSuccessfully processed {len(abstracts)} abstracts with text")
        
        # Save abstracts
        self.save_abstracts(abstracts, formats)
        
        # Create a summary file
        summary = {
            "query": query,
            "total_found": len(pmids),
            "with_abstracts": len(abstracts),
            "without_abstracts": len(records) - len(abstracts),
            "formats": formats,
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "license_info": "PubMed abstracts are in the public domain and can be freely used for any purpose, including non-commercial model training",
            "source": "PubMed (https://pubmed.ncbi.nlm.nih.gov/)",
            "usage_policy": "https://www.ncbi.nlm.nih.gov/home/about/policies/"
        }
        
        summary_file = self.output_dir / "download_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\nSummary saved to: {summary_file}")
        print(f"\nLicense: PubMed abstracts are in the PUBLIC DOMAIN")
        print("You can freely use them for training models for commercial or non-commercial purposes.")


def main():
    parser = argparse.ArgumentParser(
        description="Download abstracts from PubMed",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download neurology abstracts
  python download_pubmed_abstracts.py --email user@example.com --query "neurology OR neurological"
  
  # Download with API key for higher rate limits
  python download_pubmed_abstracts.py --email user@example.com --api-key YOUR_KEY --query "neurology"
  
  # Download specific disease abstracts
  python download_pubmed_abstracts.py --email user@example.com --query "alzheimer OR parkinson" --max-results 5000
  
  # Save in multiple formats
  python download_pubmed_abstracts.py --email user@example.com --query "neurology" --formats json csv txt
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
        default="neurology[MeSH] OR neurological diseases[MeSH]",
        help="Search query for abstracts (default: neurology-related)"
    )
    
    parser.add_argument(
        "--max-results",
        type=int,
        default=1000,
        help="Maximum number of abstracts to download (default: 1000)"
    )
    
    parser.add_argument(
        "--formats",
        nargs="+",
        choices=["json", "csv", "txt"],
        default=["json", "csv"],
        help="Output formats (default: json csv)"
    )
    
    parser.add_argument(
        "--output-dir",
        default="data/pubmed_abstracts",
        help="Output directory for downloaded abstracts (default: data/pubmed_abstracts)"
    )
    
    args = parser.parse_args()
    
    # Create downloader
    downloader = PubMedDownloader(
        email=args.email,
        api_key=args.api_key,
        output_dir=args.output_dir
    )
    
    # Download abstracts
    downloader.download_abstracts(
        query=args.query,
        max_results=args.max_results,
        formats=args.formats
    )


if __name__ == "__main__":
    main()
