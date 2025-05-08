# Terapilot 🤖

Natural Language to Linux Command Translator powered by Cohere AI

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📦 Installation

### Prerequisites
- Python 3.6+
- Cohere API key ([Get one here](https://dashboard.cohere.com))

### Install via pip (Under Construction)
```bash
pip install terapilot
```

### Meanwhile
```bash
git clone https://github.com/Akhilesh2220/terapilot.git
```
```bash
cd terapilot
```
```bash
pip install -e .
```


 # 🚀 Usage

## Basic command translation
```bash
terapilot "list all files larger than 1GB"
```

## Configure API key
```bash
terapilot --config
```

## Remove saved key
```bash
terapilot --config-remove
```

# 🔧 Configuration
1. Get your Cohere API key
2. Run: terapilot --config
3. Paste your key when prompted (input will be hidden)

# 🌟 Features
1. Converts natural language to Linux commands
2. Interactive API key setup
3. Secure credential storage (~/.config/terapilot/config.env)
4. Supports all major shells (bash, zsh, fish)
5. Real-time API key validation

# 📬 Support
For bugs or feature requests:
Email: akhileshs222000@gmail.com