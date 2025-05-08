
from Bio import SeqIO

def extract_proteins(genbank_file):
    proteins = []
    for record in SeqIO.parse(genbank_file, "genbank"):
        for feature in record.features:
            if feature.type == "CDS":
                product = feature.qualifiers.get("product", [""])[0]
                proteins.append(product)
    return proteins
