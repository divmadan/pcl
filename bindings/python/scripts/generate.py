import json
import argparse
import sys
import os


class kind:

    KIND = None
    NAME = None
    MEMBERS = None
    DEPTH = None
    state_stack = []
    kind_functions = {
        "TRANSLATION_UNIT": [],
        "NAMESPACE": [handle_NAMESPACE_0, handle_NAMESPACE_1],
        "STRUCT_DECL": [handle_STRUCT_DECL_0, handle_STRUCT_DECL_1],
        "CXX_BASE_SPECIFIER": [],
        "CXX_METHOD": [handle_CXX_METHOD],
        "CONSTRUCTOR": handle_CONSTRUCTOR,
        "VAR_DECL": handle_VAR_DECL,
        "PARM_DECL": handle_PARM_DECL,
        "TYPE_REF": handle_TYPE_REF,
        "CALL_EXPR": handle_CALL_EXPR,
    }
    linelist = []

    def handle_kind(self, item):
        KIND = item["kind"]
        NAME = item["name"]
        MEMBERS = item["members"]
        DEPTH = item["depth"]

        self.state_stack.append({"kind": KIND, "name": NAME, "depth": DEPTH})

        if self.kind_functions[KIND][0]:
            self.kind_functions[KIND][0](item)

        for item in MEMBERS:
            self.handle_kind(item)

        if self.kind_functions[KIND][1]:
            self.kind_functions[KIND][1](item)

        self.state_stack.pop()

    def handle_NAMESPACE_0(self, item):
        self.linelist.append(f"namespace {self.NAME}" + "{")

    def handle_NAMESPACE_1(self, item):
        self.linelist.append("}")

    def handle_STRUCT_DECL_0(self, item):
        MEMBERS = item["members"]
        for item in MEMBERS:
            if item["kind"]=="CXX_BASE_SPECIFIER":
                CXX_BASE_SPECIFIER = item["name"]
                self.linelist.append(f'py::class_<{self.NAME, CXX_BASE_SPECIFIER}>(m, "{self.NAME}")')
                return
        self.linelist.append(f'py::class_<{self.NAME}>(m, "{self.NAME}")')
        

    def handle_STRUCT_DECL_1(self, item):
        self.linelist.append(";")


    def handle_CXX_METHOD(item):
        prev_depth_node = self.get_prev_depth_node()
        if prev_depth_node:
            # @TODO
            METHOD_OF = prev_depth_node["name"]
            self.linelist.append(f'.def("{self.NAME}", &{METHOD_OF}::CXX_METHOD)')
        print(CXX_METHOD, "not in struct")

    def get_prev_depth_node(self):
        for prev_item in reversed(self.state_stack):
            if prev_item["depth"] == self.DEPTH - 1:
                return prev_item
        return


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
            module_linelist[i] = "".join(
                (f"PYBIND11_MODULE({module_name}, m)", "{", module_linelist[i])
            )
            break
    for line in module_linelist:
        linelist.append(line)
    linelist.append("}")
    return linelist


def handle_CALL_EXPR(item):
    pass


def handle_NAMESPACE_REF(item):
    pass


def handle_TYPE_REF(item):
    global TYPE_REF_LIST
    TYPE_REF = item["name"]
    if TYPE_REF_LIST[-1][0]:
        TYPE_REF_LIST[-1][1] = TYPE_REF
    else:
        TYPE_REF_LIST.append([None, TYPE_REF])


def handle_PARM_DECL(item):
    for sub_item in item["members"]:
        kind_functions[sub_item["kind"]](sub_item)


def handle_CONSTRUCTOR(item):
    global CONSTRUCTOR
    global TYPE_REF_LIST
    CONSTRUCTOR = item["name"]
    for sub_item in item["members"]:
        kind_functions[sub_item["kind"]](sub_item)
    parameters_kind = ",".join(params for params in TYPE_REF_LIST)
    module_linelist.append(f".def(py::init<{parameters_kind}>())")
    TYPE_REF_LIST = []
    CONSTRUCTOR = None


def handle_operator(item):
    pass
    # if STRUCT_DECL:
    #     module_linelist.append(f'.def(py::self {item["name"]} py::self)')


def handle_VAR_DECL(item):
    pass


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

        for item in header_info:
            kind_functions[item["kind"]](item)

        lines_to_write = handle_final(filename="pcl/point_types.h", module_name="pcl")
        output_filepath = get_output_path(
            os.path.realpath(source), output_dir=f"pybind11/{os.path.dirname(__file__)}"
        )
        write_to_cpp(filename=output_filepath, linelist=lines_to_write)


if __name__ == "__main__":
    main()