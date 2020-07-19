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
    assert len(parsed_info["members"]) == 0


def test_translation_unit(tmp_path):
    file_contents = ""
    parsed_info = get_parsed_info(tmp_path=tmp_path, file_contents=file_contents)

    assert parsed_info["kind"] == "TRANSLATION_UNIT"


def test_namespace(tmp_path):
    file_contents = "namespace Anamespace {}"
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
    file_contents = "struct AStruct{}; struct BStruct: public AStruct{};"
    parsed_info = get_parsed_info(tmp_path=tmp_path, file_contents=file_contents)

    child_struct_decl = parsed_info["members"][1]
    cxx_base_specifier = child_struct_decl["members"][0]

    assert cxx_base_specifier["kind"] == "CXX_BASE_SPECIFIER"
    assert cxx_base_specifier["access_specifier"] == "PUBLIC"


def test_cxx_method(tmp_path):
    file_contents = "struct AStruct{void Afunction();}"
    parsed_info = get_parsed_info(tmp_path=tmp_path, file_contents=file_contents)

    struct_decl = parsed_info["members"][0]
    cxx_method = struct_decl["members"][0]

    assert cxx_method["kind"] == "CXX_METHOD"
    assert cxx_method["result_type"] == "void"


def test_var_decl(tmp_path):
    file_contents = "int Aint=1;"
    parsed_info = get_parsed_info(tmp_path=tmp_path, file_contents=file_contents)

    var_decl = parsed_info["members"][0]

    assert var_decl["kind"] == "VAR_DECL"
    assert var_decl["element_type"] == "Int"


def test_type_ref(tmp_path):
    file_contents = "struct Astruct{int Aint;} \n void Afunction(Astruct& Aint);"
    parsed_info = get_parsed_info(tmp_path=tmp_path, file_contents=file_contents)

    function_decl = parsed_info["members"][1]
    l_value_ref = function_decl["members"][0]
    type_ref = l_value_ref["members"][0]

    assert type_ref["kind"] == "TYPE_REF"


def test_constructor(tmp_path):
    file_contents = "struct Astruct{Astruct(){}};"
    parsed_info = get_parsed_info(tmp_path=tmp_path, file_contents=file_contents)

    struct_decl = parsed_info["members"][0]
    constructor = struct_decl["members"][0]

    assert constructor["kind"] == "CONSTRUCTOR"
    assert constructor["access_specifier"] == "PUBLIC"


def test_parm_decl(tmp_path):
    file_contents = "struct Astruct{ Astruct(int Aint) {} };"
    parsed_info = get_parsed_info(tmp_path=tmp_path, file_contents=file_contents)

    struct_decl = parsed_info["members"][0]
    constructor = struct_decl["members"][0]
    parm_decl = constructor["members"][0]

    assert parm_decl["kind"] == "PARM_DECL"
    assert parm_decl["element_type"] == "Int"


def test_call_expr(tmp_path):
    file_contents = "struct Astruct{ Astruct (): Astruct() {} };"
    parsed_info = get_parsed_info(tmp_path=tmp_path, file_contents=file_contents)

    struct_decl = parsed_info["members"][0]
    constructor = struct_decl["members"][0]
    call_expr = constructor["members"][1]

    assert call_expr["kind"] == "CALL_EXPR"


def test_unexposed_expr(tmp_path):
    file_contents = "struct Astruct{ int Aint; \n\
        Astruct (int Bint): Aint(Bint) {} };"
    parsed_info = get_parsed_info(tmp_path=tmp_path, file_contents=file_contents)

    struct_decl = parsed_info["members"][0]
    constructor = struct_decl["members"][1]
    unexposed_expr = constructor["members"][2]

    assert unexposed_expr["kind"] == "UNEXPOSED_EXPR"


# @TODO: Not sure how to reproduce. Maybe later.
# def test_member_ref_expr(tmp_path):


def test_decl_ref_expr(tmp_path):
    file_contents = "struct Astruct{ int Aint; \n\
        Astruct (int Bint): Aint(Bint) {} };"
    parsed_info = get_parsed_info(tmp_path=tmp_path, file_contents=file_contents)

    struct_decl = parsed_info["members"][0]
    constructor = struct_decl["members"][1]
    unexposed_expr = constructor["members"][2]
    decl_ref_expr = unexposed_expr["members"][0]

    assert decl_ref_expr["kind"] == "DECL_REF_EXPR"


def test_field_decl(tmp_path):
    file_contents = "struct Astruct{ int Aint; };"
    parsed_info = get_parsed_info(tmp_path=tmp_path, file_contents=file_contents)

    struct_decl = parsed_info["members"][0]
    field_decl = struct_decl["members"][0]

    assert field_decl["kind"] == "FIELD_DECL"
    assert field_decl["element_type"] == "Int"


def test_member_ref(tmp_path):
    file_contents = "struct Astruct{ int Aint; \n\
        Astruct (int Bint): Aint(Bint) {} };"
    parsed_info = get_parsed_info(tmp_path=tmp_path, file_contents=file_contents)

    struct_decl = parsed_info["members"][0]
    constructor = struct_decl["members"][1]
    member_ref = constructor["members"][1]

    assert member_ref["kind"] == "MEMBER_REF"
    assert member_ref["element_type"] == "Int"


def test_class_template(tmp_path):
    file_contents = "template<typename N> struct Astruct {};"
    parsed_info = get_parsed_info(tmp_path=tmp_path, file_contents=file_contents)

    class_template = parsed_info["members"][0]

    assert class_template["kind"] == "CLASS_TEMPLATE"


def test_template_non_type_parameter(tmp_path):
    file_contents = "template<int N> struct Astruct {};"
    parsed_info = get_parsed_info(tmp_path=tmp_path, file_contents=file_contents)

    class_template = parsed_info["members"][0]
    template_non_type_parameter = class_template["members"][0]

    assert template_non_type_parameter["kind"] == "TEMPLATE_NON_TYPE_PARAMETER"
    assert template_non_type_parameter["element_type"] == "Int"


def test_function_template(tmp_path):
    file_contents = "template<int N> void Afunction() {}"
    parsed_info = get_parsed_info(tmp_path=tmp_path, file_contents=file_contents)

    function_template = parsed_info["members"][0]

    assert function_template["kind"] == "FUNCTION_TEMPLATE"
    assert function_template["result_type"] == "void"
