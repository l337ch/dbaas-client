#!/bin/

import argparse

dbaas_parser = argparse.ArgumentParser()
dbaas_parser_subparsers = dbaas_parser.add_subparsers(help='commands')

#list mysql instances
list_instance_parser = dbaas_parser_subparsers.add_parser('list_instances', help='List MySQL instances')

#create new mysql instance

#describe mysql instance
describe_instance_parser = dbaas_parser_subparsers.add_parser('describe_instance', help='Describe MySQL instance')
describe_instance_parser.add_argument('instance_id', action='store', help='MySQL instance to describe')

#create new mysql snapshot
create_snapshot_parser = dbaas_parser_subparsers.add_parser('create_snapshot', help='Create MySQL snapshot')
create_snapshot_parser.add_argument('instance_id', action='store', help='MySQL instance')

#list snapshots
list_snapshot_parser = dbaas_parser_subparsers.add_parser('list_snapshot', help='List all MySQL snapshots')

#describe snapshots
describe_snapshot_parser = dbaas_parser_subparsers.add_parser('describe_snapshot', help='Describe a MySQL snapshots')
describe_snapshot_parser.add_argument('instance_id', action='store', help='MySQL instance')

#delete snapshots
delete_snapshot_parser = dbaas_parser_subparsers.add_parser('delete_snapshot', help='Delete a MySQL snapshot')
delete_snapshot_parser.add_argument('snapshot_id', action='store', help='MySQL snapshot ID')

#print dbaas_parser.parse_args()