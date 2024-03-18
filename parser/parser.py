import os
import argparse

from colors.colors import c, fg, bg


parser = argparse.ArgumentParser(
    description=f"{fg.orange}{c.bold}Image processing CLI{c.reset}",
    prog=f"{fg.green}{c.bold}{os.path.basename(__file__)}{c.reset}",
)

subparsers = parser.add_subparsers(
    title="commands",
    help="valid command options"
)


    ## Convert
convert_parser = subparsers.add_parser(
    "convert", 
    help="convert images from one format to another",
    usage=f"{fg.lightgreen}{c.bold}inputFile outputFile --extension [--resize]{c.reset}"
)
    ## Upgrade
convert_all_parser = subparsers.add_parser(
    "convert_dir", 
    help="convert all images in provided directory",
    usage=f"{fg.lightgreen}{c.bold}PathToDirectory --extension --all [--resize] [--log]{c.reset}"
)

    ## Delete
delete_all_parser = subparsers.add_parser(
    "delete",
    help="delete all created images if image_convert.log exists",
    usage=f"{fg.lightgreen}{c.bold}[--pathToLog/-ptl=PATH]{c.reset}"
)