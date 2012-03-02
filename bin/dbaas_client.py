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

import httplib2
import json
import argparse
import sys

# list all mysql instances for a user

class DBaaSClient(httplib2.Http):

    def __init__(self, url, token=None, api_version = "v1.0", timeout=30):
        super(DBaaSClient, self).__init__(timeout=timeout)
        self.url = url
        self.api_version = api_version
        self.token = token
        self.headers = {}
        self.headers['X-Auth-Token'] = self.token
        self.url_part = "/".join([self.url,self.api_version,"dbaasapi"])

    def list_instances(self):
        self.path = "instances"
        self.list_uri = "/".join([self.url_part,self.path])

        resp, content = super(DBaaSClient, self).request(self.list_uri, "GET", headers=self.headers)
        print json.dumps(json.loads(content), indent=4)
        return resp, content

    def create_instance(self, db_name):
        self.path = "instances"
        self.db_name = db_name
        self.create_uri = "/".join([self.url_part,self.path])
        self.headers['Content-Type'] = 'application/json'

        #construct request json
        request_json = json.dumps({"instance": {"name":self.db_name, "flavorRef":"url_to_flavor_version", "port":"3306",
                                              "dbtype":{"name":"mysql", "version":"5.1.2"}, "volume": {"size":"2"}}})
        print request_json

        resp, content = super(DBaaSClient, self).request(self.create_uri, "POST", request_json.encode('utf-8'), headers=self.headers)
        print content
        print json.dumps(json.loads(content), indent=4)
        return resp, content

    #describe specific mysql instance
    def describe_instance(self, instance_id):
        self.path = instance_id
        self.list_uri = "/".join([self.url_part,self.path])

        resp, content = super(DBaaSClient, self).request(self.list_uri, "GET", headers=self.headers)
        print json.dumps(json.loads(content), indent=4)
        return resp, content

    #create snapshot for a mysql instance
    def create_snapshot(self, instance_id, snapshot_name):
        self.instance_id = instance_id
        self.snapshot_name = snapshot_name
        self.path = "snapshots"
        self.snap_uri = "/".join([self.url_part,self.path])
        self.headers['Content-Type'] = 'application/json'
        request_json = json.dumps({"snapshot": {"instanceId":self.instance_id, "name": self.snapshot_name}})

        resp, content = super(DBaaSClient, self).request(self.snap_uri, "POST", request_json.encode('utf-8'), headers=self.headers)
        print json.dumps(json.loads(content), indent=4)
        return resp, content

    #describe snapshot for a mysql instance
    def describe_snapshot(self, instance_id = None):
        self.path = "snapshots"
        instance_id = instance_id
        describe_uri = "/".join([self.url_part,self.path]) + "?instance_id=" + str(instance_id)

        resp, body = super(DBaaSClient, self).request(describe_uri, "GET", headers=self.headers)
        print json.dumps(json.loads(body), indent=4)
        return resp, body

    #delete snapshot
    def delete_snapshot(self, snapshot_id):
        self.path = "snapshots"
        snapshot_id = snapshot_id
        delete_uri = "/".join([self.url_part,self.path,snapshot_id])

        resp, content = super(DBaaSClient, self).request(delete_uri, "DELETE", headers=self.headers)
        print content
        return resp, content

    #delete mysql instance
    def delete_instance(self, instance_id):
        self.instance_id = instance_id
        self.path = "instances"
        self.delete_uri = "/".join([self.url_part, self.path, self.instance_id])
        print self.delete_uri

        resp, content = super(DBaaSClient, self).request(self.delete_uri, "DELETE", headers=self.headers)
        print json.dumps(json.loads(content), indent=4)
        return resp, content

dbaas_demo_url = "http://15.185.163.25:8775"
dbaas = DBaaSClient(dbaas_demo_url, "abc:123")

dbaas_parser = argparse.ArgumentParser()
dbaas_parser_subparsers = dbaas_parser.add_subparsers(help='commands')

#list mysql instances
list_instance_parser = dbaas_parser_subparsers.add_parser('list_instances', help='List MySQL instances')
list_instance_parser.add_argument('--command', action='store', default='list_instance')
#list_instance_parser.set_defaults(function=dbaas.list_instances)

#create new mysql instance
create_instance_parser = dbaas_parser_subparsers.add_parser('create_instance', help='Create a new MySQL instance')
create_instance_parser.add_argument('--name', dest='name', action='store', required=True, help='Name for new MySQL instance')
create_instance_parser.add_argument('--command', action='store', default='create_instance')
#create_instance_parser.set_defaults(function=dbaas.create_instance('name'))

#describe mysql instance
describe_instance_parser = dbaas_parser_subparsers.add_parser('describe_instance', help='Describe MySQL instance')
describe_instance_parser.add_argument('--instance_id', action='store', required=True, help='MySQL instance to describe')
describe_instance_parser.add_argument('--command', action='store', default='discribe_instance')
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

    if args.command == "list_instance":
        print "list_instance"
        dbaas.list_instances()
    elif args.command == "create_instance":
        print "create_instance --name=" + args.name
        dbaas.create_instance(args.name)

    elif args.command == "describe_instance":
        print "describe_instance --instance_id=" + args.instance_id
        dbaas.describe_instance(args.instance_id)

    elif args.command == "create_snapshot":
        print "create_snapshot --instance_id=" + args.instance_id + " --snapshot_name=" + args.snapshot_name
        dbaas.create_snapshot(args.instance_id, args.snapshot_name)

    elif args.command == "list_snapshot":
        print "list_snapshot --instance_id=" + str(args.snapshot_id)
        dbaas.describe_snapshot(args.snapshot_id)

    elif args.command == "delete_snapshot":
        print "delete_snapshot --snapshot_id=" + args.snapshot_id

    elif args.command == "delete_instance":
        print "delete_instance --instance_id=" + args.instance_id
        dbaas.delete_instance(args.instance_id)

    else:
        dbaas_parser.parse_args(['-h'])

if __name__ == "__main__":
    main()
