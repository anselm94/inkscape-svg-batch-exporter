#!/usr/bin/env python3

# The MIT License (MIT)
#
# Copyright (c) 2016 Merbin J Anselm
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import subprocess
import os
import sys
import argparse
import json
import tempfile

# Export formats supported by Inkscape
INKSCAPE_FORMATS = [
    "png",
    "pdf",  # Cannot be exported with custom width, height
    "ps",  # Cannot be exported with custom width, height
    "eps"  # Cannot be exported with custom width, height
]

# Export formats supported by Pillow library
PIL_FORMATS = [
    "jpeg",
    "jpg",
    "bmp",
    "gif",
    "im",
    "pcx",
    "tiff"
]


def _report_error(exception, error_desc):
    """
    Helper for reporting error

    Args:
        exception (Exception): A valid exception
        error_desc (str): A brief error description
    """
    print(error_desc)
    sys.exit(1)


def _report_status(status):
    """
    Helper for reporting status

    Args:
        status (str): Brief status description
    """
    print(status)


def _get_script_path():
    """
    Helper for getting script path

    Returns:
        Path to the script
    """
    return os.getcwd()


def _run_command(cmd):
    """
    Helper for running commands

    Args:
        cmd (str): A list containing command parameters
    """
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def _parse_arguments():
    """
    Helper for parsing arguments when running in command-line

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(description="Inkscape powered rule-based SVG batch exporter to multiple image formats",
                                     epilog="See https://github.com/anselm94/inkscape-svg-batch-exporter for more help")
    parser.add_argument('srcdir', help="Path to directory containing SVG files")
    parser.add_argument('outdir', help="Path to directory to output image files")
    parser.add_argument('--rules', help="JSON rules file")
    parser.add_argument('--size', help="\'width,size\' (without space) Size of exported images in pixels. E.g 50,50 \
                                                        If --rules is supplied, files not mentioned in the JSON file will be \
                                                        exported with SIZE")
    parser.add_argument('--format', help="Image format to be exported. Formats supported: png, jpeg, jpg, pdf, bmp, \
                                                        gif, ps, eps, im, pcx, tiff")
    parser.add_argument('--drawing_only', help="\'yes\' or \'y\' -> Drawing area alone should be exported. \
                                                        \'no\' or \'n\' -> Whole page should be exported")
    parser.add_argument(
        '--inkscape', help="Inkscape custom executable path. Leave it if default Inkscape installation is to be used")
    return parser.parse_args()


def _get_inkscape_path():
    """
    Helper for getting Inkscape executable path for current OS

    Returns:
        Path to Inkscape executable
    Raises:
        FileNotFoundError: If no Inkscape executable is found
    """
    if os.name == "nt":
        path = "C:\\Program Files\\Inkscape\\inkscape.exe"
        if not os.path.isfile(path):
            path = "C:\\Program Files (x86)\\Inkscape\\inkscape.exe"
            if not os.path.isfile(path):
                _report_error(FileNotFoundError,
                              "Inkscape installation not found!")
    else:
        path = ("/Applications/Inkscape.app" +
                "/Contents/Resources/bin/inkscape-bin")
        if not os.path.isfile(path):
            path = "/usr/bin/inkscape"
            if not os.path.isfile(path):
                _report_error(FileNotFoundError,
                              "No Inkscape installation found!")
    _report_status("Inkscape installation found ... " + path)
    return path


def _build_svg_filenames(dirpath):
    """
    Helper for building a list of SVG file names in a directory

    Args:
        filepath (str): Directory path containing SVG files
    Returns:
        List of SVG file names (without .svg extension)
    Raises:
        FileNotFoundError: If no SVG file is found
    """
    svg_file_names = []
    for file_name in os.listdir(dirpath):
        if file_name.endswith(".svg"):
            name = file_name.split('.svg')[0]
            svg_file_names.append(name)
    no_of_svg_files = len(svg_file_names)
    if no_of_svg_files == 0:
        _report_error(FileNotFoundError, "No SVG file found in " + dirpath)
    _report_status(str(no_of_svg_files) + " SVG files found")
    return svg_file_names


def _build_data_from_json(json_filename):
    """
    Helper for building a dictionary from JSON file

    Args:
        json_filename (str): JSON file path
    Returns:
        Dictionary containing JSON data
    Raises:
        FileNotFoundError: If file path is not valid
        json.JSONDecodeError: If the file is not a valid JSON format
    """
    if _resolve_path(json_filename):
        with open(json_filename) as json_file:
            try:
                json_data = json.load(json_file)
                return json_data
            except json.JSONDecodeError:
                _report_error(json.JSONDecodeError, json_filename +
                              " is not a valid JSON file format!")
    else:
        _report_error(FileNotFoundError, json_filename +
                      " is not a valid file!")


def _resolve_dir(dirpath):
    """
    Helper to resolve if a directory exists

    Args:
        dirpath (str): Directory path
    Returns:
        True if it is a valid directory else False
    Raises:
        FileNotFoundError: If directory path is not valid
    """
    if not os.path.isdir(dirpath):
        _report_error(FileNotFoundError, dirpath +
                      " is not a valid directory!")
        return False
    return True


def _resolve_path(filepath):
    """
    Helper to resolve if a file exists

    Args:
        filepath (str): File path
    Returns:
        True if it is a valid file else False
    Raises:
        FileNotFoundError: If file path is not valid
    """
    if not os.path.isfile(filepath):
        _report_error(FileNotFoundError, filepath +
                      " is not a valid file path!")
        return False
    return True


def _is_inkscape_format(in_form):
    """
    Helper to check if a particular format is supported by Inkscape exporter

    Args:
        in_form (str): Input format to check
    Returns:
        True if a particular format is supported else False
    """
    for frm in INKSCAPE_FORMATS:
        if in_form.lower() == frm.lower():
            return True
    return False


def _is_pillow_format(in_form):
    """
    Helper to check if a particular format is supported by Pillow library exporter

    Args:
        in_form (str): Input format to check
    Returns:
        True if a particular format is supported else False
    """
    for frm in PIL_FORMATS:
        if in_form.lower() == frm.lower():
            return True
    return False


def _convert_via_inkscape(inkscape_path, src_svg_path, out_img_path, file_format, size=None, drawing_only=True):
    """
    Helper to export single SVG file to another image format

    Args:
        inkscape_path (str): Inkscape executable path
        src_svg_path (str): File path to source SVG file
        out_img_path (str): File path to output image file
        file_format (str): Image format to be exported
        size (list): List containing width and height. e.g. [50, 50]
        drawing_only (bool): True if only drawing is to be exported. False if entire page is to be exported
    Raises:
        ImportError: If Pillow library isn't installed
        TypeError: If the image format is not supported
    """
    # Building command
    cmd = [inkscape_path, "-f", src_svg_path]
    if drawing_only:
        cmd = cmd + ["--export-area-drawing"]
    else:
        cmd = cmd + ["--export-area-page"]
    if _is_inkscape_format(file_format):
        if file_format == "png":
            cmd = cmd + ["--export-png=" + out_img_path]
            if size:
                cmd = cmd + ["-w", str(size[0]), "-h", str(size[1])]
        elif file_format == "pdf":
            cmd = cmd + ["--export-pdf=" + out_img_path]
        elif file_format == "ps":
            cmd = cmd + ["--export-ps=" + out_img_path]
        elif file_format == "eps":
            cmd = cmd + ["--export-eps=" + out_img_path]
        _run_command(cmd)
    elif _is_pillow_format(file_format):
        # Export SVG to PNG using Inkscape and then convert the PNG to
        # another image format using Pillow (fork of PIL) library
        # Writing to a temperory PNG file
        tempf_path = tempfile.gettempdir() + os.sep + "mJaAjM.png"
        cmd = cmd + ["--export-png=" + tempf_path]
        if size:
            cmd = cmd + ["-w", str(size[0]), "-h", str(size[1])]
        _run_command(cmd)
        # Convert temperory PNG file to the target image format
        try:
            from PIL import Image
            with open(tempf_path, 'rb') as image_file:
                with Image.open(image_file) as im:
                    im.save(out_img_path)
        except ImportError:
            _report_error(ImportError, "Python3 Pillow library not found!")
        finally:
            # Cleaning the temperory PNG file
            os.remove(tempf_path)
    else:
        _report_error(TypeError("Unsupported file format to export: " +
                                file_format), "Unsupported file format to export: " + file_format)


def export_svg(src_dir, out_dir, json_rules_file=None, file_format=None, size=None, drawing_only=None, inkscape_path="default"):
    """
    Batch exports SVG files from a directory to a destination directory

    Args:
        src_svg_path (str): Path to directory containing source SVG file
        out_img_path (str): Path to directory to output the exported image files
        json_rules_file (str): File path to JSON Rules file containing rules
        file_format (str): Image format to be exported.
        size (list): List containing width and height. e.g. [50, 50]
        drawing_only (bool): True if only drawing is to be exported. False if entire page is to be exported
        inkscape_path (str): \'default\' if default Inkscape installation is to be used else a custom executable path
    """
    _resolve_dir(src_dir) and _resolve_dir(out_dir)
    if json_rules_file:
        _resolve_path(json_rules_file)
    if inkscape_path == "default":
        inkscape_path = _get_inkscape_path()
    else:
        _resolve_path(inkscape_path)
    rule_data = []
    global_param = {}
    # Building Default parameter
    def_param = {
        "size": None,
        "format": "png",
        "drawing_only": True
    }
    supplied_param = {}

    def curated_param(data):
        if "size" in data:
            if data["size"] == "default":
                data["size"] = None
        return data
    svg_files = _build_svg_filenames(src_dir)
    if json_rules_file is not None:
        rule_data = _build_data_from_json(json_rules_file)

    # Building Global parameter
    if "_globalrule_" in rule_data:
        global_param = curated_param(rule_data["_globalrule_"])

    # Building Supplied parameter
    if size is not None:
        supplied_param["size"] = size
    if file_format is not None:
        supplied_param["format"] = file_format
    if drawing_only is not None:
        supplied_param["drawing_only"] = drawing_only

    for svg_file in svg_files:
        local_param = {}
        final_param = {}
        params = ["size", "format", "drawing_only"]
        if svg_file in rule_data:
            local_param = curated_param(rule_data[svg_file])
        param_blocks = [local_param, supplied_param, global_param, def_param]
        for param in params:
            for block in param_blocks:
                if param in block:
                    final_param[param] = block[param]
                    break
        _convert_via_inkscape(inkscape_path, src_dir + os.path.sep + svg_file + ".svg",
                              out_dir + os.path.sep + svg_file +
                              "." + final_param["format"],
                              final_param["format"], final_param["size"],
                              final_param["drawing_only"])
        _report_status("Saved " + svg_file + "." + final_param["format"])
    _report_status("Done")

if __name__ == "__main__":
    args = _parse_arguments()
    image_size = None
    f_drawing_only = True
    f_format = args.format
    if args.drawing_only:
        draw = args.drawing_only.lower()
        if draw == "y" or draw == "yes":
            f_drawing_only = True
        elif draw == "n" or draw == "no":
            f_drawing_only = False
        else:
            print(
                "Wrong argument supplied for --drawing_only parameter! \nUse --help or -h to get help")
            sys.exit()
    if args.size:
        image_size = list(args.size.split(","))
        if len(image_size) != 2:
            print(
                "Wrong argument supplied for --size parameter! \nUse --help or -h to get help")
            sys.exit()
    if args.inkscape:
        inkscape = args.inkscape
    else:
        inkscape = "default"
    export_svg(args.srcdir, args.outdir, json_rules_file=args.rules, file_format=f_format,
               size=image_size, drawing_only=f_drawing_only, inkscape_path=inkscape)
