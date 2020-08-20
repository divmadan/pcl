import os
import json


def get_filelist(root, whitelist):
    """
    1. Generates a file list dictionary of the structure:

    {
        pcl_folder: {
            sub_folder: {
                "impls": [list_of_impl_files]
                "headers": [list_of_header_files]
            }
            ...
        }
        ...
    }

    """
    pcl = {}

    for folder in whitelist:
        folder_path = os.path.join(root, folder)
        if os.path.exists(folder_path):
            impl_files = []
            header_files = []

            # walk the folder to get filenames
            for root, _, files in os.walk(folder_path):
                for file in files:
                    # filter for implementation files
                    if file.split(".")[-1] == "hpp":
                        impl_files.append(os.path.join(root, file))
                    # filter for header files
                    if file.split(".")[-1] == "h":
                        header_files.append(os.path.join(root, file))
                    # filter for cpp files
                    if file.split(".")[-1] == "cpp":
                        header_files.append(os.path.join(root, file))
                    # add a filter for any other file type if desired
                    _

            # add list to pcl dict
            pcl[folder] = {"impls": impl_files, "headers": header_files}

        else:
            raise Exception(f"{folder_path} doesn't exist")

    return pcl


def generate_compile_commmands(
    file_list, directory_name, compiler_path, compiler_arguments
):
    """
    2. Generating compilation commands database from the dictionary:

    [
        {
            "directory": "build_directory",
            "command": "path_to_compiler [compiler_argument_1, compiler_argument_2, ...] filename",
            "file": "filename",
        }
        ...
    ]

    """
    compile_commands = []

    for contents in file_list.values():
        for files in contents.values():
            for file in files:
                item = {
                    "directory": directory_name,
                    "command": f"{compiler_path} {compiler_arguments} {file}",
                    "file": file,
                }
                compile_commands.append(item)

    return compile_commands


def main():
    pcl_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # folders = os.listdir(root) # if file list needs to be generated for all folders
    whitelist = ["common"]
    pcl = get_filelist(pcl_root, whitelist)

    # with open("pcl_files.json", "w") as f:
    #     json.dump(pcl, f, indent=2)

    directory_name = os.path.dirname(os.path.abspath(__file__))
    compiler_path = "/usr/bin/clang++"
    compiler_arguments = "-std=c++14 -I/usr/include/pcl-1.8"
    compile_commmands = generate_compile_commmands(
        pcl, directory_name, compiler_path, compiler_arguments
    )

    with open("compile_commands.json", "w") as f:
        json.dump(compile_commmands, f, indent=2)


if __name__ == "__main__":
    main()
