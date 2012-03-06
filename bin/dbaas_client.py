#!/usr/local/bin/python

# Copyright 2012 HP Software, LLC"
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
import os
from dbaasclient import client

def env(*vars, **kwargs):
    """
    returns the first environment variable set
    if none are non-empty, defaults to '' or keyword arg default
    """
    for v in vars:
        value = os.environ.get(v, None)
        if value:
            return value
    return kwargs.get('default', '')

dbaas_demo_url = "http://15.185.163.25:8775"
dbaas = client.DBaaSClient(dbaas_demo_url, "abc:123")

dbaas_parser = argparse.ArgumentParser(prog='dbaas_client',
    epilog='See "dbaas_client help COMMAND" for help on a specific command.',
    add_help=False)

#Global arugments
dbaas_parser.add_argument('-h', '--help',
    action='help',
    help=argparse.SUPPRESS)

dbaas_parser.add_argument('--username',
    default=env('DBAAS_USERNAME'),
    help='Defaults to env[DBAAS_USERNAME]')

dbaas_parser.add_argument('--password',
    default=env('DBAAS_PASSWORD'),
    help='Defaults to env[DBAAS_PASSWORD]')

dbaas_parser.add_argument('--endpoint',
    default=env('DBAAS_ENDPOINT'),
    help='Defaults to env[DBAAS_ENDPOINT]')

dbaas_parser_subparsers = dbaas_parser.add_subparsers(help='commands')

#list mysql instances
list_instance_parser = dbaas_parser_subparsers.add_parser('list_instances', help='List MySQL instances')
list_instance_parser.add_argument('--command', action='store', default='list_instances')
#list_instance_parser.set_defaults(function=dbaas.list_instances)

#create new mysql instance
create_instance_parser = dbaas_parser_subparsers.add_parser('create_instance', help='Create a new MySQL instance')
create_instance_parser.add_argument('--name', dest='name', action='store', required=True, help='Name for new MySQL instance')
create_instance_parser.add_argument('--command', action='store', default='create_instance')
#create_instance_parser.set_defaults(function=dbaas.create_instance('name'))

#describe mysql instance
describe_instance_parser = dbaas_parser_subparsers.add_parser('describe_instance', help='Describe MySQL instance')
describe_instance_parser.add_argument('--instance_id', action='store', required=True, help='MySQL instance to describe')
describe_instance_parser.add_argument('--command', action='store', default='describe_instance')
#describe_instance_parser.set_defaults(function=dbaas.create_instance(['--instance_id']))

#create new mysql snapshot
create_snapshot_parser = dbaas_parser_subparsers.add_parser('create_snapshot', help='Create MySQL snapshot')
create_snapshot_parser.add_argument('--instance_id', action='store', required=True, help='MySQL instance_id')
create_snapshot_parser.add_argument('--snapshot_name', action='store', required=True, help='Name of snapshot')
create_snapshot_parser.add_argument('--command', action='store', default='create_snapshot')
#create_snapshot_parser.set_defaults(function=dbaas.create_snapshot(['--instance_id', '--snapshot_name']))

#list snapshots
list_snapshot_parser = dbaas_parser_subparsers.add_parser('list_snapshot', help='List all MySQL snapshots')
list_snapshot_parser.add_argument('--snapshot_id', action='store', help='Name of snapshot')
list_snapshot_parser.add_argument('--command', action='store', default='list_snapshot')
#list_snapshot_parser.set_defaults(function=dbaas.describe_snapshot(['--snapshot_id']))

#delete snapshots
delete_snapshot_parser = dbaas_parser_subparsers.add_parser('delete_snapshot', help='Delete a MySQL snapshot')
delete_snapshot_parser.add_argument('--snapshot_id', action='store', required=True, help='MySQL snapshot ID')
delete_snapshot_parser.add_argument('--command', action='store', default='delete_snapshot')
#delete_snapshot_parser.set_default(function=dbaas.delete_snapshot(['-snapshot_id']))

#delete mysql instance
delete_instance_parser = dbaas_parser_subparsers.add_parser('delete_instance', help='Delete a MySQL instance')
delete_instance_parser.add_argument('--instance_id', action='store', required=True, help='MySQL instance ID')
delete_instance_parser.add_argument('--command', action='store', default='delete_instance')

def main():
    args = dbaas_parser.parse_args()
    dbaas_command = args.command
    print dbaas_command

    dbaas_options = {"list_instances"    : dbaas.list_instances,
                     "create_instance"   : dbaas.create_instance(args.name),
                     "describe_instance" : dbaas.describe_instance(args.instance_id),
                     "create_snapshot"   : dbaas.create_snapshot(args.instance_id, args.snapshot_name),
                     "list_snapshot"     : dbaas.describe_snapshot(args.instance_id),
                     "delete_snapshot"   : dbaas.delete_snapshot(args.snapshot_id),
                     "delete_instance"   : dbaas.delete_instance(args.instance_id)
                     }

    dbaas_options[dbaas_command]()

#    if args.command == "list_instance":
#        print "list_instance"
#        dbaas.list_instances()
#    elif args.command == "create_instance":
#        print "create_instance --name=" + args.name
#        dbaas.create_instance(args.name)

#    elif args.command == "describe_instance":
#        print "describe_instance --instance_id=" + args.instance_id
#        dbaas.describe_instance(args.instance_id)

#    elif args.command == "create_snapshot":
#        print "create_snapshot --instance_id=" + args.instance_id + " --snapshot_name=" + args.snapshot_name
#        dbaas.create_snapshot(args.instance_id, args.snapshot_name)

#    elif args.command == "list_snapshot":
#        print "list_snapshot --instance_id=" + str(args.snapshot_id)
#        dbaas.describe_snapshot(args.snapshot_id)

#    elif args.command == "delete_snapshot":
#        print "delete_snapshot --snapshot_id=" + args.snapshot_id

#    elif args.command == "delete_instance":
#        print "delete_instance --instance_id=" + args.instance_id
 #       dbaas.delete_instance(args.instance_id)

#    else:
#        dbaas_parser.parse_args(['-h'])

if __name__ == "__main__":
    main()