# Using SWIG to generate C++ bindings
This document contains information about SWIG as a useful tool for development of C++ bindings.

Table of Contents:
- [Using SWIG to generate C++ bindings](#using-swig-to-generate-c-bindings)
	- [Introduction](#introduction)
	- [Features](#features)
		- [Target Languages supported as of latest version (swig-4.0.0)](#target-languages-supported-as-of-latest-version-swig-400)
		- [ISO C++](#iso-c)
		- [Preprocessing](#preprocessing)
		- [Doxygen documentation](#doxygen-documentation)
		- [Customization features](#customization-features)
	- [Compilation Requirements](#compilation-requirements)
	- [Executive Summary](#executive-summary)
	- [References](#references)

## Introduction
- SWIG is a software development tool that connects programs written in C/C++ with high-level programming languages.
- SWIG is typically used to parse C/C++ interfaces and generate the 'glue code' required for the above target languages to call into the C/C++ code.
- SWIG can also export its parse tree in the form of XML.
- SWIG is a free software and the code that SWIG generates is compatible with both commercial and non-commercial projects.
- One of it's many use cases is the construction of scripting language extension modules. SWIG can be used to turn common C/C++ libraries into components for use in popular scripting languages.
- SWIG is in use in many open source projects. These can be a useful reference for seeing how SWIG is used in real projects. For full list: [reference][4]
- A simple tutorial: [reference][7]

***

## Features

### Target Languages supported as of latest version (swig-4.0.0)
- C#
- D
- Go
- Guile
- Java including Android
- Javascript
- Lua
- MzScheme/Racket
- OCaml
- Octave
- Perl
- PHP
- Python
- R
- Ruby
- Scilab
- Tcl
- Support for Allegrocl, CFFI, Chicken, CLISP, Modula3, S-EXP, UFFI and Pike was removed in swig-4.0.0, was available in the previous versions.

### ISO C++
SWIG provides wrapping support for ISO C++98 to C++17. Features include:

- All C++ datatypes.
- References
- Pointers to members
- Classes
- Inheritance and multiple inheritance
- Overloaded functions and methods (using dynamic dispatch)
- Overloaded operators
- Static members
- Namespaces (including using declarations, aliases, nesting, etc.)
- Templates
- Nested classes
- Member templates
- Template specialization and partial specialization
- Smart pointers
- C++ library support for strings and the STL
- The majority of the newer C++11 to C++17 standard features.
- **Note**: SWIG currently requires instantiation of all template classes. [reference and more info][5] (Although I will try using 'lazy' method, see if it works)

### Preprocessing
SWIG provides a full C preprocessor with the following features:

- Macro expansion.
- Automatic wrapping of #define statements as constants (when applicable).
- Support for C99 (variadic macro expansion).

### Doxygen documentation
Doxygen documentation comments in C++ comments are parsed and converted into equivalent Java and Python documentation comments.

### Customization features
SWIG provides control over most aspects of wrapper generation. Most of these customization options are fully integrated into the C++ type system--making it easy to apply customizations across inheritance hierarchies, template instantiations, and more. For more info: [reference][6]

***

## Compilation Requirements
- SWIG is supported on Unix, Microsoft Windows and Macintosh.
- SWIG is implemented in C and C++ and is distributed in source form.
- It requires a working C++ compiler (e.g., g++) to build SWIG. It doesn't depend upon any of the supported scripting languages for its own compilation.
- Although SWIG is partly written in C++, a compiler is not required to use it--it works fine with both ISO C and C++.

***

## Executive Summary
- SWIG is an interface compiler. It works by taking the declarations found in C/C++ header files and uses them to generate the wrapper code that scripting languages need to access the underlying C/C++ code.
- In addition, SWIG provides a variety of customization features that let us tailor the wrapping process to suit your application.
- Some relevant points:
	- ISO C/C++ syntax:
		- SWIG parses ISO C++ that has been extended with a number of special directives.
		- As a result, interfaces are usually built by grabbing a header file and tweaking it a little bit.
		- This particular approach is especially useful when the underlying C/C++ program undergoes frequent modification.
	- SWIG does not define a protocol nor is it a component framework:
		- SWIG does not define mechanisms or enforce rules regarding the way in which software components are supposed to interact with each other. Nor is it a specialized runtime library or alternative scripting language API.
		- SWIG is merely a code generator that provides the glue necessary to hook C/C++ to other languages.
	- Designed to work with existing C/C++ code:
		- For the most part, it encourages to keep a clean separation between C/C++ and its scripting interface.
- For more uses: [reference][3]

***

## References

- http://www.swig.org/
- http://www.swig.org/compat.html
- http://www.swig.org/exec.html
- http://www.swig.org/projects.html
- http://www.swig.org/Doc4.0/SWIGPlus.html#SWIGPlus_nn30
- http://www.swig.org/tutorial.html

***

[1]: http://www.swig.org/	"SWIG Homepage"
[2]: http://www.swig.org/compat.html	"SWIG Compatibility"
[3]: http://www.swig.org/exec.html	"SWIG Summary"
[4]: http://www.swig.org/projects.html	"SWIG Projects"
[5]: http://www.swig.org/Doc4.0/SWIGPlus.html#SWIGPlus_nn30	"SWIG Templating"
[6]: http://www.swig.org/compare.html	"SWIG Features"
[7]: http://www.swig.org/tutorial.html	"SWIG Tutorial"

