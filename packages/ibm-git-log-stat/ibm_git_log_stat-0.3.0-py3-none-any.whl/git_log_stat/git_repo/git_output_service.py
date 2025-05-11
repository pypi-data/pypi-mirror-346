from pathlib import Path

import pandas as pd

from git_log_stat.app_logs.logger_service import IBMLogger
from git_log_stat.git_repo.git_nlp import generate_commit_summary_docx, generate_commit_summary_pdf, \
    generate_commit_summary_pptx


class GitOutputService:

    def __init__(self):
        self.log = IBMLogger("GitOutputService").get_logger()

    def generate_output_file(self, output_format, output_file_name, output):
        match output_format:
            case "txt":
                self.generate_txt(output_file_name, output)
            case "pdf":
                self.generate_pdf(str(output_file_name), output)
            case "xls":
                self.generate_xls(output_file_name, output)
            case "csv":
                self.log.info("CSV not implemented yet")
            case "tsv":
                self.log.info("TSV not implemented yet")
            case "docx":
                self.generate_docx(str(output_file_name), output)
            case "ppt":
                self.generate_ppt(str(output_file_name), output)

    def get_commit_count(self, output: str):
        self.log.info("Commit Count called")
        return str(len(output.split("\n")))

    def generate_txt(self, output_file, output):
        try:
            out_file_path = Path(output_file).resolve()
            with open(out_file_path, 'w') as out_file:
                out_file.write(output)
                out_file.flush()
            self.log.info("Output File written to %s", out_file_path)
        except Exception as e:
            self.log.error(str(e), exc_info=True)

    def generate_xls(self, output_file, output: str):
        try:
            data = []
            output_lines = output.split("\n")
            for line in output_lines:
                parts = [part.strip() for part in line.split("|", 3)]
                if len(parts) == 4:
                    date, author, commit_hash, message = parts
                    data.append({
                        "Date": date,
                        "Author": author,
                        "Commit": commit_hash,
                        "Message": message
                    })

            df = pd.DataFrame(data)
            df.to_excel(output_file, index=False, engine='openpyxl')
            self.log.info(f"✅ Excel file written to: {output_file}")
        except Exception as e:
            self.log.error(str(e), exc_info=True)

    def generate_pdf(self, output_file_name, output):
        self.log.info("generating pdf %s", output_file_name)
        generate_commit_summary_pdf(output, output_file_name)

    def generate_docx(self, output_file_name, output):
        self.log.info("generating docx %s", output_file_name)
        generate_commit_summary_docx(output, output_file_name)

    def generate_ppt(self, output_file_name, output):
        self.log.info("generating ppt %s", output_file_name)
        generate_commit_summary_pptx(output, output_file_name)
