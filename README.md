# PostgreSQL Multi-DB Query Runner

This repository contains scripts that can be used to run a SQL query on all databases within a PostgreSQL server. The scripts connect to the PostgreSQL server, retrieve a list of all databases, and execute the specified SQL query on each database. The results of the query will be written to an output file in a more readable format.

## Configuration File

```bash
[postgresql]
host = <hostname>
port = <port>
user = <username>
password = <password>
```

## Usage

### Python Script
The Python script is a command line application that can be used to run a SQL query on all databases within a PostgreSQL server. The script connects to the PostgreSQL server, retrieves a list of all databases, and executes the specified SQL query on each database. The results of the query will be written to an output file in a more readable format.

#### Requirements for python
 - psycopg2 library

```bash
python cross_db.py cross_db.conf cross_db.sql cross_db.out [xml|text|json]
```

 - cross_db.conf: The configuration file containing the database credentials.
 - cross_db.sql: The SQL file containing the query to be executed on each database.
 - cross_db.out: The file to write the query output to in a more readable format.

#### Sample SQL
```sql
WITH table_sizes AS (
    SELECT
        table_schema || '.' || table_name AS table_name,
        pg_total_relation_size(table_schema || '.' || table_name) AS table_size
    FROM
        information_schema.tables
    WHERE
        table_schema NOT LIKE 'pg_%'
        AND table_schema != 'information_schema'
    ORDER BY
        table_size DESC
)
SELECT
    table_name,
    pg_size_pretty(table_size) AS pretty_size
FROM
    table_sizes
LIMIT 3;
```
#### Sample outputs in JSON
```json
{
  "postgres": [
    [
      "public.pgbench_account_postgresl",
      "4486 MB"
    ],
    [
      "public.foo",
      "346 MB"
    ],
    [
      "public.pgbench_tellers",
      "256 kB"
    ]
  ],
  "testdb": [
    [
      "public.pgbench_accounts",
      "5981 MB"
    ],
    [
      "public.test_tb",
      "422 MB"
    ],
    [
      "public.pgbench_tellers",
      "312 kB"
    ]
  ]
}
```

#### Sample SQL
```sql
SELECT 
    pg_stat_get_db_numbackends(oid) AS "connections", 
    pg_stat_get_db_xact_commit(oid) AS "commits", 
    pg_stat_get_db_xact_rollback(oid) AS "rollbacks", 
    pg_stat_get_db_blocks_fetched(oid) AS "blocks_fetched", 
    pg_stat_get_db_blocks_hit(oid) AS "blocks_hit", 
    pg_stat_get_db_tuples_returned(oid) AS "tuples_returned", 
    pg_stat_get_db_tuples_fetched(oid) AS "tuples_fetched", 
    pg_stat_get_db_tuples_inserted(oid) AS "tuples_inserted", 
    pg_stat_get_db_tuples_updated(oid) AS "tuples_updated", 
    pg_stat_get_db_tuples_deleted(oid) AS "tuples_deleted", 
    pg_stat_get_db_deadlocks(oid) AS "deadlocks" 
FROM pg_database; 
```
#### Sample outputs in XML

```xml
<?xml version="1.0" ?>
<databases>
  <database name="postgres">
    <columns>
      <column>connections</column>
      <column>commits</column>
      <column>rollbacks</column>
      <column>blocks_fetched</column>
      <column>blocks_hit</column>
      <column>tuples_returned</column>
      <column>tuples_fetched</column>
      <column>tuples_inserted</column>
      <column>tuples_updated</column>
      <column>tuples_deleted</column>
      <column>deadlocks</column>
    </columns>
    <row>(1, 11173, 65, 11744073, 10639318, 33910547, 130205, 40004003, 97, 396, 0)</row>
    <row>(0, 2581, 16, 11851686, 10376734, 41038722, 38563, 50004693, 414, 15, 0)</row>
    <row>(0, 9516, 0, 402756, 400992, 3845733, 90321, 16227, 743, 34, 0)</row>
    <row>(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)</row>
    <row>(0, 2310, 8, 1163983, 151786, 31012319, 30716, 30003535, 6, 0, 0)</row>
  </database>
  <database name="testdb">
    <columns>
      <column>connections</column>
      <column>commits</column>
      <column>rollbacks</column>
      <column>blocks_fetched</column>
      <column>blocks_hit</column>
      <column>tuples_returned</column>
      <column>tuples_fetched</column>
      <column>tuples_inserted</column>
      <column>tuples_updated</column>
      <column>tuples_deleted</column>
      <column>deadlocks</column>
    </columns>
    <row>(0, 11174, 65, 11744197, 10639442, 33910587, 130245, 40004003, 97, 396, 0)</row>
    <row>(1, 2582, 16, 11851717, 10376765, 41038737, 38577, 50004693, 414, 15, 0)</row>
    <row>(0, 9516, 0, 402756, 400992, 3845733, 90321, 16227, 743, 34, 0)</row>
    <row>(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)</row>
    <row>(0, 2310, 8, 1163983, 151786, 31012319, 30716, 30003535, 6, 0, 0)</row>
  </database>
</databases>
```

### RUST Script
The Rust script is a command line application that can be used to run a SQL query on all databases within a PostgreSQL server. The script connects to the PostgreSQL server, retrieves a list of all databases, and executes the specified SQL query on each database. The results of the query will be written to an output file in a more readable format.

```bash
- cargo run -- main.rs cross_db.conf cross_db.sql cross_db.out
```

 - cross_db.conf: The configuration file containing the database credentials.
 - cross_db.sql: The SQL file containing the query to be executed on each database.
 - cross_db.out: The file to write the query output to in a more readable format.


#### Requirements for RUST
 - Rust 1.51.0 or higher
 - postgres crate
 - config crate
