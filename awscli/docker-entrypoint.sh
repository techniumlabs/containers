#!/bin/sh
set -e

if [[ -f "/env/variables" ]]; then
    source /env/variables
fi

if [ "${1#-}" != "$1" ]; then
    set -- aws "$@"
fi

# if our command is a valid aws subcommand, let's invoke it through aws instead
if aws "$1" help >/dev/null 2>&1
then
    set -- aws "$@"
else
    echo "= '$1' is not a aws command: assuming shell execution." 1>&2
fi

exec "$@"
