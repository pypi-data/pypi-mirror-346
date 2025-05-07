import subprocess
from datetime import datetime

def get_uncommitted_files():
    try:
        output = subprocess.check_output(['git', 'status', '--porcelain'])
        lines = output.decode().splitlines()
        return lines
    except Exception:
        return None

def get_last_commit_time():
    try:
        output = subprocess.check_output(
            ['git', 'log', '-1', '--format=%ct']
        )
        timestamp = int(output.decode().strip())
        return datetime.fromtimestamp(timestamp)
    except Exception:
        return None
    
def parse_git_status_lines(lines):
    """
    Parse git status --porcelain output lines into structured info.
    Returns a list of tuples: (status, filename)
    """
    parsed = []
    for line in lines:
        status_code = line[:2].strip()
        filename = line[3:] if len(line) > 3 else ""
        parsed.append((status_code, filename))
    return parsed