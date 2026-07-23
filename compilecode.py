from pathlib import Path


# ---------------------------------------------------------
# PROJECT LOCATION
# ---------------------------------------------------------

# This assumes this script is located inside the
# garden_app project folder.

PROJECT_ROOT = Path(__file__).resolve().parent

# Output TXT file
OUTPUT_FILE = PROJECT_ROOT / "compiled_code.txt"


# ---------------------------------------------------------
# FOLDERS TO IGNORE
# ---------------------------------------------------------

IGNORED_FOLDERS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "build",
    "dist",
}


# ---------------------------------------------------------
# FIND PYTHON FILES
# ---------------------------------------------------------

python_files = []

for file in PROJECT_ROOT.rglob("*.py"):

    # Ignore folders listed above
    if any(
        folder in file.parts
        for folder in IGNORED_FOLDERS
    ):
        continue

    # Don't include this compiler script itself
    if file.name == Path(__file__).name:
        continue

    python_files.append(file)


# Sort files alphabetically
python_files.sort()


# ---------------------------------------------------------
# CREATE TXT FILE
# ---------------------------------------------------------

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as output:

    output.write(
        "GARDEN APP - COMPILED PYTHON SOURCE CODE\n"
    )

    output.write("=" * 80 + "\n\n")


    for python_file in python_files:

        # Path relative to garden_app
        relative_path = python_file.relative_to(
            PROJECT_ROOT
        )


        # File separator
        output.write("\n")
        output.write("=" * 80 + "\n")
        output.write(
            f"FILE: {relative_path}\n"
        )
        output.write("=" * 80 + "\n\n")


        # Read Python code
        try:

            code = python_file.read_text(
                encoding="utf-8"
            )

            output.write(code)

        except Exception as error:

            output.write(
                f"[ERROR READING FILE: {error}]"
            )


        output.write("\n\n")


# ---------------------------------------------------------
# COMPLETE
# ---------------------------------------------------------

print()
print("=" * 50)
print("GARDEN APP CODE COMPILATION COMPLETE")
print("=" * 50)
print()
print(f"Python files found: {len(python_files)}")
print()
print(f"Compiled code saved to:")
print(OUTPUT_FILE)
