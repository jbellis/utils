import os
import subprocess
import sys

def main():
    # Save the current branch
    current_branch = subprocess.check_output("git branch --show-current", shell=True, text=True).strip()

    results = []

    print("Enter revisions separated by newlines (Ctrl+D to finish):")
    for revision in sys.stdin:
        revision = revision.strip()
        print(f"Processing revision {revision}")
        os.system(f"git checkout {revision}")

        ant_realclean = "ant realclean"
        ant_jar = "ant jar -Dno-checkstyle"
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
