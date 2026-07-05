from github import Github
from app.config import GITHUB_TOKEN
from app.config import TARGET_REPO

class GitHubClient:

    def __init__(self):
        self.client = Github(GITHUB_TOKEN)


    def get_repo(self, repo_name):
        return self.client.get_repo(repo_name)


    def fetch_issues(self, repo_name):
        repo = self.get_repo(repo_name)

        issues = []

        issue_iterator = repo.get_issues(state="all")

        for issue in issue_iterator:

            # skip pull requests
            if issue.pull_request:
                continue

            issues.append({
                "id": issue.id,
                "title": issue.title,
                "body": issue.body,
                "url": issue.html_url,
                "created_at": str(issue.created_at),
                "state": issue.state
            })

        return issues
    
    def comment_issue(self, issue_number, comment):
        repo = self.get_repo(TARGET_REPO)
        issue = repo.get_issue(number=issue_number)
        issue.create_comment(comment)