# Algos Tests


## Directory Structure

Your directory must be structured as follows:

```
.
├── DD
│   └──Main.java
└── test
    ├── cases
    │   └── DD
    │       └── ...
    ├── __main__.py
    └── README.md
```

Where each directory is named after the problem code.

## Execution

```sh
python3 test <problem_code>
```

> Note: The stderr stream is printed out after each test case is run, so it is recommended to print debug statements to stderr.

## Generating test cases

Create your ".in" file in the cases directory and execute

```sh
python3 test --gen <problem_code>
```
This will generate a ".out" file with the expected output (from your program's execution).

> Warning: This will overwrite any existing ".out" file.