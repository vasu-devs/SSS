import re
from typing import List, Dict, Any


class LinkExtractor:
    def __init__(self):
        self.url_pattern = re.compile(
            r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s]*',
            re.IGNORECASE
        )
        
        self.platform_patterns = {
            "linkedin": re.compile(r'linkedin\.com/(?:in|jobs|company|pulse)', re.IGNORECASE),
            "github": re.compile(r'github\.com/', re.IGNORECASE),
            "youtube": re.compile(r'(?:youtube\.com|youtu\.be)', re.IGNORECASE),
            "twitter": re.compile(r'(?:twitter\.com|x\.com)', re.IGNORECASE),
            "instagram": re.compile(r'instagram\.com/', re.IGNORECASE),
            "reddit": re.compile(r'reddit\.com/', re.IGNORECASE),
            "stackoverflow": re.compile(r'stackoverflow\.com/', re.IGNORECASE),
            "medium": re.compile(r'medium\.com/', re.IGNORECASE),
            "devto": re.compile(r'dev\.to/', re.IGNORECASE),
            "hackerrank": re.compile(r'hackerrank\.com/', re.IGNORECASE),
            "leetcode": re.compile(r'leetcode\.com/', re.IGNORECASE),
            "coursera": re.compile(r'coursera\.org/', re.IGNORECASE),
            "udemy": re.compile(r'udemy\.com/', re.IGNORECASE),
            "buymeacoffee": re.compile(r'buymeacoffee\.com', re.IGNORECASE),
        }

    def extract_links(self, text: str) -> List[str]:
        if not text:
            return []
        
        urls = self.url_pattern.findall(text)
        
        unique_urls = []
        seen = set()
        for url in urls:
            clean_url = url.rstrip('.,;:!?)]}')
            if clean_url not in seen:
                seen.add(clean_url)
                unique_urls.append(clean_url)
        
        return unique_urls

    def extract_from_vision_result(self, vision_result: Dict[str, Any]) -> List[str]:
        links = vision_result.get("links", [])
        
        if isinstance(links, str):
            extracted = self.extract_links(links)
        elif isinstance(links, list):
            extracted = []
            for link in links:
                if isinstance(link, str):
                    extracted.extend(self.extract_links(link))
        else:
            extracted = []
        
        content = vision_result.get("content_summary", "")
        mentioned = vision_result.get("mentioned_items", [])
        if isinstance(mentioned, list):
            content += " " + " ".join([str(m) for m in mentioned])
        else:
            content += " " + str(mentioned)
        
        extracted.extend(self.extract_links(content))
        
        return list(set(extracted))

    def categorize_links(self, links: List[str]) -> Dict[str, List[str]]:
        categorized = {
            "linkedin": [],
            "github": [],
            "youtube": [],
            "twitter": [],
            "instagram": [],
            "reddit": [],
            "stackoverflow": [],
            "medium": [],
            "devto": [],
            "hackerrank": [],
            "leetcode": [],
            "coursera": [],
            "udemy": [],
            "other": []
        }
        
        for link in links:
            categorized_link = False
            for platform, pattern in self.platform_patterns.items():
                if pattern.search(link):
                    categorized[platform].append(link)
                    categorized_link = True
                    break
            
            if not categorized_link:
                categorized["other"].append(link)
        
        return categorized

    def format_links_for_log(self, links: List[str]) -> str:
        if not links:
            return "None"
        
        categorized = self.categorize_links(links)
        
        lines = []
        for platform, urls in categorized.items():
            if urls:
                for url in urls:
                    lines.append(f"  - {url}")
        
        return "\n".join(lines) if lines else "None"
