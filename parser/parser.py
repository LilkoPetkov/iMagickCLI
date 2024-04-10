import os
import argparse

from colors.colors import c, fg, bg


parser = argparse.ArgumentParser(
    description=f"{fg.orange}{c.bold}Image processing CLI{c.reset}",
    prog=f"{fg.green}{c.bold}{os.path.basename(__file__)}{c.reset}",
    usage=f"{fg.green}{c.bold}main.py [-h] [-v]{c.reset}",
)

subparsers = parser.add_subparsers(
    title=f"{fg.orange}commands{c.reset}",
    help="",
    metavar=""
)

    ## Convert
convert_parser = subparsers.add_parser(
    "convert", 
    help="convert images from one format to another",
    usage=f"{fg.lightgreen}{c.bold}inputFile outputFile --extension=STR [--width=INT] [--height=INT]{c.reset}"
)

    ## Convert all
convert_all_parser = subparsers.add_parser(
    "convert_dir", 
    help="convert all images in provided directory",
    usage=f"{fg.lightgreen}{c.bold}PathToDirectory --extension=STR --all [--width=INT] [--height=INT] [--exceptions=STR] [--log]{c.reset}"
)

    ## Delete
delete_all_parser = subparsers.add_parser(
    "delete",
    help="delete all created images if image_convert.log exists",
    usage=f"{fg.lightgreen}{c.bold}[--pathToLog/-ptl=STR]{c.reset}",
)

    ## Encipher
encypher_parser = subparsers.add_parser(
    "encipher",
    help="encypher image with a pass phrase",
    usage=f"{fg.lightgreen}{c.bold}inputFile outputFile -passphrase/-pass=STR{c.reset}"
)

    ## Decipher
decypher_parser = subparsers.add_parser(
    "decipher",
    help="decyper image with pass phrase file (.txt)",
    usage=f"{fg.lightgreen}{c.bold}inputFile --pass_file/-pf=STR [--rm_pass/-rmp]{c.reset}"
)
