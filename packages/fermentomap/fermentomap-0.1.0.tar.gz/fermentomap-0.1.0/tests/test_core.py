
from fermentomap.core import load_trait_db, detect_traits
from fermentomap.parser import extract_proteins

def test_detect_traits():
    proteins = ["Lactate dehydrogenase", "Alcohol dehydrogenase", "Dextransucrase"]
    db = load_trait_db()
    results = detect_traits(proteins, db)
    assert "Lactate Production" in results and results["Lactate Production"]
    assert "Ethanol Production" in results and results["Ethanol Production"]
