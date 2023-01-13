extern crate postgres;
extern crate config;

use postgres::{Client, NoTls};
use std::fs::File;
use std::io::prelude::*;
use config::{Config, File as ConfigFile};

fn read_config(config_file: &str) -> config::Config {
    let mut settings = Config::new();
    settings.merge(ConfigFile::with_adjustments(config_file, |config| {
        config.merge(config::File::new("config", config::FileFormat::Ini))
    })).unwrap();
    return settings;
}

fn get_databases(config: &config::Config) -> Vec<String> {
    let conn_str = format!("postgres://{}:{}@{}:{}",
        config.get_str("postgresql.user").unwrap(),
        config.get_str("postgresql.password").unwrap(),
        config.get_str("postgresql.host").unwrap(),
        config.get_int("postgresql.port").unwrap());

    let mut client = Client::connect(&conn_str, NoTls).unwrap();
    let rows = client.query("SELECT datname FROM pg_database WHERE datistemplate = false;", &[]).unwrap();
    return rows.iter().map(|row| row.get(0)).map(|s| s.to_string()).collect();
}

fn run_query(config: &config::Config, sql_file: &str, db: &str) -> (String, Vec<Vec<postgres::types::ToSql>>) {
    let conn_str = format!("postgres://{}:{}@{}:{}/{}",
        config.get_str("postgresql.user").unwrap(),
        config.get_str("postgresql.password").unwrap(),
        config.get_str("postgresql.host").unwrap(),
        config.get_int("postgresql.port").unwrap(),
        db);

    let mut client = Client::connect(&conn_str, NoTls).unwrap();
    let mut sql_file = File::open(sql_file).unwrap();
    let mut sql = String::new();
    sql_file.read_to_string(&mut sql).unwrap();
    let rows = client.query(&sql, &[]).unwrap();
    return (db.to_string(), rows);
}

fn write_output_to_file(output: Vec<(String, Vec<Vec<postgres::types::ToSql>>)>, file: &str) {
    let mut file = File::create(file).unwrap();
    for (db, rows) in output {
        file.write_all(format!("Results for {}:\n", db).as_bytes()).unwrap();
        for row in rows {
            for val in row {
                file.write_all(format!("{} ", val).as_bytes()).unwrap();
            }
            file.write_all("\n".as_bytes()).unwrap();
        }
        file.write_all("\n".as_bytes()).unwrap();
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 4 {
        println!("Usage: script config.ini query.sql output.txt");
        std::process::exit(1);
    }
    let config_file = &args[1];
    let sql_file = &args[2];
    let output_file = &args[3];
    let config = read_config(config_file);
    let databases = get_databases(&config);
    let mut output = vec![];
    for db in &databases {
        output.push(run_query(&config, sql_file, db));
    }
    write_output_to_file(output, output_file);
}

