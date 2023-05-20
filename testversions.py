import os
import subprocess
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]  # Get the file path from the command-line argument
    git_command = f"git log --pretty=format:%h -- {file_path}"
    revisions = subprocess.check_output(git_command, shell=True, text=True).splitlines()

    # Save the current branch
    current_branch = subprocess.check_output("git branch --show-current", shell=True, text=True).strip()

    results = []

    for revision in revisions:
        print(f"Processing revision {revision}")
        os.system(f"git checkout {revision}")

        ant_realclean = "ant realclean"
        ant_jar = "ant jar"
        ant_test = "ant test -Dtest.name=VectorTypeTest"

        realclean_result = os.system(ant_realclean)
        jar_result = os.system(ant_jar)
        test_result = os.system(ant_test)

        if realclean_result == 0 and jar_result == 0 and test_result == 0:
            results.append((revision, "successful"))
        else:
            results.append((revision, "failed"))

    # Restore the original branch
    os.system(f"git checkout {current_branch}")

    # Print the results
    print("\nResults:")
    for revision, status in results:
        print(f"[{revision}] {status}")

if __name__ == "__main__":
    main()
