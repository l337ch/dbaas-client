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
#import urllib.request
import json

# list all mysql instances for a user

class DBaaSClient(httplib2.Http):

    def __init__(self, url, token=None, api_version = "v1.0", timeout=20):
        super(DBaaSClient, self).__init__(timeout=timeout)
        self.url = url
        self.api_version = api_version
        self.token = token
        self.headers = {}
        self.headers['X-Auth-Token'] = self.token
        self.url_part = self.url + self.api_version + "/dbaasapi"

    def _token(self):
        return self.token

    def list_instances(self):
        self.path = "instances"
        self.list_uri = "/".join([self.url_part,self.path])
        print self.list_uri

        resp, content = super(DBaaSClient, self).request(self.list_uri, "GET", headers=self.headers)
        return resp, content

    def create_instance(self, db_name):
        """
        create new mysql instance
        example api
        {
          "instance": {
            "name": "'my_instance_name'",
            "flavor": "url_to_flavor_version",
            "port": "3306",
            "dbtype": {
              "name": "mysql",
              "version": "5.1.2"
            },
            "volume":
            {
              "size": "2"
            }
          }
        }
        """
        #construct request json
        self.path = "instances"
        self.db_name = db_name
        self.create_uri = "/",join([self.url_part,self.path])
        self.headers['Content-Type'] = 'application/json'

        self.request_json = json.dumps({"instance": {"name":self.db_name, "flavorRef":"url_to_flavor_version", "port":"3306",
                                              "dbtype":{"name":"mysql", "version":"5.1.2"}, "volume": {"size":"2"}}})

        resp, content = super(DBaaSClient, self).request(self.create_uri, "POST", self.request_json.encode('utf-8'), headers=self.headers)
        return resp, content

    #describe specific mysql instance
    def describe_instance(self, instance_id):
        self.path = instance_id
        self.list_uri = "/".join([self.url_part,self.path])

        resp, content = super(DBaaSClient, self).request(self.list_uri, "GET", headers=self.headers)
        return resp, content

    #create snapshot for a mysql instance
    def create_snap(self, instance_id, snapshot_name):
        self.instance_id = instance_id
        self.snapshot_name = snapshot_name
        self.path = "snapshots"
        self.delete_uri = self.url_part + self.path
        self.headers['Content-Type'] = 'application/json'

        self.request_json = json.dumps({"snapshot": {"instanceId":self.instance_id, "name": self.snapshot_name}})

        resp, content = super(DBaaSClient, self).request(self.create_uri, "POST", self.request_json.encode('utf-8'), headers=self.headers)
        return resp, content

    #describe snapshot for a mysql instance
    def describe_snapshot(self, instance_id):
        self.path = "snapshots"
        self.instance_id = instance_id
        self.describe_uri = "/".join([self.url_part,self.path,self.instance_id])

        resp, content = super(DBaaSClient, self).request(self.describe_uri, "GET", headers=self.headers)
        return resp, content

    #delete snapshot
    def delete_snapshot(self, snapshot_id):
        self.path = "snapshots"
        self.snapshot_id = snapshot_id
        self.delete_uri = "/".join([self.url_part,self.path,self.snapshot_id])

        resp, content = super(DBaaSClient, self).request(self.delete_uri, "DELETE", headers=self.headers)
        return resp, content

    #delete mysql instance
    def delete_instance(self, instance_id):
        self.instance_id = instance_id
        self.path = "instances"
        self.delete_uri = "/".join([self.url_part, self.path, self.path])
        self.headers['Content-Type'] = 'application/json'

        resp, content = super(DBaaSClient, self).request(self.delete_uri, "DELETE", headers=self.headers)
        return resp, content


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

dbaas_demo_url = "http://15.185.163.25:8775/"

dbaas = DBaaSClient(dbaas_demo_url, "abc:123")

dbaas_resp = dbaas.list_instances

print dbaas_resp

# create a new mysql instance

#dbaas_create = dbaas.create_instance("lee_test")
#print dbaas_create

# reset password

# create snapshot

# delete snapshot

# destroy mysql instance
#dbaas_delete = dbaas.delete_instance("82287bb1-e266-4653-8165-686f802bee15")

#print dbaas_delete