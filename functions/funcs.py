import os
import subprocess
import uuid

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
        print(f"{fg.green}Success: Image {file} successfully converted to {extension}{c.reset}")
        print(f"{fg.green}Success: New file: {output_file}.{extension}{c.reset}")
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
        print(f"{bg.green}Success: Image convert log created{c.reset}")

    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)) and file not in exceptions:
    
            command = f"magick {os.path.join(path, file)} {os.path.join(path, file)}.{extension}" if width == 0 and height == 0 else\
            f"magick {os.path.join(path, file)} -resize {width}x{height} {os.path.join(path, file)}.{extension}"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
            if result.returncode == 0:
                if log:
                    with open("image_convert.log", "a") as f:
                        f.write(f"[{str(datetime.now(timezone.utc))}] {os.path.join(path, file)} {os.path.join(path, file)}.{extension}\n")
            else:
                if log:
                    with open("image_convert.log", "a") as f:
                        f.write(f"[{str(datetime.now(timezone.utc))}] {os.path.join(path, file)} {os.path.join(path, file)}.{extension} [{result.stderr}]")


# Delete all created files from log
def delete(pathToLog: Union[None, str]) -> None:
    remove_files = f"for image in \"$(cat {pathToLog} | awk '{{print $4}}')\"; do rm -f $image; done"
    result = subprocess.run(remove_files, shell=True, capture_output=True)

    if result.stderr:
        print(f"{c.bold}{fg.red}Error: image_convert.log might be missing, use -h for help{c.reset}")
    else:
        print(f"{fg.green}Success: Converted images removed{c.reset}")


# Encipher image
def encipher(image: str, passphrase: Union[int, str]) -> None:
    try:
        with open("passphrase.txt", 'x') as f:
            f.write(f"{passphrase}")
    except FileExistsError:
        # if file exists, create it with a UUID
        with open(f"passphrase{str(uuid.uuid4())}.txt", 'x') as f:
            f.write(f"{passphrase}")


    if not os.path.isfile(i):
        parser.exit(1, message=f"{c.bold}{fg.red}Error: {image} does not exist or is not an image{c.reset}")

    command = f"magick {image} -encipher {f.name} {image}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.stderr:
        print(f"{c.bold}{fg.red}Error: {image} could not be converted{c.reset}")
        subprocess.run(f"rm -f {f.name}", shell=True)
    else:
        print(f"{fg.green}Success: {image} converted with passphrase{c.reset}")
        print(f"{fg.green}Succcess: {f.name} created{c.reset}")
