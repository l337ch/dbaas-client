#!/bin/python env

# Copyright 2012 HP Software, LLC"
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed  to in writing, software
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

    def resp_handler(self, resp, content, message=None):
        resp_status = int(resp['status'])

#        print resp_status
#        print content
#        print "---------"

        if resp_status >= 300:
            if resp_status == 404:
                print "\n" * 2 + "Resource " + message + " does not exist" + "\n" * 2
            else:
                print "\n" * 2 + "Something went horribly wrong" + "\n" * 2
        else:
            try:
                result_json = json.loads(content)
                #print result_json
                self.json_pprint_table(result_json)
            except IndexError:
                print "No Resources Returned"
                print
#            except:
#                print "Unexpected error:", sys.exc_info()[0]
#                raise
            except:
                print
                print "Accepted for processing"
                print

    def list_instances(self, instance_id=None):
        path = "instances"

        #build different uris for list and describe
        #describe actions have an instance_id
        if instance_id is None:
            list_uri = "/".join([self.url_part,path])
        else:
            list_uri = "/".join([self.url_part,path, instance_id])

        resp, content = super(DBaaSCLI, self).request(list_uri, "GET", headers=self.headers)
        #print result_json

        #self.pprint_table(table)

        self.resp_handler(resp, content)

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

        self.resp_handler(resp, content)

        return resp, content

    def reset_password(self, instance_id, instance_password='null'):
        path = "instances"
        reset_uri = "/".join([self.url_part, path, instance_id,'resetpassword'])
        self.headers['Content-Type'] = 'application/json'

        resp, content = super(DBaaSCLI, self).request(reset_uri, "POST", body='',
            headers=self.headers)

        create_json = {'resetPassword':instance_password}

        result_json = json.loads(content)

        print
        print "new password = " + str(result_json['password'])
        print

        #print json.dumps(json.loads(content), indent=4)
        return resp, content

    def restart_instance(self, instance_id, restart_type='SOFT'):
        path = "instances"
        reset_uri = "/".join([self.url_part, path, instance_id, 'restart'])
        self.headers['Content-Type'] = 'application/json'
        create_json = {'restart':{'type':restart_type}}
        request_json = json.dumps(create_json)

        resp, content = super(DBaaSCLI, self).request(reset_uri, "POST", body=None,
            headers=self.headers)

        self.resp_handler(resp, content, instance_id)

        return resp, content

    #create snapshot for a mysql instance
    def create_snapshot(self, instance_id, snapshot_name):
        path = "snapshots"
        snap_uri = "/".join([self.url_part,path])
        self.headers['Content-Type'] = 'application/json'
        request_json = json.dumps({"snapshot": {"instanceId":instance_id, "name": snapshot_name}})

        resp, content = super(DBaaSCLI, self).request(snap_uri, "POST", request_json.encode('utf-8'),
            headers=self.headers)

        self.resp_handler(resp, content)

        return resp, content

    #describe snapshot for a mysql instance
    def describe_snapshot(self, opts):
        self.path = "snapshots"
        instance_id = opts.instance_id or ''
        snapshot_id = opts.snapshot_id
        if snapshot_id is not None:
            describe_uri = "/".join([self.url_part,self.path,str(snapshot_id)])
        else:
            describe_uri = "/".join([self.url_part,self.path]) + "?instanceId=" + str(instance_id)

        resp, content = super(DBaaSCLI, self).request(describe_uri, "GET", headers=self.headers)

        #print json.dumps(json.loads(content), indent=4)

        self.resp_handler(resp, content)

        return resp, content

    #delete snapshot
    def delete_snapshot(self, snapshot_id):
        self.path = "snapshots"
        snapshot_id = snapshot_id
        delete_uri = "/".join([self.url_part,self.path,snapshot_id])
        #print delete_uri

        resp, content = super(DBaaSCLI, self).request(delete_uri, "DELETE", headers=self.headers)

        self.resp_handler(resp, content, snapshot_id)

        return resp, content

    #delete mysql instance
    def terminate_instance(self, instance_id):
        self.instance_id = instance_id
        self.path = "instances"
        self.delete_uri = "/".join([self.url_part, self.path, self.instance_id])
        #print self.delete_uri

        resp, content = super(DBaaSCLI, self).request(self.delete_uri, "DELETE", headers=self.headers)

        self.resp_handler(resp, content, instance_id)

        return resp, content


    def get_max_width(self, table, index):
        """Creat some ASCII tables with dynamic column sizing per row.
        Get the maximum width of the given column"""
        return max([len(str(row[index])) for row in table])

    def pprint_table(self, table):
        """Prints out a table of data, padded for alignment
        Each row must have the same number of columns. """
        col_paddings = []
        row_cnt = 0
        col_per_row = len(table[0])
        out = sys.stdout

        print >> out
        print >> out

        for i in range(len(table[0])):
            col_paddings.append(self.get_max_width(table, i))

        for row in table:
            row_cnt += 1
            # left col is justified left
            print >> out, str(row[0]).ljust(col_paddings[0] + 1),
            # rest of the cols are justified left also
            for i in range(1, len(row)):
                col = str(row[i]).ljust(col_paddings[i] + 2)
                print >> out, col,
            print >> out
            if row_cnt == 1:
                print >> out, "=" * (sum(col_paddings) + (3*col_per_row))

        print >> out, "=" * (sum(col_paddings) + (3*col_per_row))
        print >> out
        print >> out

    def parse_json_obj(self, json_object):
        """Recursively search json_obj three levels deep. This is also
        testing for list types. PLEASE REFACTOR"""
        keys = []
        values = []

        for key1 in json_object:
            v = []
            k = []
            #test for value of key1 is a dict
            if isinstance(json_object[key1], dict):
                json_1 = json_object[key1]
                for key2 in json_1:
                    #test for value of key2 is a dict
                    if isinstance(json_1[key2], dict):
                        for key3 in json_1[key2]:
                            if key3 != 'links':
                                k.insert(len(k), key3)
                                v.insert(len(v), json_1[key2][key3])
                    else:
                        if key2 != 'links':
                            k.insert(len(k), key2)
                            v.insert(len(v), json_1[key2])
                values.append(v)

            #test to see if this is a list
            elif isinstance(json_object[key1], list):
                #iterate through the list
                for index in json_object[key1]:
                    v = []
                    for key2 in index:
                    #test for value of key2 is a dict
                        if isinstance(index[key2], dict):
                            for key3 in index[key2]:
                                if key3 != 'links':
                                    k.insert(len(k), key3)
                        elif key2 != 'links':
                            k.insert(len(k), key2)
                            v.insert(len(v), index[key2])

                    values.append(v)

            else:
                k.insert(len(keys), key1)
                v.insert(len(v), json_object[key1])

        keys = [ x for i,x in enumerate(k) if x not in k[i+1:]]
        result_list = [keys] + values
        return result_list
    def json_pprint_table(self, content):
        formated_list = self.parse_json_obj(content)

        self.pprint_table(formated_list)

class ArgDBaaSCLI(DBaaSCLI):

    def __init__(self, url, token=None, api_version = "v1.0", timeout=60):
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
        self.create_snapshot(opts.instance_id, opts.snapshot_name)

    def func_list_snapshot(self, opts):
        self.describe_snapshot(opts)

    def func_delete_snapshot(self, opts):
        self.delete_snapshot(opts.snapshot_id)

    def func_terminate_instance(self, opts):
        self.terminate_instance(opts.instance_id)


dbaas_demo_url = "http://15.185.163.25:8775"
dbaas = ArgDBaaSCLI(dbaas_demo_url, "abc:123")

dbaas_parser = argparse.ArgumentParser(description='Database as a Service commandline tool')
dbaas_subparsers = dbaas_parser.add_subparsers()

#list mysql instances
list_instance_parser = dbaas_subparsers.add_parser('list_instances',
    help='List MySQL instances')
list_instance_parser.add_argument('--instance_id', action='store',
    required=False, help='Show MySQL instance details by ID')
list_instance_parser.set_defaults(func=dbaas.func_list_instances)

#create new mysql instance
create_instance_parser = dbaas_subparsers.add_parser('create_instance',
    help='Create a new MySQL instance')
create_instance_parser.add_argument('--instance_name', action='store',
    required=True, help='Name for the new MySQL instance')
create_instance_parser.add_argument('--snapshot_id', action='store',
    help='Snapshot to use for MySQL instance creation')
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

def main(s=None):
    opts = dbaas_parser.parse_args(s)
    opts.func(opts)

if __name__ == "__main__":
    main()