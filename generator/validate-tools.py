#!/usr/bin/python
#
# Copyright 2019 Copyright (c) 2019 SAP SE or an SAP affiliate company. All rights reserved. This file is licensed under the Apache Software License, v. 2 except as noted otherwise in the LICENSE file.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys


def main(argv):
    pass


if __name__ == '__main__':
    main(sys.argv)
#!/usr/bin/env python3

import argparse
import subprocess
import shlex

from lib import dockerfile, commands, utils

def validate_tools(commands_list):
    errors = []
    for command in commands_list:
        if isinstance(command, commands.Curl):
            for tool in command.get_tools():
                try:
                    subprocess.run(
                        ["curl", "-sLf", shlex.quote(commands.Curl.get_download_location(tool))],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        check=True)
                except subprocess.CalledProcessError as e:
                    errors.append('Command "{}" failed with exit code {}'.format(e.cmd, e.returncode))
    return errors

parser = argparse.ArgumentParser()
parser.add_argument("--dockerfile-config", dest="dockerfile_config", required=True, help="yaml file which lists the tools to be tested")
parser.add_argument("--additional-configs", nargs='+', action="append", dest="additional_configs", default=[], required=False, help="Additional tools to test.")
args = parser.parse_args()

dockerfile_config = utils.parse_dockerfile_configs(args.dockerfile_config, args.additional_configs)
commands_list = [commands.create_command(command_config) for command_config in dockerfile_config]

validation_errors = validate_tools(commands_list)
if len(validation_errors) == 0:
    print("Validation of tools was successful")
    exit(0)
else:
    print("Validation of tools failed with the following errors:\n{}".format('\n'.join(validation_errors)))
    exit(1)