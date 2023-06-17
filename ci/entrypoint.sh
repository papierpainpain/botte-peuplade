#!/bin/sh
set -e

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#! MAIN:
#!   Botte initialization.
#!
#! USAGE:
#!   ./entrypoint.sh
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

echo "## Lancement du botte dans 60 secondes"
sleep 60
echo "## Lancement du botte..."

echo ""
exec "$@"
