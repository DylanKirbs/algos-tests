import argparse
import shutil
import subprocess as sp
import time
from pathlib import Path
from sys import exit

# Output labels
FAIL_LABEL = "\x1b[31mFAIL\x1b[0m"

PASS_LABEL = "\x1b[32mPASS\x1b[0m"

CHANGE_LABEL = "\x1b[33mGENR\x1b[0m"
SAME_LABEL = "\x1b[33mSAME\x1b[0m"

COMPILE_LABEL = "\x1b[34mCOMP\x1b[0m"

EXCEPTION_LABEL = "\x1b[35mEXCP\x1b[0m"
TIMEOUT_LABEL = "\x1b[35mTIME\x1b[0m"

EXECUTE_LABEL = "\x1b[36mEXEC\x1b[0m"
STATUS_LABEL = "\x1b[36mSTAT\x1b[0m"

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
if not cases_dir.exists():
    print("No cases for", args.problem, "found.")
    exit(1)
if not main.exists():
    print("Could not find problem directory or Main.java for", args.problem)
    exit(1)


# Clean and prepare bin and output directories
shutil.rmtree(bin, ignore_errors=True)
shutil.rmtree(out, ignore_errors=True)
bin.mkdir()
out.mkdir()

# Compile Java sources
print(COMPILE_LABEL, "Compiling Java")
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

timeout_file = cases_dir / ".timeout"
timeout = int(timeout_file.read_text().strip()) if timeout_file.exists() else None

if not cases:
    print("No matching cases found.")
    exit(1)

print("Breakdown of labels:")
print("", FAIL_LABEL, "- your output is incorrect")
print("", PASS_LABEL, "- your output is correct and ran in time")
print("", TIMEOUT_LABEL, "- your output is correct but the average time exceeds the allowed time")
print("", EXCEPTION_LABEL, "- your program terminiated with an exception")

print(
    EXECUTE_LABEL,
    "Running tests with flags:",
    flags,
    "and avg case timeout:",
    f"{timeout}ms",
)
failed = 0

# Run each test case
# case fmt str with each cell to 20 chars
case_out_fmt_str = "{status} | {name:<20} | {time:<10} | {avg_time:<10}"
print(
    case_out_fmt_str.format(
        status=STATUS_LABEL,
        name="Test Name",
        time="Time (ms)",
        avg_time="Avg Time (ms)",
    )
)
for case_path in cases:
    case_name = case_path.stem
    try:
        input_text: str = case_path.read_text()
        # read the first number of the input as the number of cases
        num_cases = int(input_text.split(maxsplit=1)[0])
        start = time.perf_counter()

        result = sp.run(
            ["java", "-cp", str(bin), *flags, "Main"],
            input=input_text,
            stdout=sp.PIPE,
            text=True,
        )
        elapsed_ms = (time.perf_counter() - start) * 1000
        output_text = result.stdout
        (out / case_name).with_suffix(".out").write_text(output_text)

        if result.returncode != 0:
            print(
                case_out_fmt_str.format(
                    status=EXCEPTION_LABEL, name=case_name, time="N/A", avg_time="N/A"
                )
            )
            failed += 1
            continue

        expected_output_file = (cases_dir / case_name).with_suffix(".out")
        expected_output = (
            expected_output_file.read_text() if expected_output_file.exists() else ""
        )

        output_differs = output_text != expected_output
        avg_time = elapsed_ms / num_cases

        if args.gen and case_name != "spec":
            (cases_dir / case_name).with_suffix(".out").write_text(output_text)
            print(
                case_out_fmt_str.format(
                    status=CHANGE_LABEL if output_differs else SAME_LABEL,
                    name=case_name,
                    time=f"{elapsed_ms:.0f}ms",
                    avg_time=f"{avg_time:.0f}ms",
                )
            )
        else:
            status = PASS_LABEL
            if output_differs:
                status = FAIL_LABEL
                failed += 1
            elif timeout and avg_time > timeout:
                status = TIMEOUT_LABEL
                failed += 1

            print(
                case_out_fmt_str.format(
                    status=status,
                    name=case_name,
                    time=f"{elapsed_ms:.0f}ms",
                    avg_time=f"{avg_time:.0f}ms",
                )
            )

    except Exception as e:
        print(EXCEPTION_LABEL, case_name, "in python process:", e)

print(f"\nSummary: {len(cases) - failed}/{len(cases)} tests passed.")
exit(failed)
