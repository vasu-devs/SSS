# SSS - Screenshot Sorting System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?style=flat&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/PyTorch-2.0+-red?style=flat&logo=pytorch" alt="PyTorch">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat" alt="License">
</p>

A local AI-powered screenshot organizer that automatically sorts screenshots into categorized folders using vision AI. Built with Qwen2-VL for high-accuracy image understanding.

## Features

- **Local Processing** - All processing happens on your machine using Qwen2-VL-2B (no cloud API calls)
- **Smart Classification** - Automatically categorizes screenshots into: anime, tech, hiring, finance, learning, health, news, memes
- **Link Extraction** - Extracts all URLs and links from screenshots
- **Text Cleaning** - Removes hashtags, emojis, and noise from extracted text
- **Detailed Logging** - Generates comprehensive markdown logs with all extracted information
- **GPU Optimized** - Designed for RTX 4060 (8GB VRAM) with memory management

## Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| GPU | 6GB VRAM | 8GB+ VRAM |
| RAM | 16GB | 24GB+ |
| Storage | 10GB free | 20GB+ |

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/vasu-devs/SSS.git
cd SSS
```

### 2. Install Python Dependencies

```bash
# Install pip if not available
sudo apt install python3-pip

# Install dependencies
pip install -r requirements.txt
```

### 3. First Run

The vision model (~4GB) will be downloaded automatically on first run.

## Usage

### Basic Usage

```bash
python main.py
```

### With Custom Input/Output Folders

```bash
python main.py --input /path/to/screenshots --output /path/to/output
```

### Configuration

Edit `config.yaml` to customize:

- Categories
- Model settings (temperature, max tokens)
- Input/output paths
- Processing options

## Project Structure

```
SSS/
├── main.py                 # Entry point
├── config.yaml             # Configuration file
├── requirements.txt        # Python dependencies
├── SPEC.md                 # Detailed specifications
├── src/
│   ├── vision_model.py     # Qwen2-VL wrapper
│   ├── text_cleaner.py     # Text cleaning utilities
│   ├── classifier.py       # Category classification
│   ├── link_extractor.py   # URL/link extraction
│   ├── file_manager.py     # File organization
│   └── logger.py           # Logging utilities
├── screenshots/            # Input screenshots (add yours here)
└── output/                # Sorted output
    ├── anime/
    ├── tech/
    ├── hiring/
    ├── finance/
    ├── learning/
    ├── health/
    ├── news/
    ├── memes/
    ├── misc/
    ├── extracted/          # Detailed text files per image
    └── links.md            # Master index with all links
```

## Output Format

### Sorted Folders

Screenshots are moved to `./output/{category}/` based on their content.

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
**Tags**: #react #javascript
```

### Extracted Text Files

Each screenshot also gets a detailed `.txt` file in `./output/extracted/` with full analysis.

## How It Works

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ Screenshot  │────▶│   Vision Model   │────▶│  Classification │
│   Input     │     │   (Qwen2-VL)     │     │    + Cleaning   │
└─────────────┘     └──────────────────┘     └────────┬────────┘
                                                      │
                       ┌──────────────────┐            │
                       │   Link Extract   │◀───────────┘
                       └────────┬─────────┘
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
     ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
     │ Sorted Files │  │ Extracted .txt│  │   links.md   │
     └──────────────┘  └──────────────┘  └──────────────┘
```

## Categories

| Category | Keywords |
|----------|----------|
| anime | Anime, manga, Crunchyroll, MyAnimeList, anime episodes |
| tech | Programming, GitHub, VSCode, React, Python, AWS, Docker |
| hiring | Jobs, LinkedIn, interviews, resume, careers |
| finance | Stocks, crypto, trading, investments |
| learning | Courses, tutorials, Udemy, Coursera |
| health | Fitness, workout, gym, diet |
| news | Breaking news, headlines |
| memes | Funny, comedy, viral |
| misc | Everything else |

## Memory Management

The system is optimized for GPUs with limited VRAM:

- Model loads once at startup
- Images process one at a time (no batching)
- GPU cache clears every 5 images
- Uses `bfloat16` for reduced memory footprint

## Troubleshooting

### Out of Memory

If you run out of VRAM, edit `config.yaml`:

```yaml
model:
  name: "Qwen/Qwen2-VL-2B-Instruct"  # Try 2B instead of 7B
```

### Slow Processing

Processing takes ~5-10 seconds per image on RTX 4060. This is expected for local inference.

### No Images Found

Make sure your screenshots are in the `./screenshots/` folder (or your custom input folder) and have supported extensions: `.jpg`, `.jpeg`, `.png`, `.webp`, `.heic`, `.bmp`, `.gif`

## Future Enhancements

- [ ] Mobile app (Flutter/React Native)
- [ ] Cloud deployment option
- [ ] Duplicate detection
- [ ] Manual reclassification
- [ ] Real-time folder watching

## License

MIT License - feel free to use and modify.

## Acknowledgments

- [Qwen2-VL](https://huggingface.co/Qwen/Qwen2-VL-2B-Instruct) - Vision language model
- [Transformers](https://github.com/huggingface/transformers) - Hugging Face Transformers library
