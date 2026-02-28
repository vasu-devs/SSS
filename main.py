import argparse
import os
import sys
import logging
from pathlib import Path
from typing import List
import yaml

from src.vision_model import VisionModel
from src.text_cleaner import TextCleaner
from src.classifier import Classifier
from src.link_extractor import LinkExtractor
from src.file_manager import FileManager
from src.logger import Logger

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.webp', '.heic', '.bmp', '.gif'}


def load_config(config_path: str = "config.yaml") -> dict:
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def get_image_files(input_dir: Path) -> List[Path]:
    images = []
    for ext in SUPPORTED_FORMATS:
        images.extend(input_dir.glob(f"*{ext}"))
        images.extend(input_dir.glob(f"*{ext.upper()}"))
    return sorted(images)


def process_image(
    image_path: Path,
    vision_model: VisionModel,
    cleaner: TextCleaner,
    classifier: Classifier,
    link_extractor: LinkExtractor,
    file_manager: FileManager,
    logger_obj: Logger,
    clear_cache_every: int,
    processed_count: int
) -> bool:
    try:
        logger.info(f"Processing: {image_path.name}")
        
        vision_result = vision_model.process_image(str(image_path))
        
        cleaned_result = cleaner.clean_dict(vision_result)
        
        links = link_extractor.extract_from_vision_result(cleaned_result)
        
        category = classifier.classify(cleaned_result, links)
        
        dest_path = file_manager.move_file(
            str(image_path),
            category,
            image_path.name
        )
        
        file_manager.save_extracted_text(
            image_path.name,
            cleaned_result,
            category
        )
        
        tags = []
        if cleaned_result.get("mentioned_items"):
            items = cleaned_result["mentioned_items"]
            if isinstance(items, list):
                tags.extend([f"#{item.replace(' ', '').lower()}" for item in items[:5]])
        
        log_entry = {
            "filename": image_path.name,
            "category": category,
            "account_name": cleaned_result.get("account_name"),
            "content_summary": cleaned_result.get("content_summary", ""),
            "purpose": cleaned_result.get("purpose", ""),
            "potential_use": cleaned_result.get("potential_use", ""),
            "mentioned_items": cleaned_result.get("mentioned_items", []),
            "links": links,
            "tags": ", ".join(tags) if tags else ""
        }
        logger_obj.add_entry(log_entry)
        
        logger.info(f"  → Categorized as: {category}")
        
        if (processed_count + 1) % clear_cache_every == 0:
            vision_model.clear_cache()
            logger.info("  → GPU cache cleared")
        
        return True
        
    except Exception as e:
        logger.error(f"Error processing {image_path.name}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Screenshot Sorting System")
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    parser.add_argument("--input", help="Input folder (overrides config)")
    parser.add_argument("--output", help="Output folder (overrides config)")
    args = parser.parse_args()
    
    config = load_config(args.config)
    
    input_dir = Path(args.input) if args.input else Path(config["paths"]["input"])
    output_dir = Path(args.output) if args.output else Path(config["paths"]["output"])
    log_file = config["paths"]["log"]
    
    if not input_dir.exists():
        logger.error(f"Input directory does not exist: {input_dir}")
        sys.exit(1)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info("Initializing components...")
    
    vision_model = VisionModel(
        model_name=config["model"]["name"],
        device=config["model"]["device"],
        max_tokens=config["model"]["max_tokens"],
        temperature=config["model"]["temperature"]
    )
    
    cleaner = TextCleaner()
    classifier = Classifier(config["categories"])
    link_extractor = LinkExtractor()
    file_manager = FileManager(str(output_dir), config["categories"])
    logger_obj = Logger(log_file)
    
    images = get_image_files(input_dir)
    
    if not images:
        logger.warning("No images found in input directory")
        return
    
    logger.info(f"Found {len(images)} images to process")
    
    processed_count = 0
    success_count = 0
    
    for image_path in images:
        if process_image(
            image_path,
            vision_model,
            cleaner,
            classifier,
            link_extractor,
            file_manager,
            logger_obj,
            config["processing"]["clear_cache_every"],
            processed_count
        ):
            success_count += 1
        processed_count += 1
    
    logger.info("Saving logs...")
    logger_obj.save()
    logger_obj.save_category_files(output_dir, config["categories"])
    
    logger.info(f"\n{'='*50}")
    logger.info(f"Processing complete!")
    logger.info(f"Total: {len(images)} | Success: {success_count} | Failed: {len(images) - success_count}")
    
    summary = logger_obj.get_summary()
    logger.info("\nSummary by category:")
    for category, count in sorted(summary.items(), key=lambda x: -x[1]):
        logger.info(f"  {category}: {count}")
    
    logger.info(f"\nOutput: {output_dir}")
    logger.info(f"Log: {log_file}")


if __name__ == "__main__":
    main()
