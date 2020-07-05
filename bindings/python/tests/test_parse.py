# from context import scripts
import scripts.parse as parse

import clang.cindex as clang


def test_node_in_this_file_true():
    def recursive_call(cursor):
        for child in cursor.get_children():
            assert parse.node_in_this_file(child, tu.spelling) == True
            recursive_call(cursor=child)

    unsaved_files = (("file.cpp", "void function() {}"),)
    tu = clang.TranslationUnit.from_source(filename="file.cpp", unsaved_files=unsaved_files)
    recursive_call(cursor=tu.cursor)


def test_node_in_this_file_false_none():
    def recursive_call(cursor):
        for child in cursor.get_children():
            if child.location.file:
                assert parse.node_in_this_file(child, tu.spelling) == False
            else:
                assert parse.node_in_this_file(child, tu.spelling) == None
            recursive_call(cursor=child)

    unsaved_files = (("file.cpp", "#include<algorithm>"),)
    tu = clang.TranslationUnit.from_source(filename="file.cpp", unsaved_files=unsaved_files)
    recursive_call(cursor=tu.cursor)

