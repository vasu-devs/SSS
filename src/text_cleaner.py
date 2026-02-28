import re
from typing import List, Dict, Any


class TextCleaner:
    def __init__(self):
        self.hashtag_pattern = re.compile(r'#\w+')
        self.mention_pattern = re.compile(r'@\w+')
        self.emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+",
            flags=re.UNICODE
        )
        self.url_pattern = re.compile(r'https?://\S+|www\.\S+')
        self.whitespace_pattern = re.compile(r'\s+')

    def clean(self, text: str) -> str:
        if not text:
            return ""
        
        cleaned = text
        
        cleaned = self.emoji_pattern.sub('', cleaned)
        
        cleaned = self.hashtag_pattern.sub('', cleaned)
        
        cleaned = self.mention_pattern.sub(lambda m: m.group(0)[1:], cleaned)
        
        cleaned = self._remove_repeated_chars(cleaned)
        
        cleaned = self.whitespace_pattern.sub(' ', cleaned)
        
        cleaned = cleaned.strip()
        
        return cleaned

    def _remove_repeated_chars(self, text: str) -> str:
        return re.sub(r'(.)\1{2,}', r'\1\1', text)

    def clean_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        cleaned_data = data.copy()
        
        if cleaned_data.get("content_summary"):
            cleaned_data["content_summary"] = self.clean(cleaned_data["content_summary"])
        
        if cleaned_data.get("purpose"):
            cleaned_data["purpose"] = self.clean(cleaned_data["purpose"])
        
        if cleaned_data.get("potential_use"):
            cleaned_data["potential_use"] = self.clean(cleaned_data["potential_use"])
        
        if cleaned_data.get("mentioned_items"):
            items = cleaned_data["mentioned_items"]
            if isinstance(items, list):
                cleaned_data["mentioned_items"] = [self.clean(str(i)) for i in items]
            else:
                cleaned_data["mentioned_items"] = self.clean(str(items))
        
        return cleaned_data

    def extract_hashtags(self, text: str) -> List[str]:
        return self.hashtag_pattern.findall(text)

    def extract_mentions(self, text: str) -> List[str]:
        return self.mention_pattern.findall(text)
