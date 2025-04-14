import argparse
from pathlib import Path
from sys import exit
import shutil
import subprocess as sp
import time

PASS = "\x1b[32mPASS\x1b[0m"
FAIL = "\x1b[31mFAIL\x1b[0m"
EXCP = "\x1b[35mEXCP\x1b[0m"

parser = argparse.ArgumentParser(
    prog="Algos Test Runner", description="Executes algos tests"
)

parser.add_argument("problem", help="The two letter problem code")

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

print("Compiling")
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

print("Executing tests")
for case in cases_dir.glob("*.in"):
    case = case.name.split(".")[0]
    try:
        start = time.perf_counter()
        res = sp.run(
            ["java", "-cp", str(bin), "-Xmx16m", "Main"],
            input=(cases_dir / f"{case}.in").read_text(),
            capture_output=True,
            text=True,
        )
        elapsed_ms = (time.perf_counter() - start) * 1000

        # Save output
        (out / f"{case}.out").write_text(res.stdout)
        (out / f"{case}.err").write_text(res.stderr)
        print(res.stderr)

        if res.returncode != 0:
            print(EXCP, case, "during java execution")
            continue

        # Compare output
        if res.stdout != (cases_dir / f"{case}.out").read_text():
            print(FAIL, end=" ")
        else:
            print(PASS, end=" ")
        print(case, f"{elapsed_ms:.0f}ms")

    except Exception as e:
        print(EXCP, case, "in python process")
