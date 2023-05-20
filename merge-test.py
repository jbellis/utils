import subprocess
import sys
import re

def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode().strip()

def count_conflicts(commit):
    conflict_markers = 0
    files_with_conflicts = set()
    try:
        # Attempt a test merge
        subprocess.check_output(f"git merge --no-commit --no-ff {commit}", shell=True)
    except subprocess.CalledProcessError:
        # If merge failed, count conflict markers and files with conflicts
        diff_output = run_cmd("git diff")
        conflict_markers = diff_output.count('>>>>>>') + diff_output.count('======') + diff_output.count('<<<<<<')
        files_with_conflicts = set(re.findall(r'\+\+\+ b/(.*)', diff_output))
    finally:
        # Always try to abort the merge, even if no merge was started or if it failed
        subprocess.call("git merge --abort", shell=True)
    return conflict_markers, len(files_with_conflicts)

# get the commit hash for X and name of branch A from command line arguments
commit_x = sys.argv[1]
branch_a = sys.argv[2]

# get all the commits from commit X to A's HEAD
commits = run_cmd(f"git rev-list {commit_x}..{branch_a}").split()

print(f"Common ancestor: {commit_x}")
for commit in commits[::-1]:  # Reverse the list as rev-list gives commits from newest to oldest
    conflicts, files = count_conflicts(commit)
    print(f"Commit {commit}: {conflicts} conflicts in {files} files")
