#!/usr/bin/env python3

from context import scripts
import scripts.parse as parse
import scripts.generate as generate
import scripts.utils as utils

import yaml
import os

from argparse import ArgumentParser


"""
mode:
  1: make a compilation database for use
  2: use an existing compilation database
  3: use a list of filepaths

root_path: 
  path (mode 1)
  None (rest)
"""


def parse_arguments():
    parser = ArgumentParser(description="Pybind11 bindings")
    parser.add_argument("--config", help="Path to config (yaml)", required=True)
    return parser.parse_args()


class bind:
    def __init__(self, config: dict):
        for setting_config in config.values():
            self.mode = setting_config.get("mode", None)
            self.root_path = setting_config.get("root_path", None)
            self.filelist = setting_config.get("filelist", None)
            self.compilation_database_path = setting_config.get(
                "compilation_database_path", None
            )
            self.compilation_commands = setting_config.get("compilation_commands", None)
            self.json_output_path = setting_config.get("json_output_path", None)

    def bind_code(self):
        if self.mode == 1:
            raise Exception("Under development")
        elif self.mode == 2:
            raise Exception("Under development")
        elif self.mode == 3:
            for file in self.filelist:
                if not os.path.exists(file):
                    raise Exception(f"Incorrect filepath in configuration: {file}")
                else:
                    parsed_info = parse.parse_file(
                        source=file,
                        compilation_commands=self.compilation_commands,
                        compilation_database_path=self.compilation_database_path,
                    )

                # Output path for dumping the parsed info into a json file
                output_filepath = utils.get_output_path(
                    source=file,
                    output_dir=utils.join_path(self.json_output_path, "json"),
                    split_from="pcl",
                    extension=".json",
                )

                # Dump the parsed info at output path
                utils.dump_json(filepath=output_filepath, info=parsed_info)

    def check_config(self) -> Exception:
        if self.mode not in (1, 2, 3):
            raise Exception(f"Invalid mode in configuration: {self.mode}")


def main():
    args = parse_arguments()
    with open(args.config) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

        bind_object = bind(config)
        bind_object.check_config()
        bind_object.bind_code()


if __name__ == "__main__":
    main()
