import argparse
import shutil
import subprocess as sp
import time
from pathlib import Path
from sys import exit
import re
import subprocess as sp
import time


def time_output_chunks(java_cmd, full_input) -> tuple[int, str, str, list[float]]:
    """
    The function runs a Java program with the given command and input,
    captures its output, and measures the time taken for each test case.

    returns:
        - return code of the Java process
        - output text from the Java process
        - error text from the Java process
        - list of times taken for each test case in milliseconds
    """
    proc = sp.Popen(
        java_cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, text=True, bufsize=1
    )

    if not (proc and proc.stdin and proc.stdout and proc.stderr):
        return -1, "", "", []

    # Send full input
    proc.stdin.write(full_input)
    proc.stdin.close()

    times = []
    out_buff = []
    current_test = 1
    start_time = time.perf_counter()

    pattern = re.compile(r"(\d+):")

    while True:
        out_line = proc.stdout.readline()
        if not out_line:
            break
        out_line = out_line.rstrip()

        out_buff.append(out_line)

        match = pattern.match(out_line)
        if match and int(match.group(1)) == current_test:
            now = time.perf_counter()
            if current_test > 1:
                # skip the line "1:" because it is the start of the first test (not the end)
                elapsed = (now - start_time) * 1000
                times.append(round(elapsed, 4))
            start_time = now
            current_test += 1

    # Catch final test case time
    end_time = time.perf_counter()
    elapsed = (end_time - start_time) * 1000
    times.append(round(elapsed, 4))

    proc.wait()

    return proc.returncode, "\n".join(out_buff) + "\n", proc.stderr.read(), times


# Output labels
PASS = "\x1b[32mPASS\x1b[0m"
FAIL = "\x1b[31mFAIL\x1b[0m"
EXCP = "\x1b[35mEXCP\x1b[0m"
CHNG = "\x1b[33mGENR\x1b[0m"
SAME = "\x1b[33mSAME\x1b[0m"
COMP = "\x1b[34mCOMP\x1b[0m"
EXEC = "\x1b[36mEXEC\x1b[0m"

# Argument parser
parser = argparse.ArgumentParser(
    prog="Algos Test Runner", description="Executes algos tests"
)
parser.add_argument("problem", help="The two letter problem code")
parser.add_argument(
    "contains",
    nargs="*",
    help="Only tests containing any of these substrings in their name will be run",
)
parser.add_argument("--gen", action="store_true", help="Generate .out files")
parser.add_argument("--gc-info", action="store_true", help="Enable GC info")
parser.add_argument(
    "--enable-assertions", action="store_true", help="Enable assertions"
)
parser.add_argument("--no-mem-limit", action="store_true", help="Disable memory limit")

args = parser.parse_args()

# Paths
problem_dir = Path(args.problem).resolve()
main = problem_dir / "Main.java"
bin = problem_dir / "bin"
out = problem_dir / "out"
test_dir = Path("test").resolve()
cases_dir = test_dir / "cases" / args.problem

# Validate input
if not main.exists():
    print("Could not find problem directory or Main.java")
    exit(1)
if not cases_dir.exists():
    print("No cases for", args.problem, "found.")
    exit(1)

# Clean and prepare bin and output directories
shutil.rmtree(bin, ignore_errors=True)
shutil.rmtree(out, ignore_errors=True)
bin.mkdir()
out.mkdir()

# Compile Java sources
print(COMP, "Compiling Java")
try:
    sp.run(
        ["javac", "-d", str(bin)] + [str(f) for f in problem_dir.glob("*.java")],
        check=True,
    )
except sp.CalledProcessError:
    print("Java compilation failed.")
    exit(1)

# Java execution flags
flags = []
if not args.gen and not args.no_mem_limit:
    flags += ["-Xmx16m"]
if args.gc_info:
    flags += ["-XX:+PrintGCDetails"]
if args.enable_assertions:
    flags += ["-ea"]

# Collect test cases
cases = list(
    filter(
        lambda x: any(s in x.name for s in args.contains) if args.contains else True,
        sorted(cases_dir.glob("*.in")),
    )
)

if not cases:
    print("No matching cases found.")
    exit(1)

print(EXEC, "Running tests with flags:", flags)
failed = 0

# Run each test case
for case_path in cases:
    case_name = case_path.stem
    try:
        input_text = case_path.read_text()
        returncode, output_text, error_text, times = time_output_chunks(
            ["java", "-cp", str(bin), *flags, "Main"],
            input_text,
        )

        (out / case_name).with_suffix(".out").write_text(output_text)

        if returncode != 0:
            print(EXCP, case_name, "during java execution")
            continue

        expected_output_file = (cases_dir / case_name).with_suffix(".out")
        expected_output = (
            expected_output_file.read_text() if expected_output_file.exists() else ""
        )

        output_differs = output_text != expected_output

        if args.gen and case_name != "spec":
            (cases_dir / case_name).with_suffix(".out").write_text(output_text)
            print((CHNG if output_differs else SAME), case_name)
        else:
            if output_differs:
                print(FAIL, case_name, times)
                failed += 1
            else:
                print(PASS, case_name, times)

    except Exception as e:
        print(EXCP, case_name, "in python process:", e)

print(f"\nSummary: {len(cases) - failed}/{len(cases)} tests passed.")
exit(failed)
