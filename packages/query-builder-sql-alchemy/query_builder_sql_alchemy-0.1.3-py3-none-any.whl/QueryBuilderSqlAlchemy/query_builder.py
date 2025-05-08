from typing import List, Optional, Type, Any, Tuple, Union, Callable
from sqlalchemy.orm import attributes
from enum import Enum


class Operator(str, Enum):
    """Enum for SQL operators used in conditions"""

    EQ = "="
    NE = "<>"
    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="
    LIKE = "LIKE"
    BETWEEN = "BETWEEN"
    IN = "IN"


class Condition:
    """A class to represent SQL conditions for the WHERE clause."""

    def __init__(
        self,
        column: Union[str, attributes.InstrumentedAttribute],
        operator: Operator,
        value: Any,
        value2: Any = None,
    ):
        self.column = column
        self.operator = operator
        self.value = value
        self.value2 = value2  # Used for BETWEEN operator

    def to_sql_string(self) -> str:
        # Extract table name and column name if it's a SQLAlchemy column
        if isinstance(self.column, attributes.InstrumentedAttribute):
            table_name = self.column.parent.class_.__tablename__
            column_name = self.column.key
            column_str = f"`{table_name}`.`{column_name}`"
        else:
            column_str = self.column

        # Format the value appropriately
        if isinstance(self.value, str):
            # Escape single quotes in strings
            escaped_value = self.value.replace("'", "''")
            formatted_value = f"'{escaped_value}'"
        elif self.value is None:
            formatted_value = "NULL"
        else:
            formatted_value = str(self.value)

        # Get the operator string value
        operator_str = (
            str(self.operator.value)
            if isinstance(self.operator, Operator)
            else str(self.operator)
        )

        # Handle specific operators
        if self.operator == Operator.EQ and self.value is None:
            return f"{column_str} IS NULL"
        elif self.operator == Operator.NE and self.value is None:
            return f"{column_str} IS NOT NULL"
        elif self.operator == Operator.LIKE:
            # Ensure LIKE values have wildcards if not already present
            if not (formatted_value.startswith("'%") or formatted_value.endswith("%'")):
                # Fix: Prepare the value separately to avoid backslashes in f-string expression
                escaped_value = self.value.replace("'", "''")
                formatted_value = f"'%{escaped_value}%'"
            return f"{column_str} {operator_str} {formatted_value}"
        elif self.operator == Operator.BETWEEN:
            # Format second value for BETWEEN
            if isinstance(self.value2, str):
                # Fix: Prepare the value separately to avoid backslashes in f-string expression
                escaped_value2 = self.value2.replace("'", "''")
                formatted_value2 = f"'{escaped_value2}'"
            elif self.value2 is None:
                raise ValueError("BETWEEN operator requires two non-NULL values")
            else:
                formatted_value2 = str(self.value2)
            return (
                f"{column_str} {operator_str} {formatted_value} AND {formatted_value2}"
            )
        elif self.operator == Operator.IN:
            # Format list for IN operator
            if not isinstance(self.value, (list, tuple)):
                raise ValueError("IN operator requires a list or tuple value")
            values_list = []
            for val in self.value:
                if isinstance(val, str):
                    # Fix: Prepare the value separately to avoid backslashes in f-string expression
                    escaped_val = val.replace("'", "''")
                    values_list.append(f"'{escaped_val}'")
                elif val is None:
                    values_list.append("NULL")
                else:
                    values_list.append(str(val))
            formatted_values = ", ".join(values_list)
            return f"{column_str} {operator_str} ({formatted_values})"
        else:
            return f"{column_str} {operator_str} {formatted_value}"


class ConditionGroup:
    """A class to group conditions with logical operators (AND, OR)."""

    def __init__(self, conditions=None, operator="AND"):
        self.conditions = conditions or []
        self.operator = operator

    def to_sql_string(self) -> str:
        if not self.conditions:
            return ""

        condition_strings = []
        for condition in self.conditions:
            if isinstance(condition, (Condition, ConditionGroup)):
                condition_strings.append(condition.to_sql_string())
            elif isinstance(condition, str):
                condition_strings.append(condition)
            else:
                raise TypeError(f"Unsupported condition type: {type(condition)}")

        joined_conditions = f" {self.operator} ".join(condition_strings)

        # Add parentheses if there's more than one condition
        if len(condition_strings) > 1:
            return f"({joined_conditions})"
        return joined_conditions


class QueryBuilder:
    """
    Builds SQL queries for SQLAlchemy models, supporting SELECT, FROM, WHERE,
    ORDER BY, LIMIT, and OFFSET clauses.

    This class generates SQL query strings, and is designed to be compatible with
    SQLAlchemy ORM models.  It handles table and column names correctly,
    including proper quoting.
    """

    def __init__(self):
        """
        Initializes a new SqlQueryBuilder instance.  All internal state
        is reset, so a new query is started.
        """
        self._select_columns: List[str] = []
        self._from_table: Optional[str] = None
        self._where_conditions: List[Any] = []  # Change to List[Any]
        self._order_by_clause: Optional[str] = None
        self._limit_value: Optional[int] = None
        self._offset_value: Optional[int] = None
        self._joins: List[Tuple[str, Any, str]] = []  # on_clause can now be Any

    # Convenience methods for conditions
    def equals(
        self, column: Union[str, attributes.InstrumentedAttribute], value: Any
    ) -> "SqlQueryBuilder":
        """Add an equals condition to the WHERE clause."""
        self.where(Condition(column, Operator.EQ, value))
        return self

    def not_equals(
        self, column: Union[str, attributes.InstrumentedAttribute], value: Any
    ) -> "SqlQueryBuilder":
        """Add a not-equals condition to the WHERE clause."""
        self.where(Condition(column, Operator.NE, value))
        return self

    def less_than(
        self, column: Union[str, attributes.InstrumentedAttribute], value: Any
    ) -> "SqlQueryBuilder":
        """Add a less-than condition to the WHERE clause."""
        self.where(Condition(column, Operator.LT, value))
        return self

    def less_than_or_equal(
        self, column: Union[str, attributes.InstrumentedAttribute], value: Any
    ) -> "SqlQueryBuilder":
        """Add a less-than-or-equal condition to the WHERE clause."""
        self.where(Condition(column, Operator.LE, value))
        return self

    def greater_than(
        self, column: Union[str, attributes.InstrumentedAttribute], value: Any
    ) -> "SqlQueryBuilder":
        """Add a greater-than condition to the WHERE clause."""
        self.where(Condition(column, Operator.GT, value))
        return self

    def greater_than_or_equal(
        self, column: Union[str, attributes.InstrumentedAttribute], value: Any
    ) -> "SqlQueryBuilder":
        """Add a greater-than-or-equal condition to the WHERE clause."""
        self.where(Condition(column, Operator.GE, value))
        return self

    def like(
        self, column: Union[str, attributes.InstrumentedAttribute], value: str
    ) -> "SqlQueryBuilder":
        """Add a LIKE condition to the WHERE clause."""
        self.where(Condition(column, Operator.LIKE, value))
        return self

    def between(
        self,
        column: Union[str, attributes.InstrumentedAttribute],
        value1: Any,
        value2: Any,
    ) -> "SqlQueryBuilder":
        """Add a BETWEEN condition to the WHERE clause."""
        self.where(Condition(column, Operator.BETWEEN, value1, value2))
        return self

    def in_list(
        self, column: Union[str, attributes.InstrumentedAttribute], values: list
    ) -> "SqlQueryBuilder":
        """Add an IN condition to the WHERE clause."""
        self.where(Condition(column, Operator.IN, values))
        return self

    def and_group(self, *conditions) -> "SqlQueryBuilder":
        """Group conditions with AND operator."""
        self.where(ConditionGroup(conditions, "AND"))
        return self

    def or_group(self, *conditions) -> "SqlQueryBuilder":
        """Group conditions with OR operator."""
        self.where(ConditionGroup(conditions, "OR"))
        return self

    def reset(self):
        """
        Resets the query builder to its initial state, allowing for a new
        query to be constructed.  This is useful if you want to reuse
        the same builder object for multiple queries.
        """
        self._select_columns = []
        self._from_table = None
        self._where_conditions = []
        self._order_by_clause = None
        self._limit_value = None
        self._offset_value = None
        self._joins = []

    def select(self, columns: List[Any]) -> "SqlQueryBuilder":
        """
        Specifies the columns to be selected in the query.

        This method now accepts a list of either column name strings (e.g., 'id')
        or SQLAlchemy model attributes.

        To apply SQL functions like LOWER() or UPPER() to a column,
        pass a tuple with the column and the function name as a string.
        Example: (User.username, 'LOWER') will generate LOWER(`users`.`username`) AS `username`

        Args:
            columns: A list of column names, SQLAlchemy model attributes, or tuples of (column, function).
        Returns:
            The SqlQueryBuilder instance (for chaining).
        """
        new_select_columns = []
        for col in columns:
            if isinstance(col, str):
                new_select_columns.append(col)  # Keep the string column name
            elif isinstance(col, tuple) and len(col) == 2:
                # Handle (column, function) tuple
                column, func = col
                if isinstance(column, attributes.InstrumentedAttribute):
                    table_name = column.parent.class_.__tablename__
                    col_key = column.key
                    # Apply the function and create an alias
                    new_select_columns.append(
                        f"{func}(`{table_name}`.`{col_key}`) AS `{col_key}`"
                    )
                else:
                    raise TypeError(
                        f"Invalid column type in tuple: {type(column)}. Expected SQLAlchemy model attribute."
                    )
            elif isinstance(col, attributes.InstrumentedAttribute):
                # Assuming it's a SQLAlchemy model attribute, get full column name
                new_select_columns.append(
                    f"`{col.parent.class_.__tablename__}`.`{col.key}`"
                )
            else:
                raise TypeError(
                    f"Invalid column type: {type(col)}. Expected str, tuple, or SQLAlchemy model attribute."
                )
        self._select_columns = new_select_columns
        return self

    def from_table(self, model_class: Type[Any]) -> "SqlQueryBuilder":
        """
        Specifies the table for the query.

        Args:
            model_class: The SQLAlchemy model class.

        Returns:
            The SqlQueryBuilder instance (for chaining).
        """
        if not (isinstance(model_class, type) and hasattr(model_class, "__table__")):
            raise TypeError("Expected a SQLAlchemy model class.")
        self._from_table = model_class.__tablename__
        return self

    def where(self, condition: Any) -> "SqlQueryBuilder":
        """
        Adds a WHERE condition to the query.

        Args:
            condition: The WHERE condition, which can be a string, a SQLAlchemy expression,
                       a Condition object, or a ConditionGroup object.
                       It's the caller's responsibility to ensure this condition
                       is valid SQL. The condition is added to a list, and
                       they are combined with AND.
        Returns:
            The SqlQueryBuilder instance (for chaining).
        """
        if isinstance(condition, str):
            self._where_conditions.append(condition)
        elif hasattr(condition, "compile"):  # check for SQLAlchemy where clause
            self._where_conditions.append(condition)
        elif isinstance(condition, (Condition, ConditionGroup)):
            self._where_conditions.append(condition)
        else:
            raise TypeError(
                "WHERE condition must be a string, SQLAlchemy expression, Condition, or ConditionGroup"
            )
        return self

    def order_by(self, column: Any, direction: str = "ASC") -> "SqlQueryBuilder":
        """
        Specifies the ORDER BY clause for the query.

        Args:
            column:  The column to order by.  This can be a string or a
                     SQLAlchemy model attribute (e.g., User.id).
            direction: The sorting direction ('ASC' or 'DESC').  Defaults to 'ASC'.
                       The code will uppercase this, and check for validity.

        Returns:
            The SqlQueryBuilder instance (for chaining).
        """
        direction_upper = direction.upper()
        if direction_upper not in ("ASC", "DESC"):
            raise ValueError(
                f"Invalid direction '{direction}'.  Must be 'ASC' or 'DESC'."
            )

        if isinstance(column, str):
            self._order_by_clause = f"`{column}` {direction_upper}"
        elif isinstance(column, attributes.InstrumentedAttribute):
            self._order_by_clause = f"`{column.parent.class_.__tablename__}`.`{column.key}` {direction_upper}"
        else:
            raise TypeError("column must be a string or a SQLAlchemy model attribute.")
        return self

    def limit(self, limit: int) -> "SqlQueryBuilder":
        """
        Specifies the LIMIT clause for the query.

        Args:
            limit: The maximum number of rows to return.

        Returns:
            The SqlQueryBuilder instance (for chaining).
        """
        if not isinstance(limit, int) or limit < 0:
            raise ValueError("Limit must be a non-negative integer.")
        self._limit_value = limit
        return self

    def offset(self, offset: int) -> "SqlQueryBuilder":
        """
        Specifies the OFFSET clause for the query.

        Args:
            offset: The number of rows to skip before starting to return rows.

        Returns:
            The SqlQueryBuilder instance (for chaining).
        """
        if not isinstance(offset, int) or offset < 0:
            raise ValueError("Offset must be a non-negative integer.")
        self._offset_value = offset
        return self

    def join(
        self,
        left_column: attributes.InstrumentedAttribute,
        right_column: attributes.InstrumentedAttribute = None,
        join_type: str = "INNER",
    ) -> "SqlQueryBuilder":
        """
        Adds a JOIN clause to the query using SQLAlchemy model columns.

        This method only accepts SQLAlchemy model column attributes (Model.column) for the join condition.

        If only left_column is provided, it will join with the column of the same name in the FROM table.

        Args:
            left_column: SQLAlchemy model column attribute (e.g., Table1.column1)
            right_column: SQLAlchemy model column attribute (e.g., Table2.column1)
                         If None, will join with the same column name in the FROM table
            join_type: The type of JOIN ("INNER", "LEFT", "RIGHT", "FULL", "CROSS")

        Returns:
            The SqlQueryBuilder instance.

        Examples:
            # Explicit join
            query.join(User.id, Post.user_id)

            # Auto-join with same column name in FROM table
            query.join(Category.id)  # Joins Category.id with the 'id' column in the FROM table
        """
        # Validate and format the join_type
        join_type_upper = join_type.upper()
        if join_type_upper not in ["INNER", "LEFT", "RIGHT", "FULL", "CROSS"]:
            raise ValueError(
                f"Invalid join_type: {join_type}. Must be INNER, LEFT, RIGHT, FULL, or CROSS."
            )

        # Ensure left_column is a SQLAlchemy column
        if not isinstance(left_column, attributes.InstrumentedAttribute):
            raise TypeError(
                "left_column must be a SQLAlchemy model column attribute (Model.column)"
            )

        # Extract left column information
        left_table = left_column.parent.class_.__tablename__
        left_column_name = left_column.key

        # If right column is None, join with the same column name in the FROM table
        if right_column is None:
            if not self._from_table:
                raise ValueError(
                    "Cannot use single-column join without specifying FROM table first"
                )

            # Create join condition using the same column name from the FROM table
            on_clause_str = f"`{left_table}`.`{left_column_name}` = `{self._from_table}`.`{left_column_name}`"
            self._joins.append((left_table, on_clause_str, join_type_upper))
            return self

        # Ensure right_column is a SQLAlchemy column
        if not isinstance(right_column, attributes.InstrumentedAttribute):
            raise TypeError(
                "right_column must be a SQLAlchemy model column attribute (Model.column)"
            )

        # Extract right column information
        right_table = right_column.parent.class_.__tablename__
        right_column_name = right_column.key

        # Create the join condition
        on_clause_str = f"`{left_table}`.`{left_column_name}` = `{right_table}`.`{right_column_name}`"

        # Add join to the joins list
        self._joins.append((left_table, on_clause_str, join_type_upper))

        return self

    def build_count_query(self) -> str:
        """
        Build a COUNT query using the same conditions.

        Returns:
            The SQL COUNT query string.
        """
        if not self._from_table:
            raise ValueError("FROM table must be specified.")

        # FROM clause
        from_clause = f"FROM `{self._from_table}`"

        # JOIN clauses
        join_clauses = ""
        for table, on_clause, join_type in self._joins:
            join_clauses += f" {join_type} JOIN `{table}` ON {on_clause}"

        # WHERE clause
        where_clause_str = ""
        if self._where_conditions:
            where_clause_parts = []
            for condition in self._where_conditions:
                if isinstance(condition, str):
                    where_clause_parts.append(condition)
                elif hasattr(condition, "compile"):
                    # Convert SQLAlchemy expression to string and replace double quotes with backticks
                    compiled_expr = str(
                        condition.compile(compile_kwargs={"literal_binds": True})
                    )
                    compiled_expr = compiled_expr.replace('"', "`")
                    where_clause_parts.append(compiled_expr)
                elif isinstance(condition, (Condition, ConditionGroup)):
                    where_clause_parts.append(condition.to_sql_string())
                else:
                    raise TypeError(
                        "Unsupported type in WHERE clause. Must be str, SQLAlchemy expression, Condition, or ConditionGroup"
                    )
            where_clause_str = f"WHERE {' AND '.join(where_clause_parts)}"
        where_clause = where_clause_str

        # Build the COUNT query with just the necessary parts
        query = f"SELECT COUNT(*) as total {from_clause} {join_clauses} {where_clause}".strip()
        return query.replace("  ", " ")  # remove double spaces

    def build(self) -> str:
        """
        Constructs the SQL query string based on the specified clauses.

        Returns:
            The complete SQL query string.

        Raises:
            ValueError: If the FROM clause has not been specified.
        """
        if not self._from_table:
            raise ValueError("FROM table must be specified.")

        # SELECT clause
        select_clause = (
            f"SELECT {', '.join(self._select_columns)}"
            if self._select_columns
            else "SELECT *"
        )

        # FROM clause
        from_clause = f"FROM `{self._from_table}`"

        # JOIN clauses
        join_clauses = ""
        for table, on_clause, join_type in self._joins:
            join_clauses += f" {join_type} JOIN `{table}` ON {on_clause}"

        # WHERE clause
        where_clause_str = ""
        if self._where_conditions:
            where_clause_parts = []
            for condition in self._where_conditions:
                if isinstance(condition, str):
                    where_clause_parts.append(condition)
                elif hasattr(condition, "compile"):
                    # Convert SQLAlchemy expression to string and replace double quotes with backticks
                    compiled_expr = str(
                        condition.compile(compile_kwargs={"literal_binds": True})
                    )
                    compiled_expr = compiled_expr.replace('"', "`")
                    where_clause_parts.append(compiled_expr)
                elif isinstance(condition, (Condition, ConditionGroup)):
                    where_clause_parts.append(condition.to_sql_string())
                else:
                    raise TypeError(
                        "Unsupported type in WHERE clause. Must be str, SQLAlchemy expression, Condition, or ConditionGroup"
                    )
            where_clause_str = f"WHERE {' AND '.join(where_clause_parts)}"
        where_clause = where_clause_str

        # ORDER BY clause
        order_by_clause = (
            f"ORDER BY {self._order_by_clause}" if self._order_by_clause else ""
        )

        # LIMIT and OFFSET clauses
        limit_clause = (
            f"LIMIT {self._limit_value}" if self._limit_value is not None else ""
        )
        offset_clause = (
            f"OFFSET {self._offset_value}" if self._offset_value is not None else ""
        )

        # Combine all clauses
        sql_query = f"{select_clause} {from_clause}{join_clauses} {where_clause} {order_by_clause} {limit_clause} {offset_clause}".strip()
        return sql_query.replace("  ", " ")  # remove double spaces
