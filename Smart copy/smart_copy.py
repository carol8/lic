import os
import re
import shutil
import argparse
from tqdm import tqdm
import math


def copy_files_within_range(source_dir, dest_dir, prefix, lower_limit, upper_limit, create_dest):
    # Ensure the destination directory exists if the create_dest flag is set
    if create_dest:
        os.makedirs(dest_dir, exist_ok=True)
    elif not os.path.exists(dest_dir):
        print(f"Error: The destination directory '{dest_dir}' does not exist.")
        return

    # List all files in the source directory
    all_files = os.listdir(source_dir)

    # Create the filtering criteria based on the specified limits
    filtered_files = [f for f in all_files if
                      any(f.startswith(f'{prefix}_{i}_') for i in range(lower_limit, upper_limit + 1))]

    # Copy the filtered files to the destination directory with progress bar
    for file_name in tqdm(filtered_files, desc="Copying files", unit="file"):
        full_file_name = os.path.join(source_dir, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, dest_dir)

    print(f"Copied {len(filtered_files)} files to {dest_dir}")


def numerical_sort(value):
    numbers = re.findall(r'\d+', value)
    return [int(num) for num in numbers]


def copy_files_within_percentage(source_dir, dest_dir, percentage, create_dest):
    # Ensure the destination directory exists if the create_dest flag is set
    if create_dest:
        os.makedirs(dest_dir, exist_ok=True)
    elif not os.path.exists(dest_dir):
        print(f"Error: The destination directory '{dest_dir}' does not exist.")
        return

    # List all files in the source directory
    all_files = sorted(os.listdir(source_dir), key=numerical_sort)
    # print('\n'.join(all_files))
    # print(len(all_files))

    # Calculate the number of files to copy
    num_files_to_copy = math.ceil(len(all_files) * (percentage / 100))

    # print(num_files_to_copy)

    # Calculate the step to select every nth file
    step = max(1, round(len(all_files) / num_files_to_copy))

    # print(step)

    # # Select every nth file
    filtered_files = all_files[::step]
    # print('\n'.join(filtered_files))
    # print(len(filtered_files))

    # Copy the filtered files to the destination directory with progress bar
    for file_name in tqdm(filtered_files, desc="Copying files", unit="file"):
        full_file_name = os.path.join(source_dir, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, dest_dir)

    print(f"Copied {len(filtered_files)} files to {dest_dir}")


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Copy files based on a sequence range or a percentage of total files.")
    parser.add_argument('source_dir', type=str, help="Path to the source directory")
    parser.add_argument('dest_dir', type=str, help="Path to the destination directory")
    parser.add_argument('--prefix', type=str, help="File prefix to filter by (e.g., 'seq')")
    parser.add_argument('--lower-limit', type=int, help="Lower limit of the sequence range")
    parser.add_argument('--upper-limit', type=int, help="Upper limit of the sequence range")
    parser.add_argument('--percentage', type=float, help="Percentage of files to copy")
    parser.add_argument('--create-dest', action='store_true', help="Create destination directory if it doesn't exist")

    # Parse the command line arguments
    args = parser.parse_args()

    # Determine which function to call based on provided arguments
    if args.percentage is not None:
        copy_files_within_percentage(args.source_dir, args.dest_dir, args.percentage, args.create_dest)
    elif args.prefix is not None and args.lower_limit is not None and args.upper_limit is not None:
        copy_files_within_range(args.source_dir, args.dest_dir, args.prefix, args.lower_limit, args.upper_limit,
                                args.create_dest)
    else:
        print(
            "Error: You must specify either a percentage or a sequence range (with prefix, lower limit, and upper limit).")


if __name__ == "__main__":
    main()
