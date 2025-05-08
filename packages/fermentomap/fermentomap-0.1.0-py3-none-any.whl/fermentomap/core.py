
import json
from .parser import extract_proteins

def load_trait_db(path="fermentomap/traits_db.json"):
    with open(path) as f:
        return json.load(f)

def detect_traits(genome_proteins, trait_db):
    results = {}
    for trait, markers in trait_db.items():
        hits = [gene for gene in genome_proteins if any(m in gene.lower() for m in markers)]
        results[trait] = hits
    return results
