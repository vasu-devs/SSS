import os
import shutil
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


class FileManager:
    def __init__(self, output_dir: str, categories: List[str]):
        self.output_dir = Path(output_dir)
        self.categories = categories
        self._create_category_folders()

    def _create_category_folders(self):
        for category in self.categories:
            folder = self.output_dir / category
            folder.mkdir(parents=True, exist_ok=True)

    def move_file(self, source_path: str, category: str, filename: str) -> str:
        if category not in self.categories:
            category = "misc"
        
        dest_folder = self.output_dir / category
        dest_path = dest_folder / filename
        
        if dest_path.exists():
            name, ext = os.path.splitext(filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}{ext}"
            dest_path = dest_folder / filename
        
        shutil.copy2(source_path, dest_path)
        
        return str(dest_path)

    def save_extracted_text(self, filename: str, data: Dict[str, Any], category: str):
        extracted_dir = self.output_dir / "extracted"
        extracted_dir.mkdir(parents=True, exist_ok=True)
        
        name, _ = os.path.splitext(filename)
        text_file = extracted_dir / f"{name}.txt"
        
        with open(text_file, "w", encoding="utf-8") as f:
            f.write(f"File: {filename}\n")
            f.write(f"Category: {category}\n")
            f.write(f"{'='*50}\n\n")
            
            if data.get("account_name"):
                f.write(f"Account: @{data['account_name']}\n\n")
            
            f.write(f"Content Summary:\n{data.get('content_summary', 'N/A')}\n\n")
            f.write(f"Purpose: {data.get('purpose', 'N/A')}\n\n")
            f.write(f"Potential Use: {data.get('potential_use', 'N/A')}\n\n")
            
            if data.get("mentioned_items"):
                items = data["mentioned_items"]
                if isinstance(items, list):
                    items = ", ".join(items)
                f.write(f"Mentioned Items: {items}\n\n")
            
            if data.get("links"):
                f.write("Links:\n")
                for link in data["links"]:
                    f.write(f"  - {link}\n")

    def get_category_path(self, category: str) -> Path:
        if category not in self.categories:
            category = "misc"
        return self.output_dir / category

    def list_processed_files(self) -> List[str]:
        processed = []
        for category in self.categories:
            folder = self.output_dir / category
            if folder.exists():
                processed.extend([f.name for f in folder.glob("*") if f.is_file()])
        return processed
