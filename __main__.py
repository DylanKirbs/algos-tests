import argparse
from pathlib import Path
from sys import exit
import shutil
import subprocess as sp
import time

# Status labels
PASS = "\x1b[32mPASS\x1b[0m"
FAIL = "\x1b[31mFAIL\x1b[0m"
EXCP = "\x1b[35mEXCP\x1b[0m"
CHNG = "\x1b[33mGENR\x1b[0m"
SAME = "\x1b[33mSAME\x1b[0m"
COMP = "\x1b[34mCOMP\x1b[0m"
EXEC = "\x1b[36mEXEC\x1b[0m"

parser = argparse.ArgumentParser(
    prog="Algos Test Runner", description="Executes a specific problem's tests"
)

# python3 __main__.py [options] <A> [contains...]
parser.add_argument("problem", help="The two letter problem code")
parser.add_argument(
    "contains",
    nargs="*",
    help="Any test that contains any of the given strings will be executed",
)

# Options
parser.add_argument(
    "--gen", action="store_true", help="Enables generation of test cases"
)
parser.add_argument("--gc-info", action="store_true", help="Enable GC info")
parser.add_argument("--enable-assertions", action="store_true", help="Enable assertions")
parser.add_argument("--no-mem-limit", action="store_true", help="Disable memory limit")

args = parser.parse_args()

# Directories
problem_dir = Path(args.problem).resolve()
src_dir = problem_dir / "src"
bin_dir = problem_dir / "bin"
out_dir = problem_dir / "out"
main_file = src_dir / "Main.java"

if not main_file.exists():
    print("Main.java not found in", src_dir)
    exit(1)

cases_dir = Path("test") / "cases" / args.problem
if not cases_dir.exists():
    print("No test cases found for", args.problem)
    exit(1)

# Rebuild bin & out
shutil.rmtree(bin_dir, ignore_errors=True)
shutil.rmtree(out_dir, ignore_errors=True)
bin_dir.mkdir()
out_dir.mkdir()

print(COMP, "Java program")
try:
    res = sp.run(["javac", "-d", str(bin_dir)] + [str(f) for f in src_dir.glob("*.java")])
    if res.returncode != 0:
        print("Compilation failed.")
        exit(1)
except Exception as e:
    print("Python exception during compilation:", e)
    exit(1)

# Runtime flags
flags = []
if not (args.gen or args.no_mem_limit):
    flags += ["-Xmx16m"]
if args.gc_info:
    flags += ["-XX:+PrintGCDetails"]
if args.enable_assertions:
    flags += ["-ea"]

cases = sorted(cases_dir.glob("*.in"))
cases = filter(
    lambda x: any(s in x.name for s in args.contains) if args.contains else True,
    cases,
)
if not cases:
    print("No cases found for", args.problem, "with the given filters.")
    exit(1)


print(EXEC, "Tests with flags:", flags)
for case in cases:
    case = case.name.split(".")[0]
print("Running with flags:", flags)

# Get list of cases
if args.case:
    case_list = [args.case]
else:
    case_list = sorted(f.name for f in cases_dir.glob("*.in"))

for case_file in case_list:
    case_name = Path(case_file).stem
    in_file = cases_dir / f"{case_name}.in"
    out_file = cases_dir / f"{case_name}.out"

    if not in_file.exists():
        print(EXCP, case_name, "input file not found")
        continue

    try:
        start = time.perf_counter()
        cmd = ["java", "-cp", str(bin_dir)] + flags + ["Main"]
        res = sp.run(cmd, input=in_file.read_text(), stdout=sp.PIPE, text=True)
        elapsed_ms = (time.perf_counter() - start) * 1000

        # Save result
        (out_dir / f"{case_name}.out").write_text(res.stdout)

        if res.returncode != 0:
            print(EXCP, case_name, "runtime exception")
            continue

        expected = out_file.read_text() if out_file.exists() else ""
        diff = res.stdout != expected

        if args.gen:
            out_file.write_text(res.stdout)
            print(CHNG if diff else SAME, case_name, f"{elapsed_ms:.0f}ms")
        else:
            print(FAIL if diff else PASS, case_name, f"{elapsed_ms:.0f}ms")

    except Exception as e:
        print(EXCP, case_name, "in Python process:", e)
