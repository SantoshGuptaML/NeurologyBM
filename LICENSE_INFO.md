# Licensing Information for Training Data

## Overview

This document provides detailed information about the licensing of data downloaded using the NeurologyBM toolkit. This information is crucial for understanding what you can and cannot do with the downloaded papers and abstracts, particularly for training machine learning models.

## PubMed Abstracts - PUBLIC DOMAIN ✅

### Summary
**PubMed abstracts have NO copyright restrictions and can be used for ANY purpose.**

### Details
- **License**: Public Domain
- **Copyright Status**: Not copyrighted
- **Commercial Use**: ✅ Allowed
- **Non-Commercial Use**: ✅ Allowed
- **Training ML Models**: ✅ Allowed (both commercial and non-commercial)
- **Attribution Required**: No (but recommended for academic integrity)
- **Redistribution**: ✅ Allowed

### Official Policy
According to NCBI:
> "PubMed Central (PMC) is a free archive of biomedical and life sciences journal literature at the U.S. National Institutes of Health's National Library of Medicine. In keeping with NLM's policy on copyright, PMC provides access to the abstracts of articles in the public domain."

Reference: https://www.ncbi.nlm.nih.gov/home/about/policies/

### What You CAN Do
✅ Use abstracts to train commercial AI models  
✅ Use abstracts to train non-commercial AI models  
✅ Include abstracts in datasets  
✅ Modify or transform the abstracts  
✅ Redistribute abstracts freely  
✅ Use for research without attribution  

### What You SHOULD Do (Best Practices)
- Cite the original papers in academic publications
- Acknowledge PubMed/NCBI as the source
- Follow NCBI's API usage guidelines (rate limiting)

## PMC Open Access Papers - VARIOUS LICENSES

### Summary
**PMC Open Access papers have individual licenses, mostly Creative Commons.**

### Details
- **License**: Varies by paper (included in metadata)
- **Common Licenses**: CC-BY, CC-BY-NC, CC-BY-NC-ND
- **Commercial Use**: Depends on license
- **Non-Commercial Use**: ✅ Generally allowed
- **Training ML Models**: Depends on license
- **Attribution Required**: Usually yes
- **Redistribution**: Depends on license

### License Types

#### Creative Commons BY (CC-BY) ✅✅✅
**Most Permissive - RECOMMENDED**
- ✅ Commercial use allowed
- ✅ Non-commercial use allowed
- ✅ Training ML models (commercial)
- ✅ Training ML models (non-commercial)
- ✅ Modification allowed
- ✅ Redistribution allowed
- ⚠️ Attribution required

#### Creative Commons BY-NC (CC-BY-NC) ✅
**Non-Commercial Only**
- ❌ Commercial use NOT allowed
- ✅ Non-commercial use allowed
- ❌ Training commercial ML models NOT allowed
- ✅ Training non-commercial ML models allowed
- ✅ Modification allowed
- ✅ Redistribution allowed (non-commercial)
- ⚠️ Attribution required

#### Creative Commons BY-NC-ND (CC-BY-NC-ND)
**Most Restrictive**
- ❌ Commercial use NOT allowed
- ✅ Non-commercial use allowed
- ❌ Training commercial ML models NOT allowed
- ⚠️ Training non-commercial ML models (check interpretation)
- ❌ Modification NOT allowed
- ✅ Redistribution allowed (unmodified, non-commercial)
- ⚠️ Attribution required

#### Public Domain / CC0 ✅✅✅
**Fully Permissive**
- ✅ All uses allowed
- Same as PubMed abstracts

### How to Check Paper Licenses

Each downloaded PMC paper includes a metadata file (e.g., `PMC12345_metadata.json`) that contains:
```json
{
  "pmc_id": "12345",
  "license": "CC-BY",
  "license_url": "https://creativecommons.org/licenses/by/4.0/",
  ...
}
```

Always check the metadata file before using papers for training.

### What You CAN Do
✅ Use papers with CC-BY licenses for commercial training  
✅ Use papers with CC-BY-NC licenses for non-commercial training  
✅ Use all Open Access papers for research  
✅ Cite papers appropriately  

### What You CANNOT Do
❌ Use CC-BY-NC papers for commercial training  
❌ Ignore attribution requirements  
❌ Violate specific license terms  

## Recommendations for ML Training

### For Non-Commercial Research/Training ✅

**Use everything freely:**
1. All PubMed abstracts (public domain)
2. All PMC Open Access papers (all licenses allow non-commercial use)

**Best Practice:**
```python
# Filter for all papers
papers = download_all_pmc_papers()
abstracts = download_all_pubmed_abstracts()
train_model(papers + abstracts)  # ✅ Allowed
```

### For Commercial Training ⚠️

**Use selectively:**
1. All PubMed abstracts (public domain) ✅
2. Only PMC papers with permissive licenses (CC-BY, CC0) ✅
3. Exclude CC-BY-NC and CC-BY-NC-ND papers ❌

**Best Practice:**
```python
# Filter for commercial-friendly papers
papers = download_pmc_papers()
commercial_papers = [p for p in papers 
                     if p['license'] in ['CC-BY', 'CC0', 'Public Domain']]
abstracts = download_all_pubmed_abstracts()
train_model(commercial_papers + abstracts)  # ✅ Allowed
```

## Filtering Papers by License

You can filter downloaded papers programmatically:

```python
import json
from pathlib import Path

def filter_by_license(data_dir, allowed_licenses):
    """Filter papers by license type."""
    allowed_papers = []
    
    for metadata_file in Path(data_dir).glob("*_metadata.json"):
        with open(metadata_file) as f:
            metadata = json.load(f)
            
        if any(lic in metadata.get('license', '').upper() 
               for lic in allowed_licenses):
            allowed_papers.append(metadata)
    
    return allowed_papers

# For commercial use
commercial_papers = filter_by_license(
    'data/pmc_papers',
    ['CC-BY', 'CC0', 'PUBLIC DOMAIN']
)

# For non-commercial use (all papers)
noncommercial_papers = filter_by_license(
    'data/pmc_papers',
    ['CC-BY', 'CC-BY-NC', 'CC0', 'PUBLIC DOMAIN', 'CC-BY-NC-ND']
)
```

## Attribution Guidelines

### For Academic Publications
When using this data in research papers:
```
Data was obtained from PubMed (https://pubmed.ncbi.nlm.nih.gov/) 
and PubMed Central Open Access Subset (https://www.ncbi.nlm.nih.gov/pmc/).
```

### For Datasets
When creating datasets:
```
This dataset includes abstracts from PubMed (public domain) and 
full-text articles from PMC Open Access Subset under various 
Creative Commons licenses. See LICENSE_INFO.md for details.
```

### For ML Model Documentation
When documenting training data:
```
Training data: X,XXX PubMed abstracts (public domain) and Y,YYY 
PMC Open Access articles (CC-BY and CC-BY-NC licenses). 
Licensed for non-commercial use.
```

## NCBI Usage Policy Compliance

This toolkit respects NCBI's usage guidelines:
- ✅ Rate limiting implemented (3 req/s or 10 req/s with API key)
- ✅ Email required for identification
- ✅ Proper use of E-utilities API
- ✅ No unauthorized bulk downloading

## Legal Disclaimer

This document provides guidance but is not legal advice. Users are responsible for:
- Verifying license compatibility with their use case
- Consulting with legal counsel for commercial applications
- Respecting all copyright and licensing terms
- Complying with institutional policies

## Questions?

For specific licensing questions:
- NCBI Policies: https://www.ncbi.nlm.nih.gov/home/about/policies/
- Creative Commons: https://creativecommons.org/licenses/
- PMC Copyright: https://www.ncbi.nlm.nih.gov/pmc/about/copyright/

## Summary Table

| Data Source | License | Commercial Training | Non-Commercial Training |
|-------------|---------|---------------------|------------------------|
| PubMed Abstracts | Public Domain | ✅ Yes | ✅ Yes |
| PMC Papers (CC-BY) | CC-BY | ✅ Yes | ✅ Yes |
| PMC Papers (CC-BY-NC) | CC-BY-NC | ❌ No | ✅ Yes |
| PMC Papers (CC0) | Public Domain | ✅ Yes | ✅ Yes |
| PMC Papers (CC-BY-NC-ND) | CC-BY-NC-ND | ❌ No | ⚠️ Check |

**Legend:**
- ✅ Yes - Clearly allowed
- ❌ No - Not allowed
- ⚠️ Check - Requires careful interpretation

---

Last Updated: 2024-12-24
