#!/bin/bash
set -e

recreate_db() {
    echo "starting drop_tables"
    python3 ./manage.py database drop_tables
    echo "starting create_tables"
    python3 ./manage.py database create_tables
}

init_db() {
    echo "\n\n"
    python3 ./manage.py users init
}

rebuild_db() {
    recreate_db
    init_db
}

help() {
    echo ""
    echo "Usage:"
    echo ""

    echo "rebuild_db -- recreate tables & init databases"
    echo "shell -- open shell"
    echo "manage -- CLI to manage"
    echo ""
}

case "$1" in
rebuild_db)
    rebuild_db
    ;;
shell)
    python3 ./manage.py shell
    ;;
manage)
    shift
    python3 ./manage.py $*
    ;;
*)
    help
    ;;
esac
