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

import httplib2
import json
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
