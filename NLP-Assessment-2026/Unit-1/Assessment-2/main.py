"""
Course: DSA0311 - Natural Language Processing
Assessment: CO1 - Assessment Tool 1 (Application Based Questions)
Section 2: Regular Expressions – Product Search System
"""

import re
from typing import List, Dict, Any

class ProductSearchEngine:
    """
    E-Commerce Product Search System using Regular Expressions.
    Supports Exact, Prefix, Suffix, Partial Keyword, and Case-Insensitive Matching.
    """
    def __init__(self, catalog: List[str]):
        self.catalog = catalog

    def search_exact(self, query: str) -> List[str]:
        """Search products using an exact keyword match (case-insensitive)."""
        pattern = re.compile(rf"^\s*{re.escape(query.strip())}\s*$", re.IGNORECASE)
        return [p for p in self.catalog if pattern.search(p)]

    def search_prefix(self, prefix: str) -> List[str]:
        """Search products where any word starts with the prefix (case-insensitive)."""
        pattern = re.compile(rf"\b{re.escape(prefix.strip())}\w*", re.IGNORECASE)
        return [p for p in self.catalog if pattern.search(p)]

    def search_suffix(self, suffix: str) -> List[str]:
        """Search products where any word ends with the suffix (case-insensitive)."""
        pattern = re.compile(rf"\w*{re.escape(suffix.strip())}\b", re.IGNORECASE)
        return [p for p in self.catalog if pattern.search(p)]

    def search_partial(self, query: str) -> List[str]:
        """Search products containing the query substring anywhere (case-insensitive)."""
        pattern = re.compile(re.escape(query.strip()), re.IGNORECASE)
        return [p for p in self.catalog if pattern.search(p)]

    def execute_search_suite(self, test_queries: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Runs test queries and returns comprehensive matching report."""
        report = []
        for q in test_queries:
            mode = q["mode"]
            term = q["term"]
            if mode == "exact":
                matches = self.search_exact(term)
            elif mode == "prefix":
                matches = self.search_prefix(term)
            elif mode == "suffix":
                matches = self.search_suffix(term)
            elif mode == "partial":
                matches = self.search_partial(term)
            else:
                matches = []
            
            report.append({
                "mode": mode.capitalize(),
                "query": term,
                "count": len(matches),
                "matches": matches
            })
        return report

def run_experiment():
    catalog = [
        "Apple iPhone 15 Pro",
        "Samsung Galaxy S24 Ultra",
        "Apple MacBook Air M3",
        "Sony WH-1000XM5 Wireless Headphones",
        "Dell XPS 15 Laptop",
        "Logitech Wireless Mouse",
        "Apple iPad Pro",
        "Samsung 4K Smart TV",
        "Nike Air Max Shoes",
        "HP Spectre x360 Laptop",
        "Sony Bravia OLED TV",
        "Anker Wireless Charging Pad",
        "Razer Gaming Mouse Pad",
        "Laptop",
        "USB-C Fast Charging Cable"
    ]

    engine = ProductSearchEngine(catalog)

    test_suite = [
        {"mode": "exact", "term": "Laptop"},
        {"mode": "prefix", "term": "wire"},
        {"mode": "prefix", "term": "App"},
        {"mode": "suffix", "term": "Pro"},
        {"mode": "suffix", "term": "pad"},
        {"mode": "partial", "term": "Air"},
        {"mode": "partial", "term": "SAMSUNG"}
    ]

    results = engine.execute_search_suite(test_suite)

    print("=" * 80)
    print("            E-COMMERCE REGEX PRODUCT SEARCH SYSTEM RESULTS")
    print("=" * 80)
    print(f"Total Products in Catalog: {len(catalog)}")
    print("-" * 80)

    for idx, res in enumerate(results, 1):
        print(f"\nSearch #{idx} | Mode: {res['mode']:<8} | Query: '{res['query']}'")
        print(f"Total Matches Found: {res['count']}")
        if res['matches']:
            for m in res['matches']:
                print(f"   -> {m}")
        else:
            print("   -> [No matching products found]")

    print("\n" + "=" * 80)
    print("                        SEARCH SUMMARY REPORT")
    print("=" * 80)
    print(f"{'Search #':<10} | {'Mode':<10} | {'Query Term':<15} | {'Match Count':<12} | {'Match Status'}")
    print("-" * 80)
    for idx, res in enumerate(results, 1):
        status = "SUCCESS" if res['count'] > 0 else "ZERO RESULTS"
        print(f"Search {idx:<3} | {res['mode']:<10} | {res['query']:<15} | {res['count']:<12} | {status}")
    print("=" * 80)

if __name__ == "__main__":
    run_experiment()
