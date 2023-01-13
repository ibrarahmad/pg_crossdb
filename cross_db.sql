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

