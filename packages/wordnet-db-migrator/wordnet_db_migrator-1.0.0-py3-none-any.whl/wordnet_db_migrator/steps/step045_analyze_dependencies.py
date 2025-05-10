#!/usr/bin/env python3
# wordnet_db_migrator/steps/step045_analyze_dependencies.py
"""
Step 6: Analyze Dependencies

This module analyzes the dependencies between tables in the SQLite database
by extracting foreign key references from the schema. It performs a topological
sort to determine the order in which tables should be created and populated
in PostgreSQL to satisfy foreign key constraints.
"""
import json
import logging
import re
from collections import defaultdict, deque
from pathlib import Path
from typing import Dict, Set, List, Tuple, Optional, Any, DefaultDict

from ..config import config

# Set up logging
logger = logging.getLogger(__name__)

def extract_dependencies(schema_sql: str) -> DefaultDict[str, Set[str]]:
    """
    Extract table dependencies from the SQLite schema.
    
    This function parses the CREATE TABLE statements in the SQLite schema
    and extracts foreign key references to build a dependency graph.
    
    Args:
        schema_sql: The SQLite schema as a string
        
    Returns:
        DefaultDict[str, Set[str]]: A dictionary mapping table names to sets of
                                   tables they depend on (reference via foreign keys)
    """
    logger.info("Extracting table dependencies from schema")
    
    dependencies: DefaultDict[str, Set[str]] = defaultdict(set)
    
    # Find all CREATE TABLE blocks
    table_blocks = re.findall(
        r"CREATE TABLE (\w+)\s*\((.*?)\);",
        schema_sql,
        re.DOTALL | re.IGNORECASE
    )
    
    logger.debug(f"Found {len(table_blocks)} CREATE TABLE blocks")
    
    # Extract dependencies from each table
    for table_name, body in table_blocks:
        table_name = table_name.strip()
        
        # Find all REFERENCES clauses
        referenced = re.findall(r"REFERENCES\s+(\w+)", body, re.IGNORECASE)
        
        # Add referenced tables to dependencies
        dependencies[table_name].update(ref.strip() for ref in referenced)
        
        # Ensure key exists even if no dependencies
        dependencies[table_name] |= set()
        
        logger.debug(f"Table {table_name} depends on: {sorted(dependencies[table_name])}")
    
    return dependencies

def topological_sort_tolerant(graph: Dict[str, Set[str]]) -> List[str]:
    """
    Perform a topological sort on the dependency graph, tolerating cycles.
    
    This function sorts tables based on their dependencies, ensuring that
    tables are created before any tables that reference them. It handles
    circular dependencies by appending cyclic tables at the end.
    
    Args:
        graph: A dictionary mapping table names to sets of tables they depend on
        
    Returns:
        List[str]: A list of table names in dependency order
    """
    logger.info("Performing topological sort on dependency graph")
    
    # Calculate in-degree for each node
    in_degree = {node: 0 for node in graph}
    for deps in graph.values():
        for dep in deps:
            if dep in in_degree:
                in_degree[dep] += 1

    # Start with nodes that have no dependencies
    queue = deque([node for node, deg in in_degree.items() if deg == 0])
    sorted_order = []
    visited = set()

    # Process nodes in breadth-first order
    while queue:
        node = queue.popleft()
        sorted_order.append(node)
        visited.add(node)
        
        # Update in-degrees of dependent nodes
        for other in graph:
            if node in graph[other]:
                in_degree[other] -= 1
                if in_degree[other] == 0 and other not in visited:
                    queue.append(other)

    # Handle cycles by appending unvisited nodes
    unvisited = set(graph.keys()) - visited
    if unvisited:
        logger.warning(f"Circular dependency detected among tables: {sorted(unvisited)}")
        logger.info(f"Appending cyclic tables at end of order: {sorted(unvisited)}")
        sorted_order += sorted(unvisited)

    return sorted_order

def run() -> bool:
    """
    Analyze table dependencies and determine creation order.
    
    This function reads the SQLite schema, extracts table dependencies,
    performs a topological sort to determine the order in which tables
    should be created, and saves the result to a JSON file.
    
    Returns:
        bool: True if dependencies were successfully analyzed and saved,
              False if an error occurred
    """
    logger.info("Starting dependency analysis step")
    
    schema_path = config.schemas_dir / "sqlite_schema.sql"
    order_json_path = config.schemas_dir / "table_order.json"

    try:
        # Read the SQLite schema
        logger.info(f"Reading SQLite schema from {schema_path}")
        with open(schema_path, "r", encoding="utf-8") as f:
            schema_sql = f.read()

        print("✅ Extracting table dependencies...")
        
        # Extract dependencies and build graph
        graph = extract_dependencies(schema_sql)
        logger.info(f"Extracted dependencies for {len(graph)} tables")
        
        # Log the dependency graph at debug level
        for table, deps in graph.items():
            logger.debug(f"Table {table} depends on: {sorted(deps)}")

        # Perform topological sort
        logger.info("Performing topological sort")
        ordered = topological_sort_tolerant(graph)
        logger.info(f"Sorted {len(ordered)} tables in dependency order")

        # Save the table order to a JSON file
        logger.info(f"Writing table order to {order_json_path}")
        with open(order_json_path, "w", encoding="utf-8") as jf:
            json.dump({"table_order": ordered}, jf, indent=2)

        print(f"✅ Table order written to {order_json_path}")
        return True

    except Exception as error:
        logger.exception("Failed to analyze dependencies")
        print(f"❌ Failed to analyze dependencies: {error}")
        config.success = False
        return False
