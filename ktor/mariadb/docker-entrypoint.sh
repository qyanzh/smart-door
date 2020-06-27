#!/bin/bash
mysql -uroot -p1234 << EOF
source /usr/local/schema.sql;
