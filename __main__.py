import argparse
from pathlib import Path
from sys import exit
import shutil
import subprocess as sp
import time

PASS = "\x1b[32mPASS\x1b[0m"
FAIL = "\x1b[31mFAIL\x1b[0m"
EXCP = "\x1b[35mEXCP\x1b[0m"
CHNG = "\x1b[33mGENR\x1b[0m"
SAME = "\x1b[33mSAME\x1b[0m"
COMP = "\x1b[34mCOMP\x1b[0m"
EXEC = "\x1b[36mEXEC\x1b[0m"

parser = argparse.ArgumentParser(
    prog="Algos Test Runner", description="Executes algos tests"
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
parser.add_argument(
    "--enable-assertions", action="store_true", help="Enable assertions"
)
parser.add_argument("--no-mem-limit", action="store_true", help="Disable memory limit")

args = parser.parse_args()

problem_dir = Path(args.problem).resolve()
main = problem_dir / "Main.java"
bin = problem_dir / "bin"
out = problem_dir / "out"


if not main.exists():
    print("Could not find problem directory or Main.java")
    exit(1)

test_dir = Path("test").resolve()
cases_dir = test_dir / "cases" / args.problem

if not cases_dir.exists():
    print("No cases for", args.problem, "found.")
    exit(1)

shutil.rmtree(bin, ignore_errors=True)
shutil.rmtree(out, ignore_errors=True)
bin.mkdir()
out.mkdir()

print(COMP, "Java program")
try:
    res = sp.run(
        ["javac", "-d", str(bin)] + [str(f) for f in problem_dir.glob("*.java")]
    )
    if res.returncode != 0:
        print("Java exception during compilation")
        exit(1)
except Exception as e:
    print("Python exception during compilation", e)
    exit(1)

flags = []
# Limit memory to 16MB
if not (args.gen or args.no_mem_limit):
    flags += ["-Xmx16m"]

# GC Logging
if args.gc_info:
    flags += ["-XX:+PrintGCDetails"]

# Enforce Assertions
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
    try:
        start = time.perf_counter()
        cmd = ["java", "-cp", str(bin)] + flags + ["Main"]
        res = sp.run(
            cmd,
            input=(cases_dir / f"{case}.in").read_text(),
            stdout=sp.PIPE,
            text=True,
        )
        elapsed_ms = (time.perf_counter() - start) * 1000

        # Save output
        (out / f"{case}.out").write_text(res.stdout)

        if res.returncode != 0:
            print(EXCP, case, "during java execution")
            continue

        diff = True
        if res.stdout and (cases_dir / f"{case}.out").exists():
            diff = res.stdout != (cases_dir / f"{case}.out").read_text()

        # If generation mode save output to cases dir else compare with expected output
        if args.gen and case != "spec":
            (cases_dir / f"{case}.out").write_text(res.stdout)
            if diff:
                print(CHNG, end=" ")
            else:
                print(SAME, end=" ")
        else:
            if diff:
                print(FAIL, end=" ")
            else:
                print(PASS, end=" ")
        print(case, f"{elapsed_ms:.0f}ms")

    except Exception as e:
        print(EXCP, case, "in python process", e)
