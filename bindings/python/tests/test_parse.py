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


def test_types(tmp_path):
    file_contents = ""
    parsed_info = get_parsed_info(tmp_path=tmp_path, file_contents=file_contents)

    assert type(parsed_info) is dict
    assert type(parsed_info["members"]) is list


def test_translation_unit(tmp_path):
    file_contents = ""
    parsed_info = get_parsed_info(tmp_path=tmp_path, file_contents=file_contents)

    assert parsed_info["kind"] == "TRANSLATION_UNIT"


def test_namespace(tmp_path):
    file_contents = "namespace Anamespace {  }// namespace Anamespace"
    parsed_info = get_parsed_info(tmp_path=tmp_path, file_contents=file_contents)

    namespace = parsed_info["members"][0]

    assert namespace["kind"] == "NAMESPACE"


def test_namespace_ref(tmp_path):
    file_contents = "#include<ostream> \n std::ostream Aostream;"
    parsed_info = get_parsed_info(tmp_path=tmp_path, file_contents=file_contents)

    namespace_ref = parsed_info["members"][0]["members"][0]

    assert namespace_ref["kind"] == "NAMESPACE_REF"


def test_struct_decl(tmp_path):
    file_contents = "struct AStruct{};"
    parsed_info = get_parsed_info(tmp_path=tmp_path, file_contents=file_contents)

    struct_decl = parsed_info["members"][0]

    assert struct_decl["kind"] == "STRUCT_DECL"


def test_cxx_base_specifier(tmp_path):
    file_contents = "struct _AStruct{}; struct AStruct: public _AStruct{};"
    parsed_info = get_parsed_info(tmp_path=tmp_path, file_contents=file_contents)

    child_struct_decl = parsed_info["members"][1]
    cxx_base_specifier = child_struct_decl["members"][0]

    assert cxx_base_specifier["kind"] == "CXX_BASE_SPECIFIER"
    assert cxx_base_specifier["access_specifier"] == "PUBLIC"


def test_cxx_method(tmp_path):
    file_contents = "struct AStruct{void Afunction();}"
    parsed_info = get_parsed_info(tmp_path=tmp_path, file_contents=file_contents)

    cxx_method = parsed_info["members"][0]["members"][0]

    assert cxx_method["kind"] == "CXX_METHOD"
    assert cxx_method["result_type"] == "void"


def test_var_decl(tmp_path):
    file_contents = "int Aint=1;"
    parsed_info = get_parsed_info(tmp_path=tmp_path, file_contents=file_contents)

    var_decl = parsed_info["members"][0]

    assert var_decl["kind"] == "VAR_DECL"


def test_type_ref(tmp_path):
    file_contents = "struct Astruct{int Aint;} \n void Afunction(Astruct& Aint);"
    parsed_info = get_parsed_info(tmp_path=tmp_path, file_contents=file_contents)

    function_decl = parsed_info["members"][1]
    l_value_ref = function_decl["members"][0]
    type_ref = l_value_ref["members"][0]

    assert type_ref["kind"] == "TYPE_REF"

