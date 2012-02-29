# Copyright 2011 OpenStack, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse

from dbaasclient import client


class DBaaSClientArgumentParser(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):
        super(DBaaSClientArgumentParser, self).__init__(*args, **kwargs)

    def error(self, message):
        """error(message: string)

        Prints a usage message incorporating the message to stderr and
        exits.
        """
        self.print_usage(sys.stderr)
        choose_from = ' (choose from'
        self.exit(2, "error: %s\nTry `%s' for more information.\n" %
                     (message.split(choose_from)[0],
                      self.prog.replace(" ", " help ", 1)))


class DBaaSShell(object):

    def get_base_parser(self):
        parser = DBaaSClientArgumentParser(
            prog='dbaas',
            description=__doc__.strip(),
            epilog='See "dbaas help COMMAND" '\
                   'for help on a specific command.',
            add_help=False,
        )

        # Global arguments
        parser.add_argument('-h', '--help',
            action='help',
            help=argparse.SUPPRESS,
        )

        parser.add_argument('--debug',
            default=False,
            action='store_true',
            help="Print debugging output")

        parser.add_argument('--url',
            default=utils.env('NOVA_URL'),
            help=argparse.SUPPRESS)

        parser.add_argument('--version',
            default=utils.env('NOVA_VERSION', default=DEFAULT_NOVA_VERSION),
            help='Accepts 1.1, defaults to env[NOVA_VERSION].')

