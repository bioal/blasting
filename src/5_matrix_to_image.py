#!/usr/bin/env python3
import argparse
from classes.ImageManager import ImageManager

parser = argparse.ArgumentParser(description='Make image file from matrix file.')
parser.add_argument('matrix', help='Matrix in tsv format')
parser.add_argument('-c', '--color', default='ff0000', help='Matrix color')
parser.add_argument('-hp', '--horizontal_pixels', default='5', help='Horizontal pixels of one dot')
parser.add_argument('-vp', '--vertical_pixels', default='1', help='Vertical pixels of one dot')
parser.add_argument('-o', '--output', required=True, help='Output file path')

args = parser.parse_args()

manager = ImageManager(args.matrix, args.color, args.horizontal_pixels, args.vertical_pixels)
manager.export(args.output)
