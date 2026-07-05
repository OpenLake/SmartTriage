import hashlib
import hmac
import json

from app.config import WEBHOOK_SECRET

from fastapi import APIRouter, Request, HTTPException

from app.ml.duplicate import detect_duplicate
from app.core.github import GitHubClient



router = APIRouter()

github = GitHubClient()

@router.post("/webhook")
async def github_webhook(request: Request):

    raw_body = await request.body()

    signature = request.headers.get("X-Hub-Signature-256")

    if not signature:
        raise HTTPException(status_code=401, detail="Missing signature")

    if not WEBHOOK_SECRET:
        raise HTTPException(
            status_code=500,
            detail="Webhook secret is not configured",
        )

    expected_signature = (
        "sha256="
        + hmac.new(
            WEBHOOK_SECRET.encode(),
            raw_body,
            hashlib.sha256,
        ).hexdigest()
    )

    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Invalid JSON payload",
        )
    
    event = request.headers.get("X-GitHub-Event")

    print(f"GitHub Event: {event}")
    
    if event == "ping":
        return {"ok": True}
    
    if event == "issues":

        action = payload.get("action")

        if action == "opened":
            issue = payload.get("issue")
            if not issue:
                return {"ok": True}
            
            title = issue.get("title")
            if not title:
                return {"ok": True}

            body = issue.get("body") or ""
            issue_text = f"{title}\n{body}"

            result = detect_duplicate(issue_text)
            print("Duplicate result:", result)

            if result and result["duplicate"]:
                comment = f"""
                Possible duplicate issue detected.

                Similar issue:
                {result['issue']['url']}

                Similarity:
                {result['similarity']:.2f}
                """
                github.comment_issue(issue["number"], comment)

    return {"ok": True}