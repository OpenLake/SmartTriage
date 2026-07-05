from dotenv import load_dotenv
import os

load_dotenv()

WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
TARGET_REPO = os.getenv("TARGET_REPO")
SOURCE_REPO = os.getenv("SOURCE_REPO")
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", 0.85))

required = {
    "GITHUB_WEBHOOK_SECRET": WEBHOOK_SECRET,
    "GITHUB_TOKEN": GITHUB_TOKEN,
    "TARGET_REPO": TARGET_REPO,
    "SOURCE_REPO": SOURCE_REPO,
}

missing = [key for key, value in required.items() if not value]

if missing:
    raise ValueError(
        f"Missing required environment variables: {', '.join(missing)}"
    )