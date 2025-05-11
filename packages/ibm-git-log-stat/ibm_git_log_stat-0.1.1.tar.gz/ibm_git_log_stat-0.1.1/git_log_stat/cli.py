import argparse
import os
import subprocess

import requests


def parse_args():
    """
    Parses arguments
    --base-dir base directory where to search git repo
    --author email of the user for git log search
    --github-user username of author for PR search
    --start-date start date in YYYY-MM-DD format
    --end-date end date in YYYY-MM-DD format
    """
    parser = argparse.ArgumentParser(description="Track git commits and GitHub PRs for a given user and date range.")

    parser.add_argument(
        "--base-dir", default=os.getenv("BASE_DIR", os.path.expanduser("~/projects")),
        help="Base directory to search for git repositories"
    )
    parser.add_argument(
        "--author", default=os.getenv("AUTHOR", ""),
        help="Git commit author email (used in git log)"
    )
    parser.add_argument(
        "--github-user", default=os.getenv("GITHUB_USER", ""),
        help="GitHub username (used to filter PRs)"
    )
    parser.add_argument(
        "--start-date", default=os.getenv("START_DATE", "2025-04-01"),
        help="Start date (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--end-date", default=os.getenv("END_DATE", "2025-04-30"),
        help="End date (YYYY-MM-DD)"
    )

    return parser.parse_args()

def main():
    # Settings
    args = parse_args()
    BASE_DIR = os.path.expanduser(args.base_dir)
    AUTHOR = args.author
    GITHUB_USER = args.github_user
    SINCE = args.start_date
    UNTIL = args.end_date
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
    HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

    # GitHub API base
    GITHUB_API = "https://api.github.ibm.com"


    def get_github_repo_url():
        """Extract GitHub org/repo name from git config"""
        try:
            remotes = subprocess.check_output(["git", "remote", "-v"]).decode()
            for line in remotes.splitlines():
                if "github.ibm.com" in line:
                    url = line.split()[1]
                    url = url.replace("git@github.ibm.com:", "").replace("https://github.ibm.com/", "").replace(".git", "")
                    return url.strip()
        except:
            return None


    def get_pull_requests(repo_full_name, author):
        """Fetch PRs by user for a given repo"""
        prs = []
        url = f"{GITHUB_API}/repos/{repo_full_name}/pulls?state=all&per_page=100"
        while url:
            res = requests.get(url, headers=HEADERS)
            if res.status_code != 200:
                return []
            for pr in res.json():
                created_at = pr["created_at"][:10]
                # print(pr["user"]["login"])
                if SINCE <= created_at <= UNTIL and str(pr["user"]["login"]).lower() == str(GITHUB_USER).lower():
                    prs.append(f"[#{pr['number']}] {pr['title']} ({created_at})")
            # Pagination
            url = res.links.get('next', {}).get('url')
        return prs


    # Format for display
    print(f"\n🔍 Git commits by {AUTHOR} from {SINCE} to {UNTIL}\n")

    try:
        # Check if base directory given in arg exists
        if not os.path.isdir(BASE_DIR):
            raise ValueError(f"Invalid base directory: {BASE_DIR}")

        # Walk through all subfolders and check for git repos
        for root, dirs, files in os.walk(BASE_DIR):
            if ".git" in dirs:
                os.chdir(root)
                try:
                    repo_name = os.path.basename(root)
                    print(f"📁 Repository: {repo_name}")
                    log_cmd = [
                        "git", "log",
                        f"--author={AUTHOR}",
                        f"--since={SINCE}",
                        f"--until={UNTIL}",
                        "--pretty=format:%h %ad | %s", "--date=short"
                    ]
                    output = subprocess.check_output(log_cmd).decode("utf-8").strip()
                    if output:
                        print(output)
                    else:
                        print("No commits found.\n")
                except Exception as e:
                    print(f"Error reading {root}: {e}")

                repo_full_name = get_github_repo_url()
                if repo_full_name:
                    prs = get_pull_requests(repo_full_name, AUTHOR)
                    print("\n🔀 Pull Requests:")
                    print("\n".join(f"  {pr}" for pr in prs) if prs else "  No PRs found.")
                else:
                    print("  ⚠️ Could not detect GitHub repo URL.")

                dirs[:] = []
    except Exception as e:
        print(str(e))
