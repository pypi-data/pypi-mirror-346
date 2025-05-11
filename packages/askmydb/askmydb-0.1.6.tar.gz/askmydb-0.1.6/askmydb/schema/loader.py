import json
from sqlalchemy import create_engine, inspect

def load_schema(db_url: str) -> dict:
    """
    Load the database schema from the given URL.
    
    Args:
        db_url (str): The database URL.
    
    Returns:
        dict: {
            "text": str (formatted schema for human readability),
            "json": dict (structured schema for programmatic access)
        }
    """
    engine = create_engine(db_url)
    inspector = inspect(engine)

    schema_info = []
    json_schema = {}

    for table in inspector.get_table_names():
        schema_info.append(f"Table: {table}")
        columns = inspector.get_columns(table)
        json_schema[table] = []

        for column in columns:
            schema_info.append(f"  Column: {column['name']} - Type: {column['type']}")
            json_schema[table].append({
                "name": column["name"],
                "type": str(column["type"]),
                "nullable": column.get("nullable", True),
                "default": str(column.get("default", None))
            })

        schema_info.append("")

    return {
        "text": "\n".join(schema_info),
        "json": json_schema
    }
