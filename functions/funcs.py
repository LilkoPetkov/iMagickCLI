import os
import subprocess
import uuid
import re

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
        print(f"{fg.green}Success{c.reset}: Image {file} successfully converted to {extension}")
        print(f"{fg.green}Success{c.reset}: New file: {output_file}.{extension}")
    else:
        print(f"{c.bold}{fg.red}{result.stderr}{c.reset}")


# Convert all images in dir
def convert_all(path: str, extension: str, exceptions: List[str], all: bool = False, log: bool = False, width: int = 0, height: int = 0) -> None:
    if not Path(path).exists():
        parser.exit(1, message=f"{c.bold}{fg.red}Error{c.reset}: the target directory doesn't exist\n")
    if not all:
        parser.exit(1, message=f"{c.bold}{fg.red}Error{c.reset}: please pass --all to confirm\n")

    if log:
        result = subprocess.run("find . -name image_convert.log -exec realpath {} \\;", shell=True, capture_output=True, text=True)
        print(f"{bg.green}Success{c.reset}: Image convert log created")

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
        print(f"{c.bold}{fg.red}{c.reset}: image_convert.log might be missing, use -h for help")
    else:
        print(f"{fg.green}Success{c.reset}: Converted images removed")


# Encipher image
def encipher(image: str, passphrase: Union[int, str]) -> None:
    if not os.path.isfile(image):
        parser.exit(1, message=f"{c.bold}{fg.red}Error{c.reset}: {image} does not exist or is not an image\n")

    try:
        with open("passphrase.txt", 'x') as f:
            f.write(f"{passphrase}")
    except FileExistsError:
        # if file exists, create it with a UUID
        with open(f"passphrase{str(uuid.uuid4())}.txt", 'x') as f:
            f.write(f"{passphrase}")

    command = f"magick {image} -encipher {f.name} {image}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.stderr:
        print(f"{c.bold}{fg.red}Error{c.reset}: {result.stderr}")
        subprocess.run(f"rm -f {f.name}", shell=True)
    else:
        print(f"{fg.green}Success{c.reset}: {image} enciphered with passphrase: {fg.pink}{passphrase}{c.reset}")
        print(f"{fg.green}Succcess{c.reset}: {f.name} created")


# Decipher images
def decipher(image: str, pass_file: str, rm_pass: bool = False) -> None:
    # regex check
    pattern: str = r"(?P<txtFile>[A-z0-9]+\.txt$)"
    try: 
        file_name = re.search(pattern, pass_file).group("txtFile")
    except AttributeError as ae:
        parser.exit(1, message=f"{c.bold}{fg.red}Error{c.reset}: passphrase file has to be .txt\n")
    
    # regular file checks
    if not os.path.isfile(image):
        parser.exit(1, message=f"{c.bold}{fg.red}Error{c.reset}: {image} does not exist or is not an image\n")
    if not os.path.isfile(pass_file):
        parser.exit(1, message=f"{c.bold}{fg.red}Error{c.reset}: {pass_file} does not exist or is not an .txt file\n")

    # command processing
    command = f"magick {image} -decipher {pass_file} {image}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.stderr:
        print(f"{c.bold}{fg.red}Error{c.reset}: {result.stderr}")
    else:
        print(f"{fg.green}Success{c.reset}: {image} deciphered with passphrase file: {fg.pink}{pass_file}{c.reset}")

    if rm_pass:
        subprocess.run(f"rm -f {pass_file}")
