from context import scripts
import scripts.parse as parse

import json
import os

import clang.cindex as clang

# def test_node_in_this_file_true():
#     def recursive_call(cursor):
#         for child in cursor.get_children():
#             assert parse.node_in_this_file(child, tu.spelling) == True
#             recursive_call(cursor=child)

#     unsaved_files = (("file.cpp", "void function() {}"),)
#     tu = clang.TranslationUnit.from_source(filename="file.cpp", unsaved_files=unsaved_files)
#     recursive_call(cursor=tu.cursor)


# def test_node_in_this_file_false():
#     def recursive_call(cursor):
#         for child in cursor.get_children():
#             assert parse.node_in_this_file(child, tu.spelling) == False
#             recursive_call(cursor=child)

#     unsaved_files = (("file.cpp", "#include<algorithm>"),)
#     tu = clang.TranslationUnit.from_source(filename="file.cpp", unsaved_files=unsaved_files)
#     recursive_call(cursor=tu.cursor)


# def test_create_file(tmpdir):
#     p = tmpdir.mkdir("input").join("hello.txt")
#     p.write("content")


def create_compilation_database(tmp_path, filepath):
    input = tmp_path / "compile_commands.json"
    x = [
        {
            "directory": f"{tmp_path}",
            "command": f"/usr/bin/clang++ -std=c++14 {filepath}",
            "file": f"{filepath}",
        }
    ]
    input.write_bytes(str(x).encode())
    tmp_path = str(tmp_path)
    return tmp_path


def test_type(tmp_path):
    source_path = tmp_path / "file.hpp"
    source_path.write_text("struct AStruct{};")

    parsed_info = parse.parse_file(
        source=str(source_path),
        compilation_database_path=create_compilation_database(
            tmp_path=tmp_path, filepath=source_path
        ),
    )

    assert type(parsed_info) is dict
    assert type(parsed_info["members"]) is list


def test_struct(tmp_path):
    source_path = tmp_path / "file.hpp"
    source_path.write_text("struct AStruct{};")

    parsed_info = parse.parse_file(
        source=str(source_path),
        compilation_database_path=create_compilation_database(
            tmp_path=tmp_path, filepath=source_path
        ),
    )

    assert parsed_info["members"][0]["kind"] == "STRUCT_DECL"

