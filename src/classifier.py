from typing import Dict, List, Any


class Classifier:
    def __init__(self, categories: List[str]):
        self.categories = categories
        self.keyword_map = {
            "anime": [
                "anime", "manga", "naruto", "one piece", "attack on titan", "aot",
                "jjk", "jujutsu kaisen", "demon slayer", "tokyo revengers", "bluelock",
                "crunchyroll", "myanimelist", "animelist", "episode", "chapter",
                "seasonal anime", "anime recommendations", "anime episode", "otaku",
                "animestagram", "anime art", "anime edit", "gojo", "sukuna",
                "midoriya", "bakugo", "mha", "my hero academia", "berserk", "chainsaw man"
            ],
            "tech": [
                "programming", "coding", "github", "stackoverflow", "developer", "dev",
                "terminal", "vscode", "rust", "python", "javascript", "typescript",
                "react", "vue", "angular", "node", "nodejs", "docker", "kubernetes",
                "k8s", "aws", "gcp", "azure", "linux", "open source", "opensource",
                "library", "framework", "api", "rest api", "graphql", "database",
                "sql", "mongodb", "postgresql", "redis", "machine learning", "ml",
                "ai", "artificial intelligence", "deep learning", "neural network",
                "git", "cli", "command line", "server", "deployment", "ci/cd",
                "devops", "sre", "software engineering", "tech twitter", "tech reddit",
                "indie hacker", "startup", "SaaS", "web development", "app development",
                "mobile development", "flutter", "react native", "swift", "kotlin"
            ],
            "hiring": [
                "job", "jobs", "hiring", "career", "careers", "linkedin", "apply",
                "salary", "offer", "interview", "resume", "cv", "curriculum vitae",
                "software engineer", "developer job", "remote job", "work from home",
                "fresher", "placement", "recruitment", "recruiter", "hiring manager",
                "leetcode", "hackerrank", "interview preparation", "technical interview",
                "system design", "behavioral interview", "job offer", "package",
                "ctc", "notice period", "experience required", "job description"
            ],
            "finance": [
                "stock", "stocks", "investment", "investing", "trading", "crypto",
                "bitcoin", "btc", "ethereum", "eth", "nifty", "sensex", "forex",
                "mutual fund", "sip", "profit", "loss", "dividend", "portfolio",
                "market", "tradingview", "stock market", "share market", "nasdaq",
                "dow jones", "wall street", "bull market", "bear market", "ipo",
                "investment tips", "stock tips", "intraday", "swing trading"
            ],
            "learning": [
                "course", "courses", "tutorial", "tutorials", "udemy", "coursera",
                "edx", "youtube", "learn", "learning", "study", "beginner",
                "advanced", "guide", "documentation", "docs", "roadmap",
                "bootcamp", "certification", "certificate", "free course", "paid course",
                "online course", "mooc", "e-learning", "learn programming",
                "coding tutorial", "how to", "step by step", "crash course"
            ],
            "health": [
                "fitness", "workout", "gym", "exercise", "diet", "nutrition",
                "health", "yoga", "running", "muscle", "weight loss", "protein",
                "calories", "macros", "calisthenics", "strength training",
                "cardio", "hiit", "abs", "chest", "back", "legs", "biceps",
                "health tips", "fitness tips", "weight gain", "bodybuilding",
                "supplements", "whey protein", "creatine", "pre-workout"
            ],
            "news": [
                "news", "breaking", "headline", "report", "update", "bbc", "cnn",
                "times of india", "reuters", "ap", "news article", "journalism",
                "current affairs", "world news", "india news", "tech news",
                "sports news", "business news", "politics"
            ],
            "memes": [
                "meme", "memes", "funny", "comedy", "humor", "humour", "reel",
                "viral", "trending", "funny video", "meme account", "memes daily",
                "comedy gold", "lol", "lmao", "rofl", "funny tweets"
            ]
        }

    def classify(self, vision_result: Dict[str, Any], links: List[str]) -> str:
        suggested = vision_result.get("suggested_category", "").lower().strip()
        
        if suggested in self.categories:
            return suggested
        
        content = vision_result.get("content_summary", "")
        mentioned = vision_result.get("mentioned_items", [])
        
        if isinstance(mentioned, list):
            mentioned_text = " ".join([str(m) for m in mentioned])
        else:
            mentioned_text = str(mentioned)
        
        full_text = f"{content} {mentioned_text} {' '.join(links)}".lower()
        
        scores = {}
        for category, keywords in self.keyword_map.items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in full_text:
                    score += 1
            if score > 0:
                scores[category] = score
        
        if scores:
            best_category = max(scores.items(), key=lambda x: x[1])[0]
            if scores[best_category] >= 2:
                return best_category
        
        return "misc"

    def get_category_description(self, category: str) -> str:
        descriptions = {
            "anime": "Anime, manga, and related content",
            "tech": "Programming, technology, and development",
            "hiring": "Jobs, careers, and recruitment",
            "finance": "Stocks, investments, and trading",
            "learning": "Courses, tutorials, and educational content",
            "health": "Fitness, health, and nutrition",
            "news": "News articles and current affairs",
            "memes": "Memes and entertainment",
            "misc": "Miscellaneous content"
        }
        return descriptions.get(category, "Miscellaneous content")
