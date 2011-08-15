#! /bin/bash

. mysql.credentials

if [ "$1" == "--install" ]; then
	mysql -h $HOST -u $USER --password=$PASSWORD $DATABASE < mysql/dropall.sql
	mysql -h $HOST -u $USER --password=$PASSWORD $DATABASE < mysql/v1.sql
else
	mysql -h $ENDPOINT -u $USER --password=$PASSWORD $DATABASE
fi

