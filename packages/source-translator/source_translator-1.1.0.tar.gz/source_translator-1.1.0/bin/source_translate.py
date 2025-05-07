#!/usr/bin/env python3

import sys
import pathlib
import argparse

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent / "src"))

from source_translator import SourceCode, c_like
from source_translator.langs import cpp, ts, php
from source_translator.naming import snake_to_lower_camel
from source_translator import language_slug

translators = {
    "cpp": cpp.CppTranslator(),
    "ts": ts.TypeScriptTranslator(),
    "js": ts.TypeScriptTranslator(False),
    "php": php.PhpTranslator(),
}
translators["c++"] = translators["cpp"]


styles = {
    "allman": c_like.AllmanStyle(),
    "k&r": c_like.KandRStyle(),
    "whitesmiths": c_like.WhitesmithsStyle(),
    "gnu": c_like.GnuStyle()
}


parser = argparse.ArgumentParser()
parser.add_argument("file", type=pathlib.Path)
parser.add_argument("--language", "-x")
parser.add_argument("--style", "-s", choices=language_slug.styles.keys())
parser.add_argument("--indent-width", "-w", type=int, default=None)
parser.add_argument("--camel", action="store_true")
args = parser.parse_args()


if __name__ == "__main__":
    with open(args.file) as f:
        source = SourceCode(f.read())

    translator = language_slug.slug_to_lang(args.language)

    if args.style:
        translator.indent_style = language_slug.styles[args.style]

    if args.indent_width:
        translator.indent_style.spaces = args.indent_width

    if args.camel:
        translator.naming_style = snake_to_lower_camel

    output = translator.convert(source)
    print(output)
