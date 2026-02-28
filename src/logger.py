from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


class Logger:
    def __init__(self, log_file: str):
        self.log_file = Path(log_file)
        self.entries: List[Dict[str, Any]] = []

    def add_entry(self, data: Dict[str, Any]):
        self.entries.append(data)

    def save(self):
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write("# Screenshot Gallery - Extracted Links & Info\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Images: {len(self.entries)}\n\n")
            f.write("---\n\n")
            
            for i, entry in enumerate(self.entries, 1):
                f.write(f"## {i}. {entry.get('filename', 'Unknown')}\n")
                f.write(f"**Category**: {entry.get('category', 'N/A')}\n")
                
                if entry.get("account_name"):
                    f.write(f"**Account**: @{entry['account_name']}\n")
                
                f.write(f"**Purpose**: {entry.get('purpose', 'N/A')}\n")
                f.write(f"**Summary**: {entry.get('content_summary', 'N/A')}\n\n")
                
                if entry.get("potential_use"):
                    f.write(f"**Potential Use**: {entry['potential_use']}\n\n")
                
                if entry.get("mentioned_items"):
                    items = entry["mentioned_items"]
                    if isinstance(items, list):
                        items = ", ".join(items)
                    f.write(f"**Mentioned Items**: {items}\n\n")
                
                links = entry.get("links", [])
                if links:
                    f.write("**Links**:\n")
                    for link in links:
                        f.write(f"  - {link}\n")
                    f.write("\n")
                
                if entry.get("tags"):
                    f.write(f"**Tags**: {entry['tags']}\n")
                
                f.write("\n---\n\n")

    def save_category_files(self, output_dir: Path, categories: List[str]):
        for category in categories:
            category_entries = [e for e in self.entries if e.get("category") == category]
            
            if not category_entries:
                continue
            
            category_file = output_dir / f"{category}.md"
            
            with open(category_file, "w", encoding="utf-8") as f:
                f.write(f"# {category.capitalize()}\n\n")
                f.write(f"Total: {len(category_entries)} images\n\n")
                f.write("---\n\n")
                
                for i, entry in enumerate(category_entries, 1):
                    f.write(f"## {i}. {entry.get('filename', 'Unknown')}\n")
                    
                    if entry.get("account_name"):
                        f.write(f"**Account**: @{entry['account_name']}\n")
                    
                    f.write(f"**Purpose**: {entry.get('purpose', 'N/A')}\n")
                    f.write(f"**Summary**: {entry.get('content_summary', 'N/A')}\n\n")
                    
                    links = entry.get("links", [])
                    if links:
                        f.write("**Links**:\n")
                        for link in links:
                            f.write(f"  - {link}\n")
                        f.write("\n")
                    
                    f.write("---\n\n")

    def get_summary(self) -> Dict[str, int]:
        summary = {}
        for entry in self.entries:
            category = entry.get("category", "misc")
            summary[category] = summary.get(category, 0) + 1
        return summary
