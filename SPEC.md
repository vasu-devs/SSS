# SSS - Screenshot Sorting System

## Project Overview

**Purpose**: Automatically sort screenshots into categorized folders based on visual content using local vision AI, with smart text extraction and link logging.

**Hardware**: RTX 4060 (8GB VRAM), 24GB RAM, Intel i7-13650HX

---

## Categories

| Category | Keywords/Indicators |
|----------|---------------------|
| anime | anime, manga, naruto, one piece, aot, jjk, tokyo revengers, attack on titan, bluelock, demon slayer, crunchyroll, myanimelist, episode, chapter, seasonal anime |
| tech | programming, coding, github, stackoverflow, dev, terminal, vscode, rust, python, javascript, react, vue, angular, node, docker, kubernetes, aws, gcp, azure, linux, open source, library, framework, api, documentation |
| hiring | job, hiring, careers, linkedin, apply, salary, offer, interview, resume, cv, software engineer, developer, remote, placement, fresher, experience, leetcode, hackerrank, interview preparation |
| finance | stock, investment, trading, crypto, bitcoin, ethereum, nifty, sensex, forex, mutual fund, sip, profit, loss, dividend, portfolio, market analysis, tradingview |
| learning | course, tutorial, udemy, coursera, edx, youtube, learn, study, beginner, advanced, guide, documentation, roadmap, bootcamp, certification |
| health | fitness, workout, gym, exercise, diet, nutrition, health, yoga, running, muscle, weight loss, protein, calories |
| news | news, article, headline, breaking, update, report, bbc, cnn, times of india, republic |
| memes | meme, funny, comedy, reel, viral, trending |
| misc | anything that doesn't fit above |

---

## Processing Pipeline

### Stage 1: Image Loading
- Load image, validate format (jpg, png, webp, heic)
- Convert to RGB
- Resize if > 2048px (preserve aspect ratio)

### Stage 2: Vision Model (Qwen2-VL-2B)
- **Prompt**: Extract structured information from the screenshot
- **Output fields**:
  - `account_name`: Username/handle if visible (without @)
  - `content_summary`: What the image/post is about (2-3 sentences)
  - `purpose`: Why this content exists (informational, promotional, entertainment)
  - `potential_use`: What user might want to save this for
  - `mentioned_items`: Any specific names, tools, frameworks, anime titles, etc.
  - `links`: All URLs found in image

### Stage 3: Text Cleaning
- Remove hashtags entirely (#word)
- Remove @mentions (keep username only, no @)
- Remove emojis
- Remove repeated characters (e.g., "happyyy" → "happy")
- Remove excessive whitespace
- Keep meaningful punctuation

### Stage 4: Classification
- Use LLM classification (already in vision prompt)
- Fallback: keyword matching if model uncertain
- Confidence threshold: 0.7

### Stage 5: Link Extraction
- Regex patterns for common platforms:
  - LinkedIn: linkedin.com/in/, linkedin.com/jobs/
  - GitHub: github.com/
  - YouTube: youtube.com/, youtu.be/
  - Twitter/X: x.com/, twitter.com/
  - Instagram: instagram.com/
  - Reddit: reddit.com/
  - General URLs: http(s)://...

### Stage 6: File Organization
- Move to `output/{category}/{original_filename}`
- If category = misc, put in `output/misc/`
- Handle duplicates: append timestamp

### Stage 7: Logging
- **links.md**: Master index with all extracted info
- **{category}.md**: Separate file per category (optional)

---

## Output Format

### links.md
```markdown
# Screenshot Gallery - Extracted Links & Info

Generated: 2026-02-28 10:30:00
Total Images: 25

---

## 1. screenshot_001.jpg
**Category**: tech
**Account**: @javascriptmastery
**Purpose**: Educational content about new React 19 features
**Summary**: Tutorial explaining React 19's new hooks and server components
**Links**: 
  - https://react.dev
  - https://github.com/reactjs/react
**Tags**: #react #javascript #webdev

---

## 2. screenshot_002.jpg
**Category**: anime
**Account**: @animehype
**Purpose**: Entertainment - weekly anime recommendations
**Summary**: Top 5 anime to watch this winter season
**Links**:
  - https://myanimelist.net
**Tags**: #anime #winter2026

---
```

---

## Memory Management

- Load model once at startup
- Process 1 image at a time (no batching)
- Clear GPU cache after every 5 images: `torch.cuda.empty_cache()`
- Use CPU fallback for text processing if needed

---

## Configuration (config.yaml)

```yaml
paths:
  input: "./screenshots"
  output: "./output"
  log: "./links.md"

model:
  name: "Qwen/Qwen2-VL-2B-Instruct"
  device: "cuda"
  max_tokens: 512
  temperature: 0.1

processing:
  image_size: 1024
  batch_size: 1
  clear_cache_every: 5

categories:
  - anime
  - tech
  - hiring
  - finance
  - learning
  - health
  - news
  - memes
  - misc
```

---

## Commands

```bash
python main.py                  # Run on default folders
python main.py --input ./my_pics    # Custom input folder
python main.py --help           # Show all options
```

---

## File Structure

```
SSS/
├── SPEC.md
├── config.yaml
├── requirements.txt
├── main.py
├── src/
│   ├── __init__.py
│   ├── vision_model.py
│   ├── text_cleaner.py
│   ├── classifier.py
│   ├── link_extractor.py
│   ├── file_manager.py
│   └── logger.py
├── screenshots/           # Put screenshots here
└── output/               # Sorted output here
```
