#!/usr/bin/env python3

import psycopg2
import configparser
import sys
import xml.etree.ElementTree as ET
import json

def read_config(config_file):
    """
    Reads the configuration file and returns the database credentials
    """
    config = configparser.ConfigParser()
    config.read(config_file)
    return {
        "host": config.get("postgresql", "host"),
        "port": config.getint("postgresql", "port"),
        "user": config.get("postgresql", "user"),
        "password": config.get("postgresql", "password")
    }

def get_databases(config):
    """
    Connects to the PostgreSQL server and returns a list of all databases
    """
    try:
        with psycopg2.connect(
            host=config["host"],
            port=config["port"],
            user=config["user"],
            password=config["password"],
            dbname="postgres"
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
                return [db[0] for db in cur.fetchall()]
    except (Exception, psycopg2.Error) as error:
        print(f"Error while connecting to PostgreSQL: {error}")
        return None

def run_query(config, sql_file, db):
    """
    Connects to the PostgreSQL server and runs the query on the specified database
    """
    try:
        with psycopg2.connect(
            host=config["host"],
            port=config["port"],
            user=config["user"],
            password=config["password"],
            dbname=db
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(open(sql_file, 'r').read())
                return (db, cur.fetchall())
    except (Exception, psycopg2.Error) as error:
        print(f"Error while connecting to PostgreSQL: {error}")

from xml.dom import minidom

def write_output_to_xml_file(output, file):
    """
    Writes the query output to the specified file in a pretty XML format.
    """
    root = ET.Element("databases")
    for (db, rows) in output:
        db_element = ET.SubElement(root, "database", name=db)
        for row in rows:
            ET.SubElement(db_element, "row").text = str(row)

    rough_string = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    with open(file, 'w') as f:
        f.write(reparsed.toprettyxml(indent="  "))

def write_output_to_json_file(output, file):
    """
    Writes the query output to the specified file in a pretty JSON format.
    """
    data = {}
    for (db, rows) in output:
        data[db] = [row for row in rows]

    with open(file, 'w') as f:
        json.dump(data, f, indent=2)

def write_output_to_file(output, file):
    """
    Writes the query output to the specified file in a more readable format
    """
    with open(file, 'w') as f:
        for (db, rows) in output:
            f.write(f'Results for {db}:\n')
            for row in rows:
                f.write(str(row) + '\n')
            f.write('\n')

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python script.py config.ini query.sql output.out [xml|json|txt]")
        sys.exit()

    if len(sys.argv) == 4:
        config_file, sql_file, output_file = sys.argv[1:]
        output_format = "xml"

    if len(sys.argv) == 5:
        config_file, sql_file, output_file, output_format = sys.argv[1:]
    
    config = read_config(config_file)
    databases = get_databases(config)
    output = []
    for db in databases:
        output.append(run_query(config, sql_file, db))
    if output_format == "txt":
        write_output_to_file(output, output_file)
    elif output_format == "xml":
        write_output_to_xml_file(output, output_file)
    elif output_format == "json":
        write_output_to_json_file(output, output_file)
