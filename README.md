# Internship Project - File Security and Gemini Help Bot

This project is a Python Tkinter desktop app for basic file security operations:
- File hash analysis (SHA-256)
- Simple malicious hash checking
- AES file encryption and decryption
- Gemini-powered help responses (optional)

## Project Files
- `gemini.py` - Main application script
- `hashes.txt` - Known malicious SHA-256 hashes (one hash per line)
- `.env.example` - Environment variable template
- `requirements.txt` - Python dependencies

## Prerequisites
- Python 3.9+
- A Gemini API key (optional, only needed for chatbot/help responses)

## Setup
1. Clone the repository.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set your Gemini API key in your environment:

```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your_api_key_here"
```

4. Add known malicious file hashes into `hashes.txt` (optional).

## Run

```bash
python gemini.py
```

## Notes
- If `GEMINI_API_KEY` is not set, the app still works for file checks/encryption/decryption, but Help Bot responses are disabled.
- Encryption creates a `.key` file next to the encrypted output.

## Disclaimer
This project is for educational/demo use. It is not a complete antivirus or enterprise-grade security product.
