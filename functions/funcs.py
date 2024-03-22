import os
import subprocess

from datetime import datetime, timezone
from pathlib import Path
from parser.parser import parser
from typing import Union, List
from colors.colors import c, fg, bg


# Convert single image
def convert(file: str, extension: str, output_file: str, width: int = 0, height: int = 0) -> None:
    command = f"magick {file} {output_file}.{extension}" if width == 0 and height == 0 else\
    f"magick {file} -resize {width}x{height} {output_file}.{extension}"

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"{bg.green}Image {file} successfully converted to {extension}{c.reset}")
        print(f"{bg.green}New file: {output_file}.{extension}{c.reset}")
    else:
        print(f"{c.bold}{fg.red}{result.stderr}{c.reset}")


# Convert all images in dir
def convert_all(path: str, extension: str, exceptions: List[str], all: bool = False, log: bool = False, width: int = 0, height: int = 0) -> None:
    if not Path(path).exists():
        parser.exit(1, message=f"{c.bold}{fg.red}Error: the target directory doesn't exist{c.reset}")
    if not all:
        parser.exit(1, message=f"{c.bold}{fg.red}Error: please pass --all to confirm{c.reset}")

    if log:
        result = subprocess.run("find . -name image_convert.log -exec realpath {} \\;", shell=True, capture_output=True, text=True)
        print(f"{bg.green}Image log created{c.reset}")

    for file in os.listdir(path):
        print(file)
        if os.path.isfile(file) and file not in exceptions:
    
            command = f"magick {file} {file}.{extension}" if width == 0 and height == 0 else\
            f"magick {file} -resize {width}x{height} {file}.{extension}"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
            if result.returncode == 0:
                if log:
                    with open("image_convert.log", "a") as f:
                        f.write(f"[{str(datetime.now(timezone.utc))}] {file} {file}.{extension}\n")
            else:
                if log:
                    with open("image_convert.log", "a") as f:
                        f.write(f"[{str(datetime.now(timezone.utc))}] {result.stderr}\n")


# Delete all created files from log
def delete(pathToLog: Union[None, str]) -> None:
    remove_files = f"for image in \"$(cat {pathToLog} | awk '{{print $4}}')\"; do rm -f $image; done"
    result = subprocess.run(remove_files, shell=True, capture_output=True)

    if result.stderr:
        print(f"{c.bold}{fg.red}Error: image_convert.log might be missing, use -h for help{c.reset}")
    else:
        print(f"{bg.green}Converted images removed{c.reset}")
