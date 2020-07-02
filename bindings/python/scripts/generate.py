import json
import argparse
import sys
import os


class bind:
    def __init__(self, root):
        self._state_stack = []
        self.linelist = []
        self._skipped = []
        self.kind_functions = {
            "TRANSLATION_UNIT": [self.skip],
            "NAMESPACE": [self.handle_namespace_0, self.handle_namespace_1],
            "NAMESPACE_REF": [self.skip],
            "STRUCT_DECL": [self.handle_struct_decl_0, self.handle_struct_decl_1],
            "CXX_BASE_SPECIFIER": [self.skip],
            "CXX_METHOD": [self.handle_cxx_method],
            "VAR_DECL": [self.skip],
            "TYPE_REF": [self.skip],
            "CONSTRUCTOR": [self.handle_constructor],
            "PARM_DECL": [self.skip],
            "CALL_EXPR": [self.skip],
            "UNEXPOSED_EXPR": [self.skip],
            "MEMBER_REF_EXPR": [self.skip],
            "DECL_REF_EXPR": [self.skip]
        }

        self.handle_node(root)

    def get_prev_depth_node(self):
        for prev_item in reversed(self._state_stack):
            if prev_item["depth"] == self.depth - 1:
                return prev_item
        return

    def skip(self):
        self._skipped.append({"line": self.item["line"], "column": self.item["line"], "kind": self.kind, "name": self.name})

    def handle_node(self, item):
        self.item = item
        self.kind = self.item["kind"]
        self.name = self.item["name"]
        self.members = self.item["members"]
        self.depth = self.item["depth"]

        self._state_stack.append({"kind": self.kind, "name": self.name, "depth": self.depth})

        self.kind_functions[self.kind][0]()

        for sub_item in self.members:
            self.handle_node(sub_item)

        if len(self.kind_functions[self.kind]) > 1:
            self.kind_functions[self.kind][1]()

        self._state_stack.pop()

    def handle_namespace_0(self):
        self.linelist.append(f"namespace {self.name}" + "{")

    def handle_namespace_1(self):
        self.linelist.append("}")

    def handle_struct_decl_0(self):
        cxx_base_specifier_list = [sub_item["name"] for sub_item in self.members if sub_item["kind"] == "CXX_BASE_SPECIFIER"]
        if cxx_base_specifier_list:
            cxx_base_specifier_list = ",".join(cxx_base_specifier_list)
            self.linelist.append(f'py::class_<{self.name, cxx_base_specifier_list}>(m, "{self.name}")')
        else:
            self.linelist.append(f'py::class_<{self.name}>(m, "{self.name}")')

    def handle_struct_decl_1(self):
        self.linelist.append(";")

    def handle_cxx_method(self):
        prev_depth_node = self.get_prev_depth_node()
        if prev_depth_node:
            method_of = prev_depth_node["name"]
            self.linelist.append(f'.def("{self.name}", &{method_of}::{self.name})')
        else:
            self.linelist.append(f'.def("{self.name}", &{self.name})')

    def handle_constructor(self):
        argument_type_list = []
        parameter_decl_list = []
        for sub_item in self.members:
            if sub_item["kind"] == "PARM_DECL":
                parameter_decl_list.append(sub_item["name"])
                if sub_item["element_type"] == "LValueReference":
                    for sub_sub_item in sub_item["members"]:
                        if sub_sub_item["kind"] == "TYPE_REF":
                            argument_type_list.append(f'&{sub_sub_item["name"]}')
                else:
                    if sub_item["element_type"] in ["Float"]:
                        argument_type_list.append(f'&{sub_item["element_type"].lower()}')
                    else:
                        argument_type_list.append(f'&{sub_item["element_type"]}')
        parameter_decl_list = ",".join([decl + "_a" for decl in parameter_decl_list])
        argument_type_list = ",".join(argument_type_list)
        self.linelist.append(f".def(py::init<{argument_type_list}>(), {parameter_decl_list})")


def read_json(filename):
    with open(filename, "r") as f:
        return json.load(f)


def write_to_cpp(filename, linelist):
    with open(filename, "w") as f:
        for line in linelist:
            f.writelines(line)
            f.writelines("\n")


def handle_final(filename, module_name):
    linelist = []
    linelist.append(f"#include <{filename}>")
    linelist.append("#include <pybind11/pybind11.h>")
    linelist.append("namespace py = pybind11;")
    for i in range(len(module_linelist)):
        if module_linelist[i].startswith("namespace"):
            continue
        else:
            module_linelist[i] = "".join((f"PYBIND11_MODULE({module_name}, m)", "{", module_linelist[i]))
            break
    for line in module_linelist:
        linelist.append(line)
    linelist.append("}")
    return linelist


def get_output_path(source, output_dir):
    x_list = source.split("json/", 1)[-1]
    x_list = x_list.split("/")

    filename = x_list[-1].split(".")[0]
    relative_dir = "/".join(x for x in x_list[:-1])
    dir = os.path.join(output_dir, relative_dir)

    # ensure the new directory exists
    if not os.path.exists(dir):
        os.makedirs(dir)

    return f"{dir}/{filename}.cpp"


def parse_arguments(args):
    parser = argparse.ArgumentParser(description="JSON to pybind11 generation")
    parser.add_argument("files", nargs="+", help="JSON input")
    return parser.parse_args(args)


def main():
    args = parse_arguments(sys.argv[1:])

    for source in args.files:
        header_info = read_json(source)
        if header_info:
            bind_object = bind(header_info[0])
        else:
            raise Exception("Empty json")

        lines_to_write = handle_final(filename="pcl/point_types.h", module_name="pcl")
        output_filepath = get_output_path(os.path.realpath(source), output_dir=f"pybind11/{os.path.dirname(__file__)}")
        write_to_cpp(filename=output_filepath, linelist=lines_to_write)


if __name__ == "__main__":
    main()
