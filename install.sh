#!/bin/bash

DIR=`dirname "$readlink -e "$0""`
cd $DIR

cp native_headers.py /usr/bin/native-headers
chmod +x /usr/bin/native-headers

cp native-headers.service /etc/systemd/user/
