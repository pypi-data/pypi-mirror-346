import os
import sys
import runpy


def main():
    make_file = "Bakery.py"
    if os.path.exists(make_file):
        sys.argv = [make_file] + sys.argv[1:]
        runpy.run_path(make_file, run_name="__main__")
    else:
        print(f"Error: Could not find '{make_file}' in the current directory.")
        exit(1)


if __name__ == "__main__":
    main()
