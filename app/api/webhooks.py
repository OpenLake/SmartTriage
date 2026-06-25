from fastapi import APIRouter, Request

from app.ml.duplicate import detect_duplicate
from app.core.github import GitHubClient

router = APIRouter()

github = GitHubClient()

@router.post("/webhook")
async def github_webhook(request: Request):

    event = request.headers.get("X-GitHub-Event")

    print(f"GitHub Event: {event}")

    try:
        payload = await request.json()
    except Exception:
        payload = {}

    if event == "issues":

        action = payload.get("action")

        if action == "opened":
            issue_text = (
                payload["issue"]["title"]
                + "\n"
                + (payload["issue"]["body"] or "")
            )

            result = detect_duplicate(issue_text)
            print("Duplicate result:", result)

            if result and result["duplicate"]:
                github.comment_issue(
                    payload["issue"]["number"],

                    f"""
Possible duplicate issue detected.

Similar issue:
{result['issue']['url']}

Similarity:
{result['similarity']:.2f}
"""
                )

    return {"ok": True}