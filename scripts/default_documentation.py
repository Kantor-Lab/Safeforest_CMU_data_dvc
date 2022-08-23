from email.policy import default
import glob
import argparse
from pathlib import Path
import shutil
import ubelt as ub
import os


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input-dir",
        default="data",
        help="Top level directory containing dated folders",
    )
    parser.add_argument(
        "--collect-readme",
        default="templates/collect_README.md",
        help="Path to the default readme for individual collects",
    )
    parser.add_argument(
        "--site-readme",
        default="templates/site_README.md",
        help="Path to the default readme for each site",
    )
    parser.add_argument(
        "--overwrite-sites",
        action="store_true",
        help="Overwrite the existing site readme",
    )
    parser.add_argument(
        "--overwrite-collects",
        action="store_true",
        help="Overwrite the existing collect readme",
    )
    parser.add_argument(
        "--move-files",
        action="store_true",
        help="Move files into raw, create processed_1 and processed_2",
    )

    parser.add_argument(
        "--move-files-pattern",
        help="Pattern to use to search for folders to move",
        default="site_*/*/collect_*",
    )
    parser.add_argument(
        "--move-files-subdirectory", help="Subdirectory of raw to move files into",
    )
    args = parser.parse_args()
    return args


def copy_file(input_file, output_dir, overwrite=False):
    output_file = Path(output_dir, "README.md")
    if overwrite or not output_file.is_file():
        shutil.copy(input_file, output_file)


def copy_default_readme(folder, readme, search_string, overwrite):
    files = Path(folder).glob(search_string)
    files = [f for f in files if "template" not in str(f)]
    [copy_file(readme, f, overwrite) for f in files]


def rename_to_raw(folder, subfolder=None):
    breakpoint()
    if not os.path.isdir(folder):
        return

    parent = folder.parent

    # Create raw folder and move data there
    raw = Path(folder, "raw")
    if not os.path.isdir(raw):
        breakpoint()
        # Optionally append subfolder
        if subfolder is not None:
            raw = Path(raw, subfolder)
        temp = Path(parent, "temp")
        shutil.move(folder, temp)
        ub.util_path.ensuredir(raw.parent, mode=0o0755)
        shutil.move(temp, raw)

    # Create processed folders if absent
    proc_1 = Path(folder, "processed_1")
    proc_2 = Path(folder, "processed_2")
    ub.util_path.ensuredir(proc_1, mode=0o0755)
    ub.util_path.ensuredir(proc_2, mode=0o0755)


def move_files(folder, search_string="site_*/*/collect_*", subdir=None):
    files = Path(folder).glob(search_string)
    [rename_to_raw(f, subdir) for f in files]


if __name__ == "__main__":
    args = parse_args()

    if args.move_files:
        move_files(
            args.input_dir,
            search_string=args.move_files_pattern,
            subdir=args.move_files_subdirectory,
        )
    else:
        copy_default_readme(
            args.input_dir,
            args.collect_readme,
            "site_*/*/collect_*",
            args.overwrite_collects,
        )
        copy_default_readme(
            args.input_dir, args.site_readme, "site_*", args.overwrite_sites
        )

