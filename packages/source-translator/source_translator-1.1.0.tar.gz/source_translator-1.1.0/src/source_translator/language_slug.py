from .langs import cpp, ts, php
from .python_source import AstTranslator, IndentationStyle
from .naming import snake_to_lower_camel, keep_same
from .c_like import AllmanStyle, KandRStyle, WhitesmithsStyle, GnuStyle

langs = {
    "c++": cpp.CppTranslator,
    "cpp": cpp.CppTranslator,
    "cxx": cpp.CppTranslator,
    "ts": ts.TypeScriptTranslator,
    "php": php.PhpTranslator,
    "js": lambda: ts.TypeScriptTranslator(False)
}

naming = {
    "snake": keep_same,
    "camel": snake_to_lower_camel,
}

styles = {
    "allman": AllmanStyle,
    "a": AllmanStyle,
    "k&r": KandRStyle,
    "kr": KandRStyle,
    "whitesmiths": WhitesmithsStyle,
    "gnu": GnuStyle,
}


def slug_to_lang(slug: str) -> AstTranslator:
    tokens: list = slug.split(":")
    translator: AstTranslator = langs[tokens.pop(0)]()

    for token in tokens:
        if token.isdigit():
            translator.indent_style.spaces = int(token)
        elif token in naming:
            translator.naming_style = naming[token]
        elif token in styles:
            style: IndentationStyle = styles[token]()
            style.spaces = translator.indent_style.spaces
            translator.indent_style = style

    return translator
