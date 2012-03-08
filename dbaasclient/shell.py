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

    dbaas_parser = argparse.ArgumentParser()
    dbaas_subparsers = dbaas_parser.add_subparsers()

    #list mysql instances
    list_instance_parser = dbaas_subparsers.add_parser('list_instances',
        help='List MySQL instances')
    list_instance_parser.add_argument('--instance_id', action='store',
        required=False, help='MySQL instance_id')
    list_instance_parser.set_defaults(func=dbaas.func_list_instances)

    #create new mysql instance
    create_instance_parser = dbaas_subparsers.add_parser('create_instance',
        help='Create a new MySQL instance')
    create_instance_parser.add_argument('--instance_name', action='store',
        required=True, help='Name for new MySQL instance')
    create_instance_parser.add_argument('--snapshot_id', action='store',
        help='Snapshot to use for MySQL creation')
    create_instance_parser.set_defaults(func=dbaas.func_create_instance)

    #reset mysql password
    reset_password_parser = dbaas_subparsers.add_parser('reset_password',
        help='Reset MySQL password')
    reset_password_parser.add_argument('--instance_id', action='store',
        required=True, help='MySQL instance_id')
    reset_password_parser.add_argument('--instance_password', action='store',
        required=False, help='New MySQL password')
    reset_password_parser.set_defaults(func=dbaas.func_reset_password)

    #restart mysql(instance)
    restart_instance_parser = dbaas_subparsers.add_parser('restart_instance',
        help='Reset MySQL password')
    restart_instance_parser.add_argument('--instance_id', action='store',
        required=True, help='MySQL instance_id')
    restart_instance_parser.add_argument('--restart_type', action='store',
        required=False, help='Restart MySQL [SOFT|HARD]')
    restart_instance_parser.set_defaults(func=dbaas.func_restart_instance)

    #create new mysql snapshot
    create_snapshot_parser = dbaas_subparsers.add_parser('create_snapshot',
        help='Create MySQL snapshot')
    create_snapshot_parser.add_argument('--instance_id', action='store',
        required=True, help='MySQL instance_id')
    create_snapshot_parser.add_argument('--snapshot_name', action='store',
        required=True, help='Name of snapshot')
    create_snapshot_parser.set_defaults(func=dbaas.func_create_snapshot)

    #list snapshots
    list_snapshot_parser = dbaas_subparsers.add_parser('list_snapshots',
        help='List all MySQL snapshots')
    list_snapshot_parser.add_argument('--instance_id', action='store',
        help='MySQL instance_id')
    list_snapshot_parser.add_argument('--snapshot_id', action='store',
        help='Snapshot id')
    list_snapshot_parser.set_defaults(func=dbaas.func_list_snapshot)

    #delete snapshots
    delete_snapshot_parser = dbaas_subparsers.add_parser('delete_snapshot',
        help='Delete a MySQL snapshot')
    delete_snapshot_parser.add_argument('--snapshot_id', action='store',
        required=True, help='MySQL snapshot ID')
    delete_snapshot_parser.set_defaults(func=dbaas.func_delete_snapshot)

    #terminate mysql instance
    terminate_instance_parser = dbaas_subparsers.add_parser('terminate_instance',
        help='Delete a MySQL instance')
    terminate_instance_parser.add_argument('--instance_id', action='store',
        required=True, help='MySQL instance ID')
    terminate_instance_parser.set_defaults(func=dbaas.func_terminate_instance)
