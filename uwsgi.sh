#!/bin/bash

case $1 in
    start)
        echo 'uwsgi start'
        uwsgi --ini ./uwsgiConfig/api_uwsgi.ini 
        ;;
    reload)
        echo 'uwsgi reload'
        uwsgi --reload ./uwsgiConfig/uwsgi.pid
        ;;
    stop)
        echo 'uwsgi stop'
        uwsgi --stop ./uwsgiConfig/uwsgi.pid
        ;;
    *)
        echo 'wrong command'
        ;;
esac

