import os
import subprocess

from git_log_stat.app_logs.logger_service import IBMLogger
from git_log_stat.git_repo.git_log_format_service import GitLogFormatService
from git_log_stat.git_repo.git_repo_service import GitRepoService


class GitLogStatService:

    def __init__(self):
        self.log = IBMLogger("GitLogStatService").log
        self.repo_service = GitRepoService()
        self.git_log_format_service = GitLogFormatService()

    def get_commits(self, base_dir, author, start_date, end_date):
        try:
            self.log.debug("getting git commits on base dir %s", base_dir)
            # Check if base directory given in arg exists
            if not os.path.isdir(base_dir):
                raise ValueError(f"Invalid base directory: {base_dir}")
            output = ""
            for root, dirs, files in os.walk(base_dir):
                if ".git" in dirs:
                    os.chdir(root)
                    try:
                        repo_name = os.path.basename(root)
                        self.log.info(f"📁 Repository: {repo_name}")
                        if author == "*":
                            log_cmd = [
                                "git", "log",
                                f"--since={start_date}",
                                f"--until={end_date}",
                                f"--pretty={self.git_log_format_service.get_log_format_detailed()}", "--date=short"
                            ]
                        else:
                            log_cmd = [
                                "git", "log",
                                f"--author={author}",
                                f"--since={start_date}",
                                f"--until={end_date}",
                                f"--pretty={self.git_log_format_service.get_log_format_detailed()}", "--date=short"
                            ]
                        output = subprocess.check_output(log_cmd).decode("utf-8").strip()
                        if output:
                            print(output)
                        else:
                            print("No commits found.\n")
                    except Exception as e:
                        print(f"Error reading {root}: {e}")

                dirs[:] = []
                return output
        except Exception as e:
            print(str(e))
            return None

    def get_pull_requests(self, api_url, repo_full_name, author, headers, start_date, end_date):
        return self.repo_service.get_pull_requests(api_url, repo_full_name, author, headers, start_date, end_date)
