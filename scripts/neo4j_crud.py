# Adjust the uri, user, and password variables for your Neo4j instance.
# This tool will handle basic node operations for nodes with any label and properties.
# Create a Node:
# python neo4j_crud_tool.py create Person --props name=Alice age=30
# Read Nodes:
# python neo4j_crud_tool.py read Person
# Update a Node:
# python neo4j_crud_tool.py update Person --match name=Alice --props age=31
# python neo4j_crud_tool.py update Person --match name=Alice --props age=31
# Delete a Node:
# python neo4j_crud_tool.py delete Person --match name=Alice

from neo4j import GraphDatabase
import argparse


class Neo4jCRUDTool:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_node(self, label, properties):
        with self.driver.session() as session:
            result = session.write_transaction(self._create_node, label, properties)
            print("Node created:", result)

    @staticmethod
    def _create_node(tx, label, properties):
        query = f"CREATE (n:{label} {{ {', '.join([f'{k}: ${k}' for k in properties.keys()])} }}) RETURN n"
        result = tx.run(query, **properties)
        return result.single()[0]

    def read_nodes(self, label):
        with self.driver.session() as session:
            result = session.read_transaction(self._read_nodes, label)
            for record in result:
                print(record)

    @staticmethod
    def _read_nodes(tx, label):
        query = f"MATCH (n:{label}) RETURN n"
        return list(tx.run(query))

    def update_node(self, label, match_property, update_properties):
        with self.driver.session() as session:
            result = session.write_transaction(self._update_node, label, match_property, update_properties)
            print("Updated nodes:", result)

    @staticmethod
    def _update_node(tx, label, match_property, update_properties):
        match_key, match_value = next(iter(match_property.items()))
        set_clause = ', '.join([f"n.{k} = ${k}" for k in update_properties.keys()])
        query = (
            f"MATCH (n:{label} {{{match_key}: ${match_key}}}) "
            f"SET {set_clause} "
            f"RETURN count(n)"
        )
        params = {**match_property, **update_properties}
        result = tx.run(query, **params)
        return result.single()[0]

    def delete_node(self, label, match_property):
        with self.driver.session() as session:
            result = session.write_transaction(self._delete_node, label, match_property)
            print("Deleted nodes:", result)

    @staticmethod
    def _delete_node(tx, label, match_property):
        match_key, match_value = next(iter(match_property.items()))
        query = f"MATCH (n:{label} {{{match_key}: ${match_key}}}) DETACH DELETE n RETURN count(n)"
        result = tx.run(query, **match_property)
        return result.single()[0]


def parse_arguments():
    parser = argparse.ArgumentParser(description="Neo4j CLI CRUD Tool")
    parser.add_argument("operation", choices=["create", "read", "update", "delete"], help="CRUD operation")
    parser.add_argument("label", help="Node label (e.g., Person, Product)")
    parser.add_argument("--props", nargs="+", help="Properties for creating or updating (e.g., name=Alice age=30)")
    parser.add_argument("--match", nargs="+", help="Property to match node for update/delete (e.g., name=Alice)")
    return parser.parse_args()


def parse_properties(props):
    return {k: v for prop in props for k, v in [prop.split("=")]}


def main():
    args = parse_arguments()

    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "password"  # Change to your Neo4j password

    tool = Neo4jCRUDTool(uri, user, password)

    try:
        if args.operation == "create":
            properties = parse_properties(args.props)
            tool.create_node(args.label, properties)

        elif args.operation == "read":
            tool.read_nodes(args.label)

        elif args.operation == "update":
            match_property = parse_properties(args.match)
            update_properties = parse_properties(args.props)
            tool.update_node(args.label, match_property, update_properties)

        elif args.operation == "delete":
            match_property = parse_properties(args.match)
            tool.delete_node(args.label, match_property)

    finally:
        tool.close()


if __name__ == "__main__":
    main()
