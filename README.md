DBaaS Client
============

For easy and fun client access to Database as a Service.

Instructions
------------

For fast, easy consumption...install these python libraries before running.

httplib2
argparse

ie : 

    easy_install httplib2
    easy_install argparse

Or use pip install if you prefer.

### Environment

Add the following to your environment:

DBAAS_USERNAME=<dbaas username>
DBAAS_PASSWORD=<dbaas password>
DBAAS_ENDPOINT=<url to the dbaas server>

Implemented features
--------------------

1.  Show list of instances
2.  Show instance details
3.  Create MySQL instance
4.  Create snapshot of a running MySQL instance
5.  List all snapshots
6.  List snapshots by MySQL instance
7.  Show snapshot details
8.  Create a new MySQL instance from a snapshot
9.  Delete a snapshot
10. Terminate a MySQL instance