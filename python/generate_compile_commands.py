import os
import json


def get_filelist(root_folder, allowlist, blocklist):
    """
    1. Generates a file list dictionary of the structure:

    {
        root_folder: {
            sub_folder: {
                "impls": [list_of_impl_files]
                "headers": [list_of_header_files]
            }
            ...
        }
        ...
    }

    """
    files_structure = {}

    # list of all blocked files
    blocklist_files = []
    for folder in blocklist:
        folder_path = os.path.join(root_folder, folder)
        if os.path.exists(folder_path):
            # walk the folder to get filenames
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # populate blocklist_files
                    blocklist_files.append(file_path)
        else:
            raise Exception(f"{folder_path} doesn't exist")

    for folder in allowlist:
        folder_path = os.path.join(root_folder, folder)
        if os.path.exists(folder_path):
            impl_files = []
            header_files = []

            # walk the folder to get filenames
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)

                    if file_path in blocklist_files:
                        continue

                    # filter for implementation files
                    if file.endswith(".hpp"):
                        impl_files.append(file_path)
                    # filter for header files
                    if file.endswith(".h"):
                        header_files.append(file_path)
                    # filter for cpp files
                    if file.endswith(".cpp"):
                        header_files.append(file_path)
                    # add a filter for any other file type if desired
                    _

            # add list to files_structure dict
            files_structure[folder] = {"impls": impl_files, "headers": header_files}

        else:
            raise Exception(f"{folder_path} doesn't exist")

    return files_structure


def generate_compile_commmands(
    files_structure, directory_name, compiler_path, compiler_arguments
):
    """
    2. Generating compilation commands database from the files structure:

    [
        {
            "directory": "build_directory",
            "command": "path_to_compiler [compiler_argument_1, compiler_argument_2, ...] filename",
            "file": "filename",
        }
        ...
    ]

    """

    return [
        dict(
            directory=directory_name,
            command=f"{compiler_path} {compiler_arguments} {file}",
            file=file,
        )
        for contents in files_structure.values()
        for files in contents.values()
        for file in files
    ]


def main():
    root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # folders = os.listdir(root) # if file list needs to be generated for all folders
    allowlist = ["common"]
    blocklist = []
    files_structure = get_filelist(root_folder, allowlist, blocklist)

    # with open("pcl_files.json", "w") as f:
    #     json.dump(files_structure, f, indent=2)

    directory_name = os.path.dirname(os.path.abspath(__file__))
    compiler_path = "/usr/bin/clang++"
    compiler_arguments = "-std=c++14 -I/usr/include/pcl-1.8"
    compile_commmands = generate_compile_commmands(
        files_structure, directory_name, compiler_path, compiler_arguments
    )

    with open("compile_commands.json", "w") as f:
        json.dump(compile_commmands, f, indent=2)


if __name__ == "__main__":
    main()
