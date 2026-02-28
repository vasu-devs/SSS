import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForVision2Seq
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class VisionModel:
    def __init__(self, model_name: str, device: str = "cuda", max_tokens: int = 512, temperature: float = 0.1):
        self.model_name = model_name
        self.device = device
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.processor = None
        self.model = None
        self._load_model()

    def _load_model(self):
        logger.info(f"Loading vision model: {self.model_name}")
        
        self.processor = AutoProcessor.from_pretrained(
            self.model_name,
            trust_remote_code=True
        )
        
        self.model = AutoModelForVision2Seq.from_pretrained(
            self.model_name,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            trust_remote_code=True
        )
        
        self.model.eval()
        logger.info("Vision model loaded successfully")

    def process_image(self, image_path: str) -> Dict[str, Any]:
        image = Image.open(image_path).convert("RGB")
        
        prompt = """You are an expert at analyzing screenshots. Analyze this image and extract structured information.

For each screenshot, provide the following:
1. account_name: The username/handle if visible (just the name without @). If not visible, say "None"
2. content_summary: What the image/post is about in 2-3 clear sentences
3. purpose: Why this content exists (educational, promotional, entertainment, informational, etc.)
4. potential_use: What the viewer might want to save this for (learning, reference, entertainment, etc.)
5. mentioned_items: Any specific names, tools, frameworks, anime titles, websites, technologies mentioned
6. links: Any URLs visible in the image (complete URLs)
7. suggested_category: Which folder this should go in (anime, tech, hiring, finance, learning, health, news, memes, misc)

Format your response exactly like this:
---
account_name: [name or None]
content_summary: [2-3 sentences]
purpose: [what it is for]
potential_use: [why someone would save this]
mentioned_items: [list of items, comma separated]
links: [list of URLs, comma separated]
suggested_category: [one word from the list above]
---"""

        conversation = [
            {
                "role": "user",
                "content": [
                    {"type": "image"},
                    {"type": "text", "text": prompt}
                ]
            }
        ]
        
        text = self.processor.apply_chat_template(
            conversation, 
            tokenize=False, 
            add_generation_prompt=True
        )
        
        inputs = self.processor(
            text=[text],
            images=[image],
            return_tensors="pt",
            padding=True
        )
        
        inputs = {k: v.to(self.device) if isinstance(v, torch.Tensor) else v 
                  for k, v in inputs.items()}
        
        with torch.no_grad():
            output_ids = self.model.generate(
                **inputs,
                max_new_tokens=self.max_tokens,
                temperature=self.temperature,
                do_sample=self.temperature > 0
            )
        
        input_ids_len = inputs["input_ids"].shape[1]
        generated_ids = output_ids[0][input_ids_len:]
        
        output_text = self.processor.decode(
            generated_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True
        )
        
        return self._parse_response(output_text)

    def _parse_response(self, response: str) -> Dict[str, Any]:
        result = {
            "account_name": None,
            "content_summary": "",
            "purpose": "",
            "potential_use": "",
            "mentioned_items": [],
            "links": [],
            "suggested_category": "misc"
        }
        
        current_key = None
        current_value = []
        
        lines = response.split("\n")
        for line in lines:
            line = line.strip()
            if not line or line.startswith("---"):
                continue
            
            if ": " in line:
                if current_key:
                    result[current_key] = " ".join(current_value).strip()
                key_part, value_part = line.split(": ", 1)
                current_key = key_part.strip().lower().replace("-", "_")
                current_value = [value_part]
            elif current_key:
                current_value.append(line)
        
        if current_key:
            result[current_key] = " ".join(current_value).strip()
        
        if result["mentioned_items"]:
            items = result["mentioned_items"]
            if isinstance(items, str):
                result["mentioned_items"] = [i.strip() for i in items.split(",") if i.strip()]
        
        if result["links"]:
            links = result["links"]
            if isinstance(links, str):
                result["links"] = [l.strip() for l in links.split(",") if l.strip()]
        
        return result

    def clear_cache(self):
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    def unload(self):
        del self.model
        del self.processor
        self.clear_cache()
        logger.info("Vision model unloaded")
