import sqlite3
import uuid
import pandas as pd
from enum import Enum
import logging
import sys

# Creating an object
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.ERROR  )

if logger.hasHandlers():
    logger.handlers.clear()
    # print("Cleared existing log handlers.")
console_handler = logging.StreamHandler(stream=sys.__stderr__)
logger.addHandler(console_handler)

# logging.debug("This is a debug message (will not show if level is INFO).")
# logging.info("This is an info message.")
# logging.warning("This is a warning message.")
# logging.error("This is an error message.")
# logging.critical("This is a critical message.")


class QuaryCriteria(Enum):
  none = -1
  equals = 0
  starts_with = 1
  ends_with = 2
  contains = 3
  greater_than = 4
  less_than = 5
  greater_than_equal = 6
  less_than_equal = 7
  between = 8
  not_between = 9
  in_list = 10
  not_in_list = 11
  is_null = 12
  is_not_null = 13

class QuaryOutFormat(Enum):
    defulat = 0,
    list = 1,
    dict = 2,
    df = 4,
    formated_text = 5
    
class SqliteTools:
    
    def __init__(self, db_name):
        try:
            if db_name == None:
                raise ValueError("Database name cannot be None.")
            elif not isinstance(db_name, str):
                raise ValueError("Database name must be a string.")
            elif len(db_name) == 0:
                raise ValueError("Database name cannot be an empty string.")
            # Ensure the database name ends with .db
            elif not db_name.lower().endswith(".db"):
                self.db_name = db_name + ".db"
            else:
                self.db_name = db_name
            logger.info(f"Initialized sqlite_tools for database: {self.db_name}")
        except ValueError as ve:
            logger.error(f"Error initializing sqlite_tools: {ve}")
            #raise
        except Exception as e:
            logger.error(f"Unexpected error initializing sqlite_tools: {e}")
            #raise

    def create_db(self):
        """Initializes the database file and logs the SQLite version."""
        sqliteConnection = None
        cursor = None
        try:
            # connect() creates the file if it doesn't exist
            sqliteConnection = sqlite3.connect(self.db_name)
            cursor = sqliteConnection.cursor()
            logger.info(f"Database '{self.db_name}' initialized or connected.")
            query = 'select sqlite_version();'
            cursor.execute(query)
            result = cursor.fetchone() # Use fetchone for single result
            logger.info('SQLite Version is {}'.format(result[0]))
            cursor.close()
        except sqlite3.Error as error:
            logger.error('%s raised an error during DB init: %s', __name__, str(error))
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                logger.info('SQLite Connection closed after DB init.')

    def connect_db(self):
        """Establishes connection to the SQLite database and enables foreign keys."""
        conn = None # Initialize conn to None
        try:
            conn = sqlite3.connect(self.db_name)
            # Use Row factory for dictionary-like access to rows
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            # Enable foreign key constraint enforcement for this connection
            cursor.execute("PRAGMA foreign_keys = ON;")
            logger.debug(f"Connected to DB '{self.db_name}' and enabled foreign keys.")
            return conn, cursor
        except sqlite3.Error as error:
            logger.error(f"Failed to connect to database '{self.db_name}': {error}")
            if conn:
                conn.close() # Ensure connection is closed on error
            raise # Re-raise the exception so the caller knows connection failed

    def create_table(self,
                     table_name: str,
                     columns: dict,
                     foreign_key_column: str = None,
                     ref_table: str = None,
                     ref_column: str = None):
        """
        Create a table in an SQLite database, automatically adding an 'id'
        primary key if none is specified, and optionally adding a foreign key.

        :param table_name: Name of the table to create.
        :param columns: Dictionary of column names and their data types
                        (e.g., {'name': 'TEXT NOT NULL', 'age': 'INTEGER'}).
                        If a column definition includes 'PRIMARY KEY', the
                        automatic 'id' column will NOT be added.
        :param foreign_key_column: Name of the column in this table to be the foreign key.
        :param ref_table: Name of the table the foreign key references.
        :param ref_column: Name of the column in the referenced table (usually its PK).

       ### Example Usage:

        db_tool = sqlite_tools("my_company_data") # Creates/Connects to my_company_data.db
        db_tool.create_db() # Optional: Just ensures connection works and logs version

        ### Example 1: Simple table, auto ID
        users_columns = {
            'username': 'TEXT UNIQUE NOT NULL',
            'email': 'TEXT',
            'signup_date': 'DATE'
        }
        db_tool.create_table('users', users_columns)

        ### Example 2: Table with explicit primary key
        products_columns = {
            'sku': 'TEXT PRIMARY KEY',
            'name': 'TEXT NOT NULL',
            'price': 'REAL CHECK(price > 0)' # Added a check constraint
        }
        db_tool.create_table('products', products_columns)

        ### Example 3: Table with foreign key (referencing the auto 'id' from 'users')
        orders_columns = {
            'user_id': 'INTEGER NOT NULL', # This will be the foreign key column
            'order_date': 'DATETIME DEFAULT CURRENT_TIMESTAMP',
            'total_amount': 'REAL'
        }
        db_tool.create_table('orders',
                             orders_columns,
                             foreign_key_column='user_id',
                             ref_table='users',
                             ref_column='id') # References the auto-generated 'id' in users

        ### Example 4: Table with foreign key referencing an explicit PK ('sku' from 'products')
        order_items_columns = {
            'order_id': 'INTEGER NOT NULL', # FK to orders table
            'product_sku': 'TEXT NOT NULL', # FK to products table
            'quantity': 'INTEGER DEFAULT 1',
            'item_price': 'REAL'
            # Could add a composite PK here if needed: 'PRIMARY KEY (order_id, product_sku)'
        }
        ### Add FK for order_id
        db_tool.create_table('order_items',
                             order_items_columns,
                             foreign_key_column='order_id',
                             ref_table='orders',
                             ref_column='id')
        ### Note: Adding multiple FKs requires modifying the create_table or using ALTER TABLE later.
        This example only adds one FK. For multiple, you'd need a more complex function
        or separate ALTER TABLE statements.

        ### Example 5: Incomplete FK info (will log warning, create table without FK)
        test_columns = {'data': 'TEXT'}
        db_tool.create_table('test_incomplete_fk', test_columns, foreign_key_column='data', ref_table='users')

        ### Example 6: FK column not in definition (will log error and raise ValueError)
        try:
            db_tool.create_table('test_bad_fk_col', test_columns, foreign_key_column='bad_column', ref_table='users', ref_column='id')
        except ValueError as e:
            print(f"Caught expected error: {e}")
        """
        sqliteConnection = None
        cursor = None
        try:
            sqliteConnection, cursor = self.connect_db()

            column_definitions = []
            primary_key_defined = False

            # Check if a primary key is already defined in the input columns
            for dtype in columns.values():
                # Case-insensitive check for "PRIMARY KEY"
                if 'PRIMARY KEY' in dtype.upper():
                    primary_key_defined = True
                    logger.debug(f"Primary key found in provided columns for '{table_name}'.")
                    break

            # Add automatic ID primary key if none was defined
            if not primary_key_defined:
                column_definitions.append("id INTEGER PRIMARY KEY AUTOINCREMENT")
                logger.info(f"No PRIMARY KEY found in columns for '{table_name}', adding 'id INTEGER PRIMARY KEY AUTOINCREMENT'.")

            # Add user-defined columns (quoting names for safety)
            for col, dtype in columns.items():
                column_definitions.append(f'"{col}" {dtype}')

            # --- Foreign Key Handling ---
            foreign_key_clause = ""
            # Check if all necessary foreign key parts are provided
            if foreign_key_column and ref_table and ref_column:
                # Check if the foreign key column exists in the provided columns dict keys
                if foreign_key_column not in columns:
                    logger.error(f"Foreign key column '{foreign_key_column}' not found in the provided columns keys {list(columns.keys())} for table '{table_name}'. Table creation aborted.")
                    # Raise an error or return to prevent table creation with invalid FK
                    raise ValueError(f"Foreign key column '{foreign_key_column}' not defined in columns.")

                # Construct the foreign key clause (quoting names for safety)
                # Added ON UPDATE CASCADE ON DELETE CASCADE as a common default
                foreign_key_clause = f', FOREIGN KEY("{foreign_key_column}") REFERENCES "{ref_table}"("{ref_column}") ON UPDATE CASCADE ON DELETE CASCADE'
                logger.info(f"Adding FOREIGN KEY constraint for '{table_name}': ('{foreign_key_column}') referencing '{ref_table}'('{ref_column}').")
            elif any([foreign_key_column, ref_table, ref_column]):
                # Log a warning if foreign key details are incomplete but some were provided
                logger.warning(f"Incomplete foreign key information provided for table '{table_name}'. "
                               "All of 'foreign_key_column', 'ref_table', and 'ref_column' must be specified to add a constraint. Proceeding without foreign key.")

            # --- Construct Final SQL ---
            columns_def_str = ', '.join(column_definitions)
            # Quote table name for safety as well
            create_table_sql = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns_def_str}{foreign_key_clause});'

            logger.debug(f"Executing SQL: {create_table_sql}")
            cursor.execute(create_table_sql)
            sqliteConnection.commit()

            logger.info(f"Table '{table_name}' checked/created successfully in database '{self.db_name}'.")

        except sqlite3.Error as error:
            logger.error(f"SQLite error creating table '{table_name}': {error}")
            if sqliteConnection:
                sqliteConnection.rollback() # Rollback on error
        except ValueError as ve: # Catch specific ValueError from FK check
             logger.error(f"Configuration error creating table '{table_name}': {ve}")
             # No need to rollback if error is before execute
        except Exception as e:
             logger.error(f"An unexpected error occurred creating table '{table_name}': {e}")
             if sqliteConnection:
                sqliteConnection.rollback()
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                logger.info(f"SQLite Connection closed after create_table attempt on '{table_name}'.")

    def check_table_if_exists(self ,table_name):
        conn, cursor = self.connect_db()
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"    
        query1 = f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{table_name}'" 
        try:
            cursor.execute(query1)
            details = cursor.rowcount 
        except sqlite3.Error as e:
            print(f"Error fetching item details: {e}")
        finally:
            conn.close()
        return details > 0
    
    def fill_table(self, table_name, df):
        """Fills (replaces) a table with data from a Pandas DataFrame."""
        sqliteConnection = None
        try:
            sqliteConnection, cursor = self.connect_db()
            df.to_sql(table_name, sqliteConnection, if_exists='replace', index=False)
            logger.info(f"Table '{table_name}' replaced with data from DataFrame.")
        except sqlite3.Error as error:
            logger.error(f"Error replacing table '{table_name}' from DataFrame: {error}")
            if sqliteConnection:
                sqliteConnection.rollback()
        except Exception as e:
            logger.error(f"Unexpected error filling table '{table_name}': {e}")
            if sqliteConnection:
                sqliteConnection.rollback()
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                logger.info(f"SQLite Connection closed after fill_table attempt on '{table_name}'.")

    def read_table(self, 
                    table_name:str, 
                    quary_column:str = '',
                    quary_value ='',
                    quary_criteria : QuaryCriteria = QuaryCriteria.none,
                    out_format = QuaryOutFormat.defulat,
                    ) -> pd.DataFrame|list[dict]|list[list]|list[tuple]|None:
        """
        read a table in an SQLite database.

        :param table_name: Name of the table.
        :param quary_criteria : 
        :param quary_column : 
        :param quary_value : 

        """
        try:
            result_table = []
            sqliteConnection,cursor = self.connect_db()
            # Use Row factory for dictionary-like access to rows
            sqliteConnection.row_factory = sqlite3.Row
            cursor = sqliteConnection.cursor()
            statement = f"SELECT * FROM {table_name}"
            if quary_criteria == QuaryCriteria.equals:
                statement = f"SELECT * FROM {table_name} WHERE {quary_column} = '{quary_value}'"
            elif quary_criteria == QuaryCriteria.starts_with:
                statement = f"SELECT * FROM {table_name} WHERE {quary_column} LIKE '{quary_value}%'"
            elif quary_criteria == QuaryCriteria.ends_with:
                statement = f"SELECT * FROM {table_name} WHERE {quary_column} LIKE '%{quary_value}'"
            elif quary_criteria == QuaryCriteria.contains:
                statement = f"SELECT * FROM {table_name} WHERE {quary_column} LIKE '%{quary_value}%'"
            else:
                statement = f"SELECT * FROM {table_name}"
                
            cursor.execute(statement)
            result_table = cursor.fetchall()
            if(len(result_table) == 0):
                return pd.DataFrame()
            sqliteConnection.commit() 
            sqliteConnection.close()
            if out_format == QuaryOutFormat.df:
                result = pd.DataFrame(result_table)
                result.columns = [desc[0] for desc in cursor.description]
                return result
            if out_format == QuaryOutFormat.dict:
                result = [dict(row) for row in result_table]
                return result
            if out_format == QuaryOutFormat.list:
                result = [list(row) for row in result_table]
                return result
            if (out_format == QuaryOutFormat.formated_text):
                if(table_name == 'contracts'):
                    result = [ (f"{row['contract_no']} {row['description']}" ,row['id'] ) for row in result_table]
                elif(table_name == 'vendor_list'):
                    result = [ (row['Description'] ,row['id'] ) for row in result_table]
                return result
            else:
                return result_table
        except sqlite3.Error as error:
            logging.error('%s raised an error:%s', __name__,str(error) )
        
        # Close DB Connection irrespective of success
        # or failure
        finally:
        
            if sqliteConnection:
                sqliteConnection.close()
                logging.info('SQLite Connection closed')

    def get_item_by_id(self,table_name:str,table_id):
        """Fetches full details for a specific item ID."""
        conn, cursor = self.connect_db()
        details = None
        try:
            cursor.execute(f"SELECT * FROM {table_name} WHERE id = ?", (table_id,))
            details = cursor.fetchone() # Returns a Row object or None
        except sqlite3.Error as e:
            print(f"Error fetching item details: {e}")
        finally:
            conn.close()
        return details

    def get_items_by_quary(self,
                          table_name:str,
                          quary_column:str='',
                          quary_value='',
                          quary_criteria : QuaryCriteria = QuaryCriteria.equals):
        """Fetches full details for a specific item ID."""
        conn, cursor = self.connect_db()
        details = None
        try:
            statement = ""
            if quary_criteria == QuaryCriteria.equals:
                statement = f"SELECT * FROM  {table_name}  WHERE {quary_column} = '{quary_value}'"
            elif quary_criteria == QuaryCriteria.starts_with:
                statement = f"SELECT * FROM  {table_name}  WHERE {quary_column} LIKE '{quary_value}%'"
            elif quary_criteria == QuaryCriteria.ends_with:
                statement = f"SELECT * FROM  {table_name}  WHERE {quary_column} LIKE '%{quary_value}'"
            elif quary_criteria == QuaryCriteria.contains:
                statement = f"SELECT * FROM  {table_name} WHERE {quary_column} LIKE '%{quary_value}%'"
            else:
                statement = f"SELECT * FROM  {table_name}"      

            cursor.execute(statement)
            details = cursor.fetchmany() # Returns a Row object or None
        except sqlite3.Error as e:
            print(f"Error fetching item details: {e}")
        finally:
            conn.close()
        return details

    def upsert_row(self, table_name: str, row_data: dict, primary_key_columns: list[str] = ['id']):
        """
        Updates or inserts a single row from a dictionary into an SQLite table.
        Handles auto-incrementing primary keys and foreign key constraints.
        Uses UPSERT (ON CONFLICT DO UPDATE) if SQLite >= 3.24.0,
        otherwise falls back to INSERT OR REPLACE (use with caution).

        Args:
            table_name (str): The name of the target table.
            row_data (dict): A dictionary where keys are column names and values
                             are the data for the row to upsert.
                             **For child tables, ensure foreign key columns and their
                             corresponding parent ID values are included in this dict.**
            primary_key_columns (list[str]): A list of column names that form the
                                             primary key of the target table.
                                             Assumes the first one might be auto-incrementing
                                             if not provided in row_data.

        Returns:
            tuple[bool, Optional[int]]: A tuple containing:
                - bool: True if the operation was successful, False otherwise.
                - Optional[int]: The ID of the inserted/updated row (based on the
                                 first primary key column), or None on failure.

        Example Usage:
            db = sqlite_tools("my_db")
            Assume 'users' table with PK 'id'
            Assume 'orders' table with PK 'id' and FK 'user_id' referencing users(id)

            Insert parent
            success, user_id = db.upsert_row('users', {'username': 'alice', 'email': 'a@e.com'})

            Update parent
            success, user_id = db.upsert_row('users', {'id': 1, 'email': 'alice_new@e.com'})

            Insert child (provide the foreign key 'user_id')
            success, order_id = db.upsert_row('orders', {'user_id': 1, 'order_date': '2024-01-01', 'total': 50.0})

            Update child
            success, order_id = db.upsert_row('orders', {'id': 5, 'total': 55.0})

            Insert child with invalid parent ID (will fail if user_id 999 doesn't exist)
            success, order_id = db.upsert_row('orders', {'user_id': 999, 'order_date': '2024-01-02', 'total': 20.0})
            -> success will be False, IntegrityError logged.
        """
        if not primary_key_columns:
            logger.error(f"Error upserting to '{table_name}': primary_key_columns list cannot be empty.")
            return False, None
        if not row_data:
            logger.error(f"Error upserting to '{table_name}': row_data dictionary cannot be empty.")
            return False, None

        # Assume the first PK column might be the auto-increment one
        pk_col = primary_key_columns[0]
        # Check if the primary key is provided and has a value (not None)
        is_update_intent = pk_col in row_data and row_data[pk_col] is not None

        sqliteConnection = None
        cursor = None
        success = False
        returned_id = None

        try:
            sqliteConnection, cursor = self.connect_db()

            # --- Check SQLite Version ---
            supports_upsert = sqlite3.sqlite_version_info >= (3, 24, 0)
            if not supports_upsert and is_update_intent: # Only warn if fallback is needed
                logger.warning(f"SQLite version {sqlite3.sqlite_version} < 3.24.0. "
                                f"Falling back to INSERT OR REPLACE for single row in '{table_name}'. "
                                "Note potential side effects with triggers/foreign keys.")
            # --------------------------

            columns = list(row_data.keys()) # Use list for consistent order
            cols_str = ", ".join(f'"{col}"' for col in columns)
            placeholders = ", ".join("?" for _ in columns)
            # Ensure values are in the same order as columns
            values_tuple = tuple(row_data[col] for col in columns)
            pk_cols_str = ", ".join(f'"{col}"' for col in primary_key_columns)

            if is_update_intent:
                # --- UPDATE or INSERT with specific ID ---
                logger.info(f"Attempting UPSERT (update intent) for row in '{table_name}' with PK {pk_col}={row_data.get(pk_col)}.")

                # Ensure all PKs are present if it's a composite key scenario
                if not all(col in row_data for col in primary_key_columns):
                    logger.error(f"Error upserting to '{table_name}': For update intent, all primary key columns "
                                f"{primary_key_columns} must be in row_data keys {list(row_data.keys())}.")
                    return False, None

                if supports_upsert:
                    # Exclude primary keys from the SET clause
                    update_set_clause = ", ".join(f'"{col}" = excluded."{col}"'
                                                  for col in columns if col not in primary_key_columns)
                    if not update_set_clause:
                         # If only PKs are provided, ON CONFLICT DO NOTHING is appropriate
                         upsert_sql = f"""
                            INSERT INTO "{table_name}" ({cols_str})
                            VALUES ({placeholders})
                            ON CONFLICT({pk_cols_str}) DO NOTHING;
                         """
                         logger.warning(f"Upserting row to '{table_name}': No non-primary-key columns found to update. Will insert if not exists.")
                    else:
                        upsert_sql = f"""
                            INSERT INTO "{table_name}" ({cols_str})
                            VALUES ({placeholders})
                            ON CONFLICT({pk_cols_str})
                            DO UPDATE SET {update_set_clause};
                        """
                    action_verb = "Upserting row (ON CONFLICT DO UPDATE)"
                else: # Fallback to INSERT OR REPLACE
                    upsert_sql = f"""
                        INSERT OR REPLACE INTO "{table_name}" ({cols_str})
                        VALUES ({placeholders});
                    """
                    action_verb = "Upserting row (INSERT OR REPLACE)"

                logger.debug(f"Executing SQL: {upsert_sql} with values {values_tuple}")
                cursor.execute(upsert_sql, values_tuple)
                returned_id = row_data[pk_col] # The ID was provided
            else:
                # --- INSERT new row (potentially with AUTOINCREMENT PK) ---
                logger.info(f"Attempting INSERT for new row in '{table_name}'.")

                # Prepare data for insertion (exclude the PK column *if* it was in row_data but None)
                insert_data = {k: v for k, v in row_data.items() if not (k == pk_col and v is None)}

                if not insert_data:
                     logger.error(f"Error inserting into '{table_name}': No data provided or only null PK provided.")
                     return False, None

                columns = list(insert_data.keys()) # Use list for consistent order
                cols_str = ", ".join(f'"{col}"' for col in columns)
                placeholders = ", ".join("?" for _ in columns)
                # Ensure values are in the same order as columns
                values_tuple = tuple(insert_data[col] for col in columns)

                insert_sql = f'INSERT INTO "{table_name}" ({cols_str}) VALUES ({placeholders})'
                action_verb = "Inserting new row"

                logger.debug(f"Executing SQL: {insert_sql} with values {values_tuple}")
                cursor.execute(insert_sql, values_tuple)
                # Get the auto-generated ID if applicable, otherwise use provided PK if it was in insert_data
                returned_id = cursor.lastrowid if pk_col not in insert_data else insert_data[pk_col]


            # Commit transaction if execution was successful up to this point
            sqliteConnection.commit()
            logger.info(f"{action_verb} completed successfully for table '{table_name}'. {cursor.rowcount} row(s) affected. ID: {returned_id}")
            success = True

        except sqlite3.IntegrityError as ie:
            # Specific handling for constraint violations (like Foreign Key)
            logger.error(f"SQLite Integrity Error during upsert/insert row to '{table_name}': {ie}. Check foreign key constraints and unique constraints.")
            if sqliteConnection:
                sqliteConnection.rollback()
        except sqlite3.Error as error:
            logger.error(f"SQLite error during upsert/insert row to '{table_name}': {error}")
            if sqliteConnection:
                sqliteConnection.rollback()
        except Exception as e:
            logger.error(f"An unexpected error occurred during upsert/insert row to '{table_name}': {e}")
            if sqliteConnection:
                sqliteConnection.rollback()
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                logger.info(f'SQLite Connection closed after upsert/insert attempt on {table_name}')

        return success, returned_id

    def update_table(self, 
                   table_name:str, 
                   update_column:str,
                   update_value,
                   quary_column:str='',
                   quary_value='',
                   quary_criteria : QuaryCriteria = QuaryCriteria.equals,
                   ):
        """
        update a table in an SQLite database.

        :param table_name: Name of the table.
        :param quary_criteria : 
        :param quary_column : 
        :param quary_value : 

        """
        try:
            sqliteConnection, cursor = self.connect_db()
            statement = f"SELECT * FROM {table_name}"
            if quary_criteria == QuaryCriteria.equals:
                statement = f"UPDATE {table_name} SET {update_column} = '{update_value}' WHERE {quary_column} = '{quary_value}'"
            elif quary_criteria == QuaryCriteria.starts_with:
                statement = f"UPDATE {table_name} SET {update_column} = '{update_value}' WHERE {quary_column} LIKE '{quary_value}%'"
            elif quary_criteria == QuaryCriteria.ends_with:
                statement = f"UPDATE {table_name} SET {update_column} = '{update_value}' WHERE {quary_column} LIKE '%{quary_value}'"
            elif quary_criteria == QuaryCriteria.contains:
                statement = f"UPDATE {table_name} SET {update_column} = '{update_value}' WHERE {quary_column} LIKE '%{quary_value}%'"
            else:
                statement = f"UPDATE {table_name} SET {update_column} = '{update_value}'"      

            cursor.execute(statement)
            sqliteConnection.commit() 
            sqliteConnection.close()
            logger.info('update successfull')
        except sqlite3.Error as error:
            logger.error('%s raised an error:%s', __name__,str(error) )
        
        # Close DB Connection irrespective of success
        # or failure
        finally:
        
            if sqliteConnection:
                sqliteConnection.close()
                logger.info('SQLite Connection closed')

    def upsert_table_using_df(self, table_name: str, df: pd.DataFrame, primary_key_columns: list[str] = ['id']):
        """
        Updates or inserts rows from a DataFrame into an existing SQLite table
        without losing the table's schema. Relies on Primary Key(s).
        Uses UPSERT (ON CONFLICT DO UPDATE) if SQLite >= 3.24.0,
        otherwise falls back to INSERT OR REPLACE.

        Args:
            table_name (str): The name of the target table.
            df (pd.DataFrame): The DataFrame containing data to upsert.
            primary_key_columns (list[str]): A list of column names that form the
                                             primary key of the target table.
        """
        if not primary_key_columns:
            logger.error(f"Error upserting to '{table_name}': primary_key_columns list cannot be empty.")
            return

        if not all(col in df.columns for col in primary_key_columns):
             logger.error(f"Error upserting to '{table_name}': One or more primary key columns "
                           f"{primary_key_columns} not found in DataFrame columns {list(df.columns)}.")
             return

        sqliteConnection = None
        cursor = None
        temp_table_name = f"_temp_{table_name}_{uuid.uuid4().hex[:8]}"

        # --- Check SQLite Version ---
        # sqlite_version_info is a tuple like (3, 30, 1)
        supports_upsert = sqlite3.sqlite_version_info >= (3, 24, 0)
        if not supports_upsert:
            logger.warning(f"SQLite version {sqlite3.sqlite_version} < 3.24.0. "
                            f"Falling back to INSERT OR REPLACE for table '{table_name}'. "
                            "Note potential side effects with triggers/foreign keys.")
        # --------------------------

        try:
            sqliteConnection,cursor = self.connect_db(self.db_name)

            # 1. Insert DataFrame data into a temporary table
            df.to_sql(temp_table_name, sqliteConnection, if_exists='replace', index=False)
            logger.info(f"DataFrame data loaded into temporary table '{temp_table_name}'.")

            # 2. Get column names
            df_columns = df.columns.tolist()
            cols_str = ", ".join(f'"{col}"' for col in df_columns)
            pk_cols_str = ", ".join(f'"{col}"' for col in primary_key_columns)

            # 3. Construct the appropriate SQL statement based on version
            if supports_upsert:
                update_set_clause = ", ".join(f'"{col}" = excluded."{col}"'
                                              for col in df_columns if col not in primary_key_columns)
            if supports_upsert:
                update_set_clause = ", ".join(f'"{col}" = excluded."{col}"'
                                              for col in df_columns if col not in primary_key_columns)
                if not update_set_clause:
                     upsert_sql = f"""
                        INSERT INTO "{table_name}" ({cols_str})
                        SELECT {cols_str} FROM "{temp_table_name}" WHERE True
                        ON CONFLICT({pk_cols_str}) DO NOTHING;
                     """
                     logging.warning(f"Upserting to '{table_name}': No non-primary-key columns found to update.")
                else:
                    upsert_sql = f"""
                        INSERT INTO "{table_name}" ({cols_str})
                        SELECT {cols_str} FROM "{temp_table_name}" WHERE True
                        ON CONFLICT({pk_cols_str})
                        DO UPDATE SET {update_set_clause};
                    """
                action_verb = "Upserting (ON CONFLICT DO UPDATE)"
            else:
                # Fallback for older SQLite versions
                upsert_sql = f""" 
                    INSERT OR REPLACE INTO "{table_name}" ({cols_str}) 
                    SELECT {cols_str} FROM "{temp_table_name} WHERE True";
                """
                action_verb = "Upserting (INSERT OR REPLACE)"


            # logging.debug(f"Executing SQL: {upsert_sql}") # Uncomment for debugging SQL
            logger.info(f"{action_verb} from '{temp_table_name}' to '{table_name}'.")
            logger.debug(f"Attempting to execute SQL: ---START---\n{upsert_sql}\n---END---") 
            cursor.execute(upsert_sql) # This is approx line 313
            sqliteConnection.commit()
            logger.info(f"Upsert completed successfully for table '{table_name}'. {cursor.rowcount} rows affected.")

        except sqlite3.Error as error:
            logger.error(f"SQLite error during upsert to '{table_name}': {error}")
            if sqliteConnection:
                sqliteConnection.rollback()
        except Exception as e:
            logger.error(f"An unexpected error occurred during upsert to '{table_name}': {e}")
            if sqliteConnection:
                sqliteConnection.rollback()
        finally:
            # Cleanup
            if cursor and sqliteConnection:
                try:
                    cursor.execute(f'DROP TABLE IF EXISTS "{temp_table_name}";')
                    sqliteConnection.commit()
                    logger.info(f"Temporary table '{temp_table_name}' dropped.")
                except sqlite3.Error as drop_error:
                     logger.error(f"Error dropping temporary table '{temp_table_name}': {drop_error}")
            if sqliteConnection:
                sqliteConnection.close()
                logger.info('SQLite Connection closed')
    
    # def update_table_using_df(self,table_name:str,df:pd.DataFrame):
    #     try:
    #         sqliteConnection = sqlite3.connect(self.db_name)
    #         df.to_sql(table_name, sqliteConnection, if_exists='replace', index=False)  # 'replace' overwrites the table
    #         # df.to_sql(table_name, conn, if_exists='append', index=False) # 'append' adds to the table
    #         # df.to_sql(table_name, conn, if_exists='fail', index=False) # 'fail' raises error if table exists
    #     except Exception as e:
    #         print(f"Error writing to table: {e}")
    #     finally:
    #         if sqliteConnection:
    #             sqliteConnection.close()
    #             logger.info('SQLite Connection closed')    
    
    # def add_to_table_using_df(self,table_name:str,df:pd.DataFrame):
    #     try:
    #         sqliteConnection = sqlite3.connect(self.db_name)
    #         df.to_sql(table_name, sqliteConnection, if_exists='append', index=False)  # 'replace' overwrites the table
    #     except Exception as e:
    #         print(f"Error writing to table: {e}")
    #     finally:
    #         if sqliteConnection:
    #             sqliteConnection.close()
    #             print('SQLite Connection closed')  
    
    def delete_from_table_by_id(self,table_name:str,id:int) :
        """
        Deletes a record from the specified table by its ID.

        Args:
            table_name (str): Name of the table from which to delete the record.
            id (int): ID of the record to delete.

        Returns:
            bool: True if the record was deleted successfully, False otherwise.
        """
        try:
            sqliteConnection, cursor = self.connect_db()
            cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (id,))
            if cursor.rowcount > 0:
                sqliteConnection.commit()
                print(f"Record with ID {id} deleted successfully.")
                return True
            else:
                return False
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return False
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                logger.debug('SQLite Connection closed')       

    def delete_from_table(self,
                          table_name:str, 
                            quary_column:str = '',
                            quary_value ='',
                            quary_criteria : QuaryCriteria = QuaryCriteria.equals,):
        try:
            sqliteConnection,cursor = self.connect_db(self.db_name)
            if quary_criteria == QuaryCriteria.equals:
                statement = f"DELETE FROM {table_name} WHERE {quary_column} = {quary_value}"
            elif quary_criteria == QuaryCriteria.greater_than:
                statement = f"DELETE  {table_name} WHERE {quary_column} > {quary_value}"
            elif quary_criteria == QuaryCriteria.less_than:
                statement = f"DELETE  {table_name} WHERE {quary_column} < {quary_value}"
            elif quary_criteria == QuaryCriteria.starts_with:
                statement = f"DELETE  {table_name} WHERE {quary_column} LIKE '{quary_value}%'"
            elif quary_criteria == QuaryCriteria.ends_with:
                statement = f"DELETE  {table_name} WHERE {quary_column} LIKE '%{quary_value}'"
            elif quary_criteria == QuaryCriteria.contains:
                statement = f"DELETE  {table_name} WHERE {quary_column} LIKE '%{quary_value}%'"

            elif quary_criteria == QuaryCriteria.none:
                statement = f"DELETE  {table_name}"

            cursor.execute(statement)
            sqliteConnection.commit() 
            sqliteConnection.close()
            logger.debug('delete successfull')
            return True    
        except sqlite3.Error as error:
            print('Error occurred - ', error)
            return False 
        # Close DB Connection irrespective of success
        # or failure
        finally:
        
            if sqliteConnection:
                sqliteConnection.close()
                logger.debug('SQLite Connection closed')                


# db = SqliteTools("titan")
# db.connect_db()
# print('db connected...')
# ---------- addd table--------------    

# table_columns = {
#     'contract_id': 'INTEGER NOT NULL',
#     'description': 'TEXT NOT NULL',
#     'unit': 'TEXT DEFAULT EA',
#     'quantity': 'REAL DEFAULT 0.0',
#     'unit_price': 'REAL DEFAULT 0.0',
#     'quantity_used' : 'REAL DEFAULT 0.0',
# }
# db.create_table('contract_services',
#                 table_columns,
#                 foreign_key_column='contract_id',
#                 ref_table='contracts',
#                 ref_column='id')

#---------- add row data-----------------
# new_service = {
#                 'contract_id': 1,  # test contract
#                 'description': 'new service', 
#                 'unit' : 'EA',
#                 'quantity': 3, 
#                 'unit_price': 200.0, 
#                 'quantity_used' :0
#             }
# print('adding row...')
#-----------update row data----------------
# new_service = {
#                 'id': 1, 
#                 'contract_id': 1,
#                 'description': 'description updated', 
#                 'unit' : 'EA',
#                 'quantity': 320, 
#                 'unit_price': 55, 
#                 'quantity_used' : 0
#             }
# print('updating row...')

# #-------- upsert(data) -----------------
# success,new_id = db.upsert_row(
#                 table_name= 'contract_services',
#                 row_data= new_service    
#             )
    
