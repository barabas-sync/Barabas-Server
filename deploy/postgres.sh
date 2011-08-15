#! /bin/bash

. pgsql.credentials

if [ "$1" == "--install" ]; then
	psql -c "$(cat postgres/dropall.sql postgres/v1.sql)" -d $DBNAME -h $HOST -U $USER
else
	psql -d $DBNAME -h $HOST -U $USER
fi
