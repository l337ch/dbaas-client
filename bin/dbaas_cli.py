#!/bin/

import argparse

def print_list():
    print "This is a list"

def print_list2():
    print "This is a list2"

dbaas_parser = argparse.ArgumentParser()
dbaas_parser_subparsers = dbaas_parser.add_subparsers(help='commands')

#list mysql instances
list_instance_parser = dbaas_parser_subparsers.add_parser('list_instances', help='List MySQL instances')
list_instance_parser.set_defaults(function=print_list)

#create new mysql instance
create_instance_parser = dbaas_parser_subparsers.add_parser('create_instance', help='Create a new MySQL instance')
create_instance_parser.set_defaults(function=print_list2)

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

args = dbaas_parser.parse_args(['create_instance'])
print args.function()

#dbaas_http = httplib2.Http(".cache")
#resp, content = dbaas_http.request("http://15.185.163.25:8775/v1.0/dbaasapi/instances", "DELETE", headers= {'X-Auth-Token':'abc:123'})
#    url = "http://15.185.163.25:8775"
#    api_version = "v1.0"
#    uri = url + api_version

#response = json.dumps(resp)
#response_content = json.dumps(content)
#print response
#print response_content

#dbaas = DBaaSClient("abc:123")
#print dbaas._token()

#dbaas_resq = dbaas.list_instances()

#new_json = json.loads(dbaas_resq[1])


#for instance in new_json['instances']:
#    print instance['name']

# create a new mysql instance

#dbaas_create = dbaas.create_instance("lee_test2")
#print dbaas_create

# reset password

# create snapshot
#dbaas_create_snapshot = dbaas.create_snapshot("5bacdbd1-1cf5-4e7e-ac97-3fff5365ff85", "snap3")
#print dbaas_create_snapshot

#describe_snapshot
#dbaas_describe_snapshot = dbaas.describe_snapshot()
#new_json = json.loads(dbaas_describe_snapshot[1])
#print json.dumps(new_json, indent=4)

# delete snapshot
#dbaas_delete_snapshot = dbaas.delete_snapshot("b5bacdbd1-1cf5-4e7e-ac97-3fff5365ff85")

#print dbaas_delete_snapshot

# destroy mysql instance
#dbaas_delete = dbaas.delete_instance("90df25c3-33fa-48e9-bed4-f6479b878406")

#print dbaas_delete

"""
dbaas_parser = argparse.ArgumentParser()
dbaas_parser_subparsers = dbaas_parser.add_subparsers(help='commands')

#list mysql instances
list_instance_parser = dbaas_parser_subparsers.add_parser('list_instances', help='List MySQL instances')
list_instance_parser.set_defaults(function=dbaas.list_instances)

#create new mysql instance
create_instance_parser = dbaas_parser_subparsers.add_parser('create_instance', help='Create a new MySQL instance')
create_instance_parser.add_argument('--name', dest='name', action='store', help='Name for new MySQL instance')
create_instance_parser.set_defaults(function=dbaas.create_instance('name'))

#describe mysql instance
describe_instance_parser = dbaas_parser_subparsers.add_parser('describe_instance', help='Describe MySQL instance')
describe_instance_parser.add_argument('--instance_id', action='store', help='MySQL instance to describe')
#describe_instance_parser.set_defaults(function=dbaas.create_instance(['--instance_id']))

#create new mysql snapshot
create_snapshot_parser = dbaas_parser_subparsers.add_parser('create_snapshot', help='Create MySQL snapshot')
create_snapshot_parser.add_argument('--instance_id', action='store', help='MySQL instance_id')
create_snapshot_parser.add_argument('--snapshot_name', action='store', help='Name of snapshot')
#create_snapshot_parser.set_defaults(function=dbaas.create_snapshot(['--instance_id', '--snapshot_name']))

#list snapshots
list_snapshot_parser = dbaas_parser_subparsers.add_parser('list_snapshot', help='List all MySQL snapshots')
list_snapshot_parser.add_argument('--snapshot_id', action='store', help='Name of snapshot')
#list_snapshot_parser.set_defaults(function=dbaas.describe_snapshot(['--snapshot_id']))

#delete snapshots
delete_snapshot_parser = dbaas_parser_subparsers.add_parser('delete_snapshot', help='Delete a MySQL snapshot')
delete_snapshot_parser.add_argument('--snapshot_id', action='store', help='MySQL snapshot ID')
#delete_snapshot_parser.set_default(function=dbaas.delete_snapshot(['-snapshot_id']))

#delete mysql_instances


args = dbaas_parser.parse_args()
"""