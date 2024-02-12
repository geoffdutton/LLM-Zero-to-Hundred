import os
import re
import argparse
from typing import List


def modify_requirements_txt(requirements_txt: str) -> str:
    modified_lines = []
    lines = requirements_txt.split("\n")
    for line in lines:

        if line:  # checks if line is not empty
            if (
                line.startswith("#") or "platform" in line
            ):  # Skip comments and platform line
                continue

            parts = list(filter(lambda x: x.strip(), line.split("=")))  # Split on '='
            if len(parts) >= 2:
                fixed_line = parts[0] + "==" + parts[1]
                modified_lines.append(fixed_line)
            else:
                modified_lines.append(line)
    return "\n".join(modified_lines)


def remove_parts_of_lines(input_filename, output_filename):
    """Removes comments and metadata from lines in a conda environment file.

    Args:
        input_filename (str): The path to the input conda environment file.
        output_filename (str): The path to the output file where the processed lines will be written.
    """

    with open(input_filename, "r") as infile, open(output_filename, "w") as outfile:
        for line in infile:
            if (
                line.startswith("#") or "platform" in line
            ):  # Skip comments and platform line
                continue

            parts = line.split("=")  # Split on '='
            if len(parts) >= 2:
                outfile.write(
                    parts[0] + "=" + parts[1] + "\n"
                )  # Reassemble package and version


def process_requirements_txt_file(requirements_txt: str) -> str:
    backup_requirements_text = requirements_txt.replace(".txt", "_fixed.txt")
    with (
        open(requirements_txt, "r") as src_file,
        open(backup_requirements_text, "w") as fixed_file,
    ):
        requirements = src_file.read()
        fixed_requirements = modify_requirements_txt(requirements)
        fixed_file.write(fixed_requirements)

    return fixed_requirements


def main():
    parser = argparse.ArgumentParser(description="Modify requirements.txt files.")
    parser.add_argument("requirements_txt", type=str, help="Path to requirements.txt")
    args = parser.parse_args()
    print(args)
    #
    # modified_requirements = process_requirements_txt(args.requirements_txt)
    #
    fixed = process_requirements_txt_file(args.requirements_txt)

    print(
        f"""
Fixed:

<<<<
{fixed}
>>>>
""".format(
            fixed=fixed
        )
    )


if __name__ == "__main__":
    main()
