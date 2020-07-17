from context import scripts
import scripts.parse as parse

import json
import os

import clang.cindex as clang


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


def get_parsed_info(tmp_path, file_contents):
    source_path = tmp_path / "file.hpp"
    source_path.write_bytes(str(file_contents).encode())

    parsed_info = parse.parse_file(
        source=str(source_path),
        compilation_database_path=create_compilation_database(
            tmp_path=tmp_path, filepath=source_path
        ),
    )

    return parsed_info
    assert type(parsed_info) is dict
    assert type(parsed_info["members"]) is list


def test_struct_decl(tmp_path):
    source_path = tmp_path / "file.hpp"
    source_path.write_text("struct AStruct{};")

    parsed_info = parse.parse_file(
        source=str(source_path),
        compilation_database_path=create_compilation_database(
            tmp_path=tmp_path, filepath=source_path
        ),
    )

    struct_decl = parsed_info["members"][0]

    assert struct_decl["kind"] == "STRUCT_DECL"


def test_cxx_base_specifier(tmp_path):
    source_path = tmp_path / "file.hpp"
    source_path.write_text("struct _AStruct{}; struct AStruct: public _AStruct{};")

    parsed_info = parse.parse_file(
        source=str(source_path),
        compilation_database_path=create_compilation_database(
            tmp_path=tmp_path, filepath=source_path
        ),
    )

    child_struct_decl = parsed_info["members"][1]
    cxx_base_specifier = child_struct_decl["members"][0]

    assert cxx_base_specifier["kind"] == "CXX_BASE_SPECIFIER"
    assert cxx_base_specifier["access_specifier"] == "PUBLIC"

