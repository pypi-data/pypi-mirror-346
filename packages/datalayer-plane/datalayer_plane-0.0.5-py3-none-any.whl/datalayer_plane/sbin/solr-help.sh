#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Datalayer Solr Help"$NOCOLOR$NOBOLD
echo

echo -e $YELLOW"""Delete Solr documents
"""$NOCOLOR
echo -e """curl --user solr:$DATALAYER_SOLR_PASSWORD \\
  http://localhost:8983/solr/xyz/update?commitWithin=500 \\
  -d '{ delete: { query: \"uid:xyz\" } }'
"""

echo -e $YELLOW"View Solr Logs"$NOCOLOR
echo
echo -e """cat ${SOLR_HOME}/server/logs/solr.log
"""

echo -e $YELLOW"View Solr UI"$NOCOLOR
echo
echo -e "http://localhost:8983/solr"
echo -e """http://localhost:8983/solr/admin/info/system
"""

echo -e $YELLOW"Check Solr"$NOCOLOR
echo
echo -e """$SOLR_HOME/bin/solr status
"""

echo -e $YELLOW"Create a collection - The create command detects the mode that Solr is running in (standalone or SolrCloud) and then creates a core or collection depending on the mode.
"$NOCOLOR
echo -e "$SOLR_HOME/bin/solr create -c demo -shards 2 -replicationFactor 2 -d $DATALAYER_HOME/etc/solr/demo -p 8983"
echo -e """$SOLR_HOME/bin/solr create_collection -c demo -shards 1 -replicationFactor 1 -d $DATALAYER_HOME/etc/solr/demo -p 8983
"""

echo -e $YELLOW"Delete a collection"$NOCOLOR
echo
echo -e """$SOLR_HOME/bin/solr delete -c demo
"""

echo -e $YELLOW"Add documents"$NOCOLOR
echo
echo -e """$SOLR_HOME/bin/post -c demo $SOLR_HOME/example/exampledocs/*.xml
$SOLR_HOME/bin/post -c demo $SOLR_HOME/docs/
$SOLR_HOME/bin/post -c demo $SOLR_HOME/example/exampledocs/*.xml
$SOLR_HOME/bin/post -c demo $SOLR_HOME/example/exampledocs/books.json
$SOLR_HOME/bin/post -c demo $SOLR_HOME/example/exampledocs/books.csv
$SOLR_HOME/bin/post -c demo -d \"<delete><id>SP2514N</id></delete>\"
curl http://localhost:8983/solr/demo/update?commit=true -H 'Content-type:application/json' -d '
[
 {\"id\" : \"book1\",
  \"title\" : \"American Gods\",
  \"author\" : \"Neil Gaiman\"
 }
]'
"""

echo -e $YELLOW"""Query documents
"""$NOCOLOR
echo -e """http://localhost:8983/solr/demo/select?q=video
"""

echo -e $YELLOW"View shards"$NOCOLOR
echo
echo -e "http://localhost:8983/solr/#/demo/collection-overview"
echo -e """http://localhost:8983/solr/#/demo_shard1_replica_n1
"""

echo -e $YELLOW"""View logs
"""$NOCOLOR
echo -e "tail -f $SOLR_HOME/server/logs/solr.log
"

echo -e $YELLOW"""Start preconfigured sets
"""$NOCOLOR
echo -e "$SOLR_HOME/bin/solr start -e cloud -noprompt"
echo -e """$SOLR_HOME/bin/solr start -e techproducts
"""

echo -e """Commands with Docker
"""
echo -e "docker exec -it --user=solr solr bin/solr create_collection -c demo -shards 3 -replicationFactor 3"
echo -e "cd $SOLR_HOME"
echo -e "docker exec -it --user=solr solr bin/post -c demo example/exampledocs/manufacturers.xml"
echo -e "docker cp $SOLR_HOME/example/exampledocs/manufacturers.xml solr:/opt/solr/manufacturers.xml"
echo -e """docker exec -it --user=solr solr bin/post -c demo manufacturers.xml
"""

echo -e $YELLOW"""Backup
"""$NOCOLOR
echo -e """curl http://localhost:8983/solr/admin/collections?action=BACKUP -d '
collection=demo&
location=/tmp&
name=solr_demo_backup'
ls /tmp/solr_demo_backup
curl http://localhost:8983/solr/admin/collections?action=RESTORE -d '
collection=demo&
location=/tmp&
name=solr_demo_backup'
"""
