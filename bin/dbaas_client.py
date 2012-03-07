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
__author__ = 'lchang'

import argparse
import httplib2
import json
import sys

class DBaaSCLI(httplib2.Http):

    def __init__(self, url, token=None, api_version = "v1.0", timeout=30):
        super(DBaaSClient, self).__init__(timeout=timeout)
        self.url = url
        self.api_version = api_version
        self.token = token
        self.headers = {}
        self.headers['X-Auth-Token'] = token
        self.url_part = "/".join([self.url,self.api_version,"dbaasapi"])

    def list_instances(self, instance_id=None):
        path = "instances"

        #build different uris for list and describe
        #describe actions have an instance_id
        if instance_id is None:
            list_uri = "/".join([self.url_part,path])
        else:
            list_uri = "/".join([self.url_part,path, instance_id])

        resp, content = super(DBaaSCLI, self).request(list_uri, "GET", headers=self.headers)
        result_json = json.loads(content)
        #print result_json


        if instance_id is None:
            il = 0
            table = [['instance_id', 'name', 'status']]
            for instances in result_json['instances']:
                row = result_json['instances'][il]
                table.append([str(row['id']), str(row['name']), str(row['status'])])
                il += 1
        else:
            table = [['instance_id', 'name', 'status', 'hostname', 'created']]

            row = result_json['instance']
            table.append([str(row['id']), str(row['name']), str(row['status']),
                          str(row['hostname']), str(row['created'])])

        self.pprint_table(table)

        return resp, content

    def create_instance(self, db_name, snapshot_id=None):

        path = "instances"
        create_uri = "/".join([self.url_part, path])
        self.headers['Content-Type'] = 'application/json'
        #construct request json
        if snapshot_id is None:
            create_json = {"instance": {"name": db_name, "flavorRef":"url_to_flavor_version", "port":"3306",
                                        "dbtype":{"name":"mysql", "version":"5.1.2"}, "volume": {"size":"2"}}}
            request_json = json.dumps(create_json)
        else:
            create_json = {"instance": {"snapshotId": snapshot_id, "name": db_name, "flavorRef":"url_to_flavor_version",
                                        "port":"3306", "dbtype":{"name":"mysql", "version":"5.1.2"},
                                        "volume": {"size":"2"}}}
            request_json = json.dumps(create_json)

        resp, content = super(DBaaSCLI, self).request(create_uri, "POST", request_json.encode('utf-8'),
            headers=self.headers)

        result_json = json.loads(content)
        #print content
        #print json.dumps(json.loads(content), indent=4)

        table = [['instance_id', 'name', 'status', 'hostname', 'launchTime']]

        row = result_json['instance']
        table.append([str(row['id']), str(row['name']), str(row['status']), str(row['hostname']), str(row['created'])])

        self.pprint_table(table)

        return resp, content

    def reset_password(self, instance_id, instance_password='null'):
        path = "instances"
        reset_uri = "/".join([self.url_part, path, instance_id,'action'])
        self.headers['Content-Type'] = 'application/json'
        create_json = {'resetPassword':instance_password}
        request_json = json.dumps(create_json)

        resp, content = super(DBaaSCLI, self).request(reset_uri, "POST", request_json.encode('utf-8'),
            headers=self.headers)

        print content
        print json.dumps(json.loads(content), indent=4)
        return resp, content

    def restart_instance(self, instance_id, restart_type='SOFT'):
        path = "instances"
        reset_uri = "/".join([self.url_part, path, instance_id, 'action'])
        self.headers['Content-Type'] = 'application/json'
        create_json = {'restart':{'type':restart_type}}
        request_json = json.dumps(create_json)

        resp, content = super(DBaaSCLI, self).request(reset_uri, "POST", request_json.encode('utf-8'),
            headers=self.headers)

        print content
        print json.dumps(json.loads(content), indent=4)
        return resp, content

    #create snapshot for a mysql instance
    def create_snapshot(self, instance_id, snapshot_name):
        path = "snapshots"
        snap_uri = "/".join([self.url_part,path])
        self.headers['Content-Type'] = 'application/json'
        request_json = json.dumps({"snapshot": {"instanceId":instance_id, "name": snapshot_name}})

        resp, content = super(DBaaSCLI, self).request(snap_uri, "POST", request_json.encode('utf-8'),
            headers=self.headers)

        result_json = content
        print result_json.split("\n")
        print json.dumps(result_json, indent=4)
        return resp, content

    #describe snapshot for a mysql instance
    def describe_snapshot(self, instance_id=None):
        self.path = "snapshots"
        instance_id = instance_id
        describe_uri = "/".join([self.url_part,self.path]) + "?instance_id=" + str(instance_id)
        #print describe_uri

        resp, content = super(DBaaSCLI, self).request(describe_uri, "GET", headers=self.headers)
        result_json = json.loads(content)

        #print json.dumps(json.loads(content), indent=4)

        il = 0
        table = [['snapshot_id', 'name', 'status', 'instance_id', 'created']]
        for instances in result_json['snapshots']:
            row = result_json['snapshots'][il]
            table.append([str(row['id']), str(row['name']), str(row['status']), str(row['instanceId']),
                          str(row['created'])])
            il += 1

        self.pprint_table(table)

        return resp, content

    #delete snapshot
    def delete_snapshot(self, snapshot_id):
        self.path = "snapshots"
        snapshot_id = snapshot_id
        delete_uri = "/".join([self.url_part,self.path,snapshot_id])
        print delete_uri

        resp, content = super(DBaaSCLI, self).request(delete_uri, "DELETE", headers=self.headers)
        print content
        return resp, content

    #delete mysql instance
    def terminate_instance(self, instance_id):
        self.instance_id = instance_id
        self.path = "instances"
        self.delete_uri = "/".join([self.url_part, self.path, self.instance_id])
        print self.delete_uri

        resp, content = super(DBaaSCLI, self).request(self.delete_uri, "DELETE", headers=self.headers)
        return resp, content

    """
    Creat some ASCII tables with dynamic column sizing per row
    """
    def get_max_width(self, table, index):
        #Get the maximum width of the given column
        return max([len(str(row[index])) for row in table])

    def pprint_table(self, table):
        """Prints out a table of data, padded for alignment
        Each row must have the same number of columns. """
        col_paddings = []
        row_cnt = 0
        col_per_row = len(table[0])
        out = sys.stdout

        print >> out

        for i in range(len(table[0])):
            col_paddings.append(self.get_max_width(table, i))

        for row in table:
            row_cnt += 1
            # left col is justified left
            print >> out, row[0].ljust(col_paddings[0] + 1),
            # rest of the cols are justified right
            for i in range(1, len(row)):
                col = str(row[i]).rjust(col_paddings[i] + 2)
                print >> out, col,
            print >> out
            if row_cnt == 1:
                print >> out, "=" * (sum(col_paddings) + (3*col_per_row))

        print >> out

class ArgDBaaSCLI(DBaaSCLI):

    def __init__(self, url, token=None, api_version = "v1.0", timeout=30):
        super(DBaaSCLI, self).__init__(timeout=timeout)
        #print "Init DBaaS " + url
        self.url = url
        self.api_version = api_version
        self.token = token
        self.headers = {}
        self.headers['X-Auth-Token'] = token
        self.url_part = "/".join([self.url,self.api_version,"dbaasapi"])

    def func_list_instances(self, opts):
        self.list_instances(opts.instance_id)

    def func_create_instance(self, opts):
        self.create_instance(opts.instance_name, opts.snapshot_id)

    def func_reset_password(self, opts):
        self.reset_password(opts.instance_id, opts.instance_password)

    def func_restart_instance(self, opts):
        self.restart_instance(opts.instance_id, opts.restart_type)

    def func_create_snapshot(self, opts):
        self.create_snapshot(opts.instance_id, opts.snapshot_id)

    def func_list_snapshot(self, opts):
        self.describe_snapshot(opts.instance_id)

    def func_delete_snapshot(self, opts):
        self.delete_snapshot(opts.snapshot_id)

    def func_terminate_instance(self, opts):
        self.terminate_instance(opts.instance_id)


dbaas_demo_url = "http://15.185.163.25:8775"
dbaas = ArgDBaaSCLI(dbaas_demo_url, "abc:123")

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

def main(s=None):
    opts = dbaas_parser.parse_args(s)
    #print "OPTS: " + str(opts)
    opts.func(opts)

if __name__ == "__main__":
    main()
    #main(['-h'])
    #main(['list_instances'])
    #main(['list_instances', '--instance_id', '5ceae7e4-6c5a-4f55-8db9-7fd4ae7416fe'])
    #main(['create_instance', '--instance_name', 'mostly harmless'])
    #main(['reset_password', '--instance_id', 'c2ff4133-c690-4ab4-9939-05db1bcd013c'])
    #main(['restart_instance', '--instance_id', 'c2ff4133-c690-4ab4-9939-05db1bcd013c'])
    #main(['list_snapshot'])
    #main(['list_snapshot', '--instance_id', '57c32bf5-5011-413e-9749-27b03963c25e'])
    #main(['create_snapshot', '--instance_id', '7100cdfa-badd-4469-a9c8-2e6603ea7e41',
    # '--snapshot_name', 'back it up take seven'])
    #main(['delete_snapshot', '--snapshot_id', 'b626a788-d689-484f-ab14-5469a6c9d526'])
    #main(['terminate_instance', '--instance_id', '92f4af8d-4543-4941-85e2-a224fb67a313'])