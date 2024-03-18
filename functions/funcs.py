import os
import subprocess

from datetime import datetime, timezone
from pathlib import Path
from parser.parser import parser
from typing import Union
from colors.colors import c, fg, bg


# Convert single image
def convert(file: str, extension: str, output_file: str, log: bool = False, resize: int = 0) -> None:
    command = f"magick {file} {output_file}.{extension}" if resize == 0 else f"magick {file} -resize {resize}% {output_file}.{extension}"

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"{bg.green}Image {file} successfully converted to {extension}{c.reset}")
        print(f"{bg.green}New file: {output_file}.{extension}{c.reset}")
    else:
        print(f"{c.bold}{fg.red}{result.stderr}{c.reset}")


# Convert all images in dir
def convert_all(path: str, extension: str, all: bool = False, log: bool = False, resize: int = 0) -> None:
    if not Path(path).exists():
        parser.exit(1, message="the target directory doesn't exist")
    if not all:
        parser.exit(1, message="please pass --all to confirm")

    if log:
        result = subprocess.run("find . -name image_convert.log -exec realpath {} \\;", shell=True, capture_output=True, text=True)
        print(f"{bg.lightgrey}Image log created: {result}{c.reset}")

    for file in os.listdir(path):
        if os.path.isfile(file):
    
            command = f"magick {file} {file}.{extension}" if resize == 0 else f"magick {file} -resize {resize}% {file}.{extension}"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
            if result.returncode == 0:
                if log:
                    with open("image_convert.log", "a") as f:
                        f.write(f"{str(datetime.now(timezone.utc))} {file} {file}.{extension}\n")
            else:
                if log:
                    with open("image_convert.log", "a") as f:
                        f.write(f"{str(datetime.now(timezone.utc))} {result.stderr}\n")


# Delete all created files from log
def delete(pathToLog: Union[None, str]) -> None:
    remove_files = f"for image in \"$(cat {pathToLog} | awk '{{print $4}}')\"; do rm -f $image; done"
    result = subprocess.run(remove_files, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"{bg.green}Converted images removed{c.reset}")
    else:
        print(f"{c.bold}{fg.red}{result.stderr}{c.reset}")
