# Gene Fetch
Gene Fetch enables high-throughput retreival of sequence data from NCBI databases based on taxonomy IDs (taxids) or taxonomic heirarchies. It can retrieve both protein and/or nucleotide sequences for various genes, including protein-coding genes (e.g., cox1, cytb, rbcl, matk) and rRNA genes (e.g., 16S, 18S).

## Installation:
Install from PyPI
```bash
pip install gene-fetch
```

## Post-installation testing:
- The Gene Fetch package includes some basic tests for each module, which can be run by: 
```bash
# Clone the repository
git clone https://github.com/bge-barcoding/gene_fetch.git
cd gene_fetch

# Install pytest
pip install pytest

# Run tests
pytest
```
* This will take a few minutes to run 65 tests, consisting of 8 test modules (tests/test_*.py). You will get 1 warning regarding API credentials as these are not provided in the basic tests.

## Usage:
```bash
python gene_fetch.py -g/--gene <gene_name> --type <sequence_type> -i/--in <samples.csv> -o/--out <output_directory> 
```
`--h/--help`: Show help and exit.

### Required arguments:
* `-g/--gene`: Name of gene to search for in NCBI GenBank database (e.g., cox1/16s/rbcl).
* `--type`: Sequence type to fetch; 'protein', 'nucleotide', or 'both' ('both' will initially search and fetch a protein sequence, and then fetches the corresponding nucleotide CDS for that protein sequence).
* `-i/--in`: Path to input CSV file containing sample IDs and TaxIDs (see [Input](#input) section below).
* `i2/--in2`: Path to alternative input CSV file containing sample IDs and taxonomic information for each sample (see [Input](#input) section below).
* `o/--out`: Path to output directory. The directory will be created if it does not exist.
* `e/--email` and `-k/--api-key`: Email address and associated API key for NCBI account. An NCBI account is required to run this tool (due to otherwise strict API limitations) - information on how to create an NCBI account and find your API key can be found [here](https://support.nlm.nih.gov/kbArticle/?pn=KA-05317).
### Optional arguments:
* `--protein-size`: Minimum protein sequence length filter. Applicable to mode 'batch' and 'single' search modes (default: 500).
* `--nucleotide-size`: Minimum nucleotide sequence length filter. Applicable to mode 'batch' and 'single' search modes (default: 1500).
* `s/--single`: Taxonomic ID for 'single' sequence search mode (`-i` and `-i2` are ignored when run with `-s` mode). 'single' mode will fetch all (or N if specifying `--max-sequences`) target gene or protein sequences on GenBank for a specific taxonomic ID.
* `--max-sequences`: Maximum number of sequences to fetch for a specific taxonomic ID (only applies when run in 'single' mode).
* `-b/--genbank`: Saves genbank (.gb) files for fetched nucleotide and/or protein sequences to `genbank/` (applies when run in 'batch' or 'single' mode).


## Input:
**Example 'samples.csv' input file (-i/--in)**
| ID | taxid |
| --- | --- |
| sample-1  | 177658 |
| sample-2 | 177627 |
| sample-3 | 3084599 |

**Example 'samples_taxonomy.csv' input file (-i2/--in2)**
| ID | phylum | class | order | family | genus | species |
| --- | --- | --- | --- | --- | --- | --- |
| sample-1  | Arthropoda | Insecta | Diptera | Acroceridae | Astomella | |
| sample-2 | Arthropoda | Insecta | Hemiptera | Cicadellidae | Psammotettix | Psammotettix sabulicola |
| sample-3 | Arthropoda | Insecta | Trichoptera | Limnephilidae | Dicosmoecus | Dicosmoecus palatus |
* Leave blank if taxonomic information not known/needed


** Authored by Dan Parsons and Ben Price @ NHMUK (2025). **
