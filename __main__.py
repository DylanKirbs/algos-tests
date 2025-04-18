import argparse
import shutil
import subprocess as sp
import time
from pathlib import Path
from sys import exit

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
# case fmt str with each cell to 20 chars
case_out_fmt_str = "{status} | {name:<20} | {time:<10} | {avg_time:<10}"
print(
    case_out_fmt_str.format(
        status="STAT", name="Test Name", time="Time (ms)", avg_time="Avg Time (ms)"
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
                    status=EXCP, name=case_name, time="N/A", avg_time="N/A"
                )
            )
            failed += 1
            continue

        expected_output_file = (cases_dir / case_name).with_suffix(".out")
        expected_output = (
            expected_output_file.read_text() if expected_output_file.exists() else ""
        )

        output_differs = output_text != expected_output

        if args.gen and case_name != "spec":
            (cases_dir / case_name).with_suffix(".out").write_text(output_text)
            print(
                case_out_fmt_str.format(
                    status=CHNG if output_differs else SAME,
                    name=case_name,
                    time=f"{elapsed_ms:.0f}ms",
                    avg_time=f"{elapsed_ms/num_cases:.0f}ms",
                )
            )
        else:
            if output_differs:
                print(
                    case_out_fmt_str.format(
                        status=FAIL,
                        name=case_name,
                        time=f"{elapsed_ms:.0f}ms",
                        avg_time=f"{elapsed_ms/num_cases:.0f}ms",
                    )
                )
                failed += 1
            else:
                print(
                    case_out_fmt_str.format(
                        status=PASS,
                        name=case_name,
                        time=f"{elapsed_ms:.0f}ms",
                        avg_time=f"{elapsed_ms/num_cases:.0f}ms",
                    )
                )

    except Exception as e:
        print(EXCP, case_name, "in python process:", e)

print(f"\nSummary: {len(cases) - failed}/{len(cases)} tests passed.")
exit(failed)
