# add validation for the parser, use type=pathlib.Path stuff
import argparse
import sys
import pathlib
import tifffile
import sys
import os
import json
import numpy as np


def cli(arguments):
    parser = argparse.ArgumentParser(
        description="Split or merge tiffs using reshape split", prog="reSplit"
    )
    subparser = parser.add_subparsers()
    parser.set_defaults(splitter=None)
    split_subparser = subparser.add_parser("split", help="split the image")
    split_subparser.set_defaults(splitter=True)
    merge_subparser = subparser.add_parser("merge", help="merge the split images")
    split_subparser.add_argument("reshape", type=pathlib.Path, help="ReShAPE JSON file")
    split_subparser.add_argument(
        "split", type=pathlib.Path, help="source image (TIFF format)"
    )
    merge_subparser.add_argument("reshape", type=pathlib.Path, help="ReShAPE JSON file")
    merge_subparser.add_argument(
        "source", type=pathlib.Path, help="directory of split images to merge"
    )
    merge_subparser.set_defaults(splitter=False)
    args = parser.parse_args(arguments)
    # if no args are passed print usage
    if args.splitter == None:
        parser.print_help()
        parser.print_usage()
        sys.exit(1)
    return args


def split_main(args):
    with open(args.reshape, "r") as f:
        stitch_guide = json.load(f)
    fp = tifffile.imread(args.source)
    base_path, ext = os.path.splitext(args.source)
    for tile in stitch_guide["tiles"]:
        n, _ = os.path.splitext(tile["name"])
        new_suffix = n.split("_")[-1]
        out_fname = f"{base_path}_{new_suffix}{ext}"
        tifffile.imwrite(
            out_fname,
            fp[tile["y"] : tile["y"] + tile["h"], tile["x"] : tile["x"] + tile["w"]],
        )
        print(f"[INFO] writing: {out_fname}")


def merge_main(args):
    # TODO merge the corrected parts back together.
    with open(args.reshape, "r") as f:
        stitch_guide = json.load(f)
    blank_array = np.zeros(
        (stitch_guide["height"], stitch_guide["width"]), dtype="uint8"
    )
    assert os.path.exists(args.source), f"Path '{args.source}' does not exist"
    # just use the pixel order in the image itself!
    for tile in stitch_guide["tiles"]:
        target = os.path.join(args.source, tile["name"])
        tile_arr = tifffile.imread(target)
        blank_array[
            tile["y"] : tile["y"] + tile["h"], tile["x"] : tile["x"] + tile["w"]
        ] = tile_arr
    im_title = f"{os.path.basename(stitch_guide['source'])}.tif"
    tifffile.imwrite(im_title, blank_array)


def main(arg=sys.argv[1:]):
    args = cli(arg)
    if args.splitter:
        split_main(args)
    else:
        merge_main(args)


if __name__ == "__main__":
    main()
