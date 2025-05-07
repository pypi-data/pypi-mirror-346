Python Source Translator
========================

Module to translate Python source code into other programming languages

It supports source conversion of most Python features, but the output code might
need some minor tweaks to run in the target language.


Examples
--------

Simple usage:

```py
from source_translator import SourceCode
from source_translator.langs import cpp

code = SourceCode("""
def my_function(a: int, b: int) -> int:
    '''
    This function does something
    '''
    if a > b:
        # Sum them
        return a + b
    else:
        return a
""")

print(cpp.CppTranslator().convert(code))
```

```cpp
/**
 * This function does something
 */
int my_function(int a, int b)
{
    if ( a > b )
    {
        // Sum them
        return a + b;
    }
    else
    {
        return a;
    }
}
```

Indentation styling:

```py
from source_translator import SourceCode
from source_translator.langs import cpp
from source_translator.c_like import KandRStyle

code = SourceCode("""
def my_function(a: int, b: int) -> int:
    '''
    This function does something
    '''
    if a > b:
        # Sum them
        return a + b
    else:
        return a
""")

print(cpp.CppTranslator(KandRStyle(spaces=8)).convert(code))
```

```cpp
/**
 * This function does something
 */
int my_function(int a, int b) {
        if ( a > b ) {
                // Sum them
                return a + b;
        } else {
                return a;
        }
}
```

Converting a Python function:

```py
import inspect
from source_translator import SourceCode
from source_translator.langs import cpp


def my_function(a: int, b: int) -> int:
    '''
    This function does something
    '''
    if a > b:
        # Sum them
        return a + b
    else:
        return a


code = SourceCode(inspect.getsource(my_function))

print(cpp.CppTranslator().convert(code))
```

Supported Languages
-------------------

C++

```py
from source_translator import SourceCode
from source_translator.langs import cpp

code = SourceCode("""
def my_function(a: int, b: int) -> int:
    '''
    This function does something
    '''
    if a > b:
        # Sum them
        return a + b
    else:
        return a
""")

print(cpp.CppTranslator().convert(code))
```

```cpp
/**
 * This function does something
 */
int my_function(int a, int b)
{
    if ( a > b )
    {
        // Sum them
        return a + b;
    }
    else
    {
        return a;
    }
}
```

TypeScript

```py
from source_translator import SourceCode
from source_translator.langs import ts

code = SourceCode("""
def my_function(a: int, b: int) -> int:
    '''
    This function does something
    '''
    if a > b:
        # Sum them
        return a + b
    else:
        return a
""")

print(ts.TypeScriptTranslator().convert(code))
```

```ts
/**
 * This function does something
 */
function myFunction(a: number, b: number): number {
    if ( a > b ) {
        // Sum them
        return a + b;
    } else {
        return a;
    }
}
```
JavaScript

```py
from source_translator import SourceCode
from source_translator.langs import ts

code = SourceCode("""
def my_function(a: int, b: int) -> int:
    '''
    This function does something
    '''
    if a > b:
        # Sum them
        return a + b
    else:
        return a
""")

print(ts.TypeScriptTranslator(False).convert(code))
```

```js
/**
 * This function does something
 */
function myFunction(a, b) {
    if ( a > b ) {
        // Sum them
        return a + b;
    } else {
        return a;
    }
}
```


PHP

```php
/**
 * This function does something
 */
function my_function(int $a, int $b): int
{
    if ( $a > $b )
    {
        // Sum them
        return $a + $b;
    }
    else
    {
        return $a;
    }
}
```

License
-------

Copyright (C) 2023-2024 Mattia Basaglia

GPLv3+ (see COPYING)


Development
-----------

### Requirements

```bash
pip install twine build coverage
```

### Running Tests

```bash
./test.sh [testcase]
```

### Building Packages

```bash
python3 -m build --sdist
python3 -m build --wheel
twine upload dist/*
```
