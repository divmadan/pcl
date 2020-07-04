from context import scripts
import scripts.parse as parse

import pytest


unsaved_files = (("test_parse.cpp", "void function() {;}"),)

tu = parse.clang.TranslationUnit.from_source(filename="test_parse.cpp", unsaved_files=unsaved_files)
