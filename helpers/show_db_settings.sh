#!/bin/sh

docker compose exec -T db psql -U user -d demo_db -c 'SHOW ALL;' | grep -E 'max_connections|idle_in_transaction_session_timeout|statement_timeout' | awk -F'|' '
BEGIN {
    print "Setting Name                           | Value";
    print "---------------------------------------+----------------------------------";
}
{
    # Trim whitespace from the first two fields and print
    printf "% -38s | % -32s\n", substr(trim($1), 1, 38), substr(trim($2), 1, 32);
}

function trim(s) {
    sub(/^[ \t\r\n]+/, "", s);
    sub(/[ \t\r\n]+$/, "", s);
    return s;
}'
