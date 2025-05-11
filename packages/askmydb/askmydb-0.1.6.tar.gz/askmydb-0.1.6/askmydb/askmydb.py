from askmydb.sql.executor import execute_sql
from askmydb.schema.loader import load_schema
from askmydb.llm.base import LLMProvider


class AskMyDB:
    def __init__(self, db_url: str, llm: LLMProvider):
        """        
        Core class for AskDB.

        Args:
            db_url (str): _database URL_.
            llm (LLMProvider): _LLM provider_.
        """
        self.db_url = db_url
        self.llm = llm
        try:
            schema = load_schema(db_url)
            self.schema = schema["text"]
            self.schema_json = schema["json"]
        except Exception as e:
            raise RuntimeError(f"AskDB.__init__ error loading schema: {e}") from e
        
    def get_schema_json(self) -> dict:
        """
        Get the schema of the database.
        Returns:
            dict: _schema_.
        """
        try:
            return self.schema_json
        except Exception as e:
            raise RuntimeError(f"AskMyDB: {e}") from e
    
    def get_schema_text(self) -> str:
        """
        Get the schema of the database.
        Returns:
            str: _schema_.
        """
        try:
            return self.schema
        except Exception as e:
            raise RuntimeError(f"AskMyDB: {e}") from e
    
    def ask(self, prompt: str) -> list[dict]:
        """
        Ask the database a question.
        Args:
            prompt (str): _question_.
        Returns:
            list[dict]: _list of answers_.
        """
        try:
            sql_query = self.llm.generate_sql(prompt,self.schema)
            # print(f"SQL Query: {sql_query}")
            results = execute_sql(sql_query, self.db_url)
            return sql_query,results
        except Exception as e:
            raise RuntimeError(f"AskMyDB: {e}") from e
