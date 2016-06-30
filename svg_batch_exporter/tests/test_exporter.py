#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from PIL import Image
import unittest
from svg_batch_exporter import _build_svg_filenames, _get_script_path, _get_inkscape_path, export_svg

SRC_DIR = _get_script_path() + os.sep + "src"
OUT_DIR = _get_script_path() + os.sep + "output"
RULES_DIR = _get_script_path() + os.sep + "rules"

class TestExporter(unittest.TestCase):
    def test__build_svg_filenames(self):
        '''Building SVG file list from the source directory'''
        file_names = [ "icecream_sandwich", "ink", "gauge" ]
        self.assertSequenceEqual(_build_svg_filenames(SRC_DIR), file_names)

    def test__get_inkscape_path(self):
        '''Checking default Inkscape installation'''
        path = _get_inkscape_path()
        self.assertIsNotNone(path)

    def test_export_svg_rules_full(self):
        '''Checking image size with full rules'''
        param = [
        ["gauge.gif", [300, 300]],
        ["icecream_sandwich.png", [158, 133]],
        ["ink.jpg", [500, 449]]
        ]
        export_svg(SRC_DIR, OUT_DIR + os.sep + "rules_full", RULES_DIR + os.sep + "rules_full.json")
        for im in param:
            self.assertImageSameSize(OUT_DIR + os.sep + "rules_full" + os.sep + im[0], im[1])

    def test_export_svg_rules_partial_1(self):
        '''Checking image size with partial rules including _globalrule_'''
        param = [
        ["gauge.jpg", [300, 300]],
        ["icecream_sandwich.jpg", [300, 300]],
        ["ink.gif", [500, 449]]
        ]
        export_svg(SRC_DIR, OUT_DIR + os.sep + "rules_partial_1", RULES_DIR + os.sep + "rules_partial.json")
        for im in param:
            self.assertImageSameSize(OUT_DIR + os.sep + "rules_partial_1" + os.sep + im[0], im[1])

    def test_export_svg_rules_partial_2(self):
        '''Checking image size with partial rules including programmatic rules'''
        param = [
        ["gauge.bmp", [400, 400]],
        ["icecream_sandwich.bmp", [400, 400]],
        ["ink.gif", [500, 449]]
        ]
        export_svg(SRC_DIR, OUT_DIR + os.sep + "rules_partial_2", RULES_DIR + os.sep + "rules_partial.json", "bmp", [400,400])
        for im in param:
            self.assertImageSameSize(OUT_DIR + os.sep + "rules_partial_2" + os.sep + im[0], im[1])

    def test_export_svg_rules_none(self):
        '''Checking image size with no rules'''
        param = [
        ["gauge.gif", [400, 400]],
        ["icecream_sandwich.gif", [400, 400]],
        ["ink.gif", [400, 400]]
        ]
        export_svg(SRC_DIR, OUT_DIR + os.sep + "rules_none", None, "gif", [400,400])
        for im in param:
            self.assertImageSameSize(OUT_DIR + os.sep + "rules_none" + os.sep + im[0], im[1])

    def assertImageSameSize(self, img_path, size):
        '''
        Do not use it with pdf, ps, eps formats as Pillow does not support it.
        Though eps is supported, Inkscape does not have an option to export with fixed width, height
        '''
        with Image.open(img_path) as image:
            im_size = list(image.size)
        self.assertSequenceEqual(im_size, size)

if __name__ == "__main__":
    unittest.main()
