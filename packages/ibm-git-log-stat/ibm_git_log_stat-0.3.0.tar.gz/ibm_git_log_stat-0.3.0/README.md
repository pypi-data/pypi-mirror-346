# IBM Git Log Stat

A lightweight CLI tool to track your **git commits** and **GitHub pull requests** within a date range, across multiple
repositories.

## 🔧 Installation

```bash
pip install ibm-git-log-stat
```

## Usage

```bash
export GITHUB_TOKEN="provide_your_github_token_here"
ibm-git-log-stat \
  --base-dir ~/projects \
  --author "you@example.com" \
  --github-user yourgithubusername \
  --start-date 2025-04-01 \
  --end-date 2025-04-30 \
  --output-format xls,txt,pdf,docx,ppt \
  --check-pr true (remove the argument if u want to disable PR) 

Arguments can also be set using environment variables:

BASE_DIR
AUTHOR
GITHUB_USER
START_DATE
END_DATE
OUTPUT_FORMAT

Just export before running if you dont want to specify everytime in parameter
```


