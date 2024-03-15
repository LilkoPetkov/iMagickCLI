from parser.parser import parser, convert_parser, convert_all_parser
from typing import Union
from functions.funcs import convert, convert_all


# Arguments single convert
convert_parser.add_argument(
    "file", 
    type=str,
    help="input file name or relative/absolute path to file",
    metavar="inputFile"
)
convert_parser.add_argument(
    "output_file",
    type=str,
    help="name of output file",
    metavar="outputFile"
)
convert_parser.add_argument(
    "--extension",
    "-e",
    help="file extension of output file",
    required=True,
    type=str,
    metavar=""
)
convert_parser.add_argument(
    "--resize",
    "-re",
    help="resize image by percentage",
    metavar="",
    type=Union[int],
    default=0
)

# convert all pareser
convert_all_parser.add_argument(
    "path",
    help="absolute path to directory",
    metavar="",    
)
convert_all_parser.add_argument(
    "--extension",
    "-e",
    help="file extension of output files",
    required=True,
    type=str,
    metavar=""
)
convert_all_parser.add_argument(
    "--all",
    help="all images in the directory path",
    action="store_true",
    required=True
)
convert_all_parser.add_argument(
    "--resize",
    "-re",
    help="resize image by percentage",
    metavar="",
    type=Union[int],
    default=0
)
convert_all_parser.add_argument(
    "--log",
    help="creates a log for all conversions",
    action="store_true"
)


# set callback functions
convert_parser.set_defaults(func=convert)
convert_all_parser.set_defaults(func=convert_all)

# parse args
args = parser.parse_args()