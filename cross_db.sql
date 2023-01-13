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

