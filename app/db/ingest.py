from app.core.github import GitHubClient
from app.ml.clean import clean_issue
from app.db.vector import add_issue
from app.config import SOURCE_REPO
import json
import os

def main():

    github = GitHubClient()
    issues = github.fetch_issues(SOURCE_REPO)
    
    raw_issues = []

    for issue in issues:
        cleaned = clean_issue(issue)
        add_issue(
            cleaned["id"],
            cleaned["text"],
            cleaned["embedding"],
            {
                "state": cleaned["state"],
                "url": cleaned["url"]
            }
        )
        raw_issues.append({
            "id": issue['id'],
            "title": issue['title'],
            "body": issue['body'],
            "state": issue['state'],
            "url": issue['url']
        })

    os.makedirs("data", exist_ok=True)

    with open("data/issues.json", "w", encoding="utf-8") as f:
        json.dump(raw_issues, f, indent=4, ensure_ascii=False)
    print(f"Stored {len(issues)} issues")


if __name__ == "__main__":
    main()