#!/usr/bin/env python3

import argparse
import os

import PIL.Image


def get_ansi_color_code(r, g, b):
    if r == g and g == b:
        if r < 8:
            return 16
        if r > 248:
            return 231
        return round(((r - 8) / 247) * 24) + 232
    return 16 + (36 * round(r / 255 * 5)) + (6 * round(g / 255 * 5)) + round(b / 255 * 5)


def get_color(r, g, b):
    return "\x1b[48;5;{}m \x1b[0m".format(int(get_ansi_color_code(r, g, b)))


def show_image(img_path, rows, max_columns, aspect):
    img = PIL.Image.open(img_path)

    columns = min(max_columns, int((aspect * rows * img.width) / img.height))
    img: PIL.Image.Image = img.resize((columns, rows), PIL.Image.ANTIALIAS)

    for row in range(rows):
        for col in range(columns):
            pix = img.getpixel((col, row))
            print(get_color(pix[0], pix[1], pix[2]), sep='', end='')
        print()


def _main():
    _arg_parser = argparse.ArgumentParser(description="console image view utility")
    _arg_parser.add_argument('image', help="image file")
    _arg_parser.add_argument('--rows', '-R', help='rows to use', type=int)
    _arg_parser.add_argument('--aspect', '-A', help='console "pixel" aspect h/w', type=float, default=2.8)
    _args = _arg_parser.parse_args()
    _columns, _rows = os.get_terminal_size()
    if not _args.rows:
        _rows = int(_columns / _args.aspect)
    else:
        _rows = _args.rows
    show_image(_args.image, _rows, _columns, _args.aspect)


if __name__ == '__main__':
    _main()
