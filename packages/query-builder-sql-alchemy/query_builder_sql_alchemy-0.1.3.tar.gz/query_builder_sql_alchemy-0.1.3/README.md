# query-builder-sql-alchemy

A flexible SQL query builder for SQLAlchemy ORM models that makes it easy to build complex SQL queries using a fluent interface.

## Features

- 🚀 Fluent interface for building SQL queries
- 🔍 Support for complex WHERE conditions with AND/OR grouping
- 🔄 JOIN operations (INNER, LEFT, RIGHT, FULL, CROSS)
- 📊 ORDER BY, LIMIT, and OFFSET support
- 🛡️ Safe SQL string generation with proper escaping
- 🎯 Compatible with SQLAlchemy ORM models
- 📝 Type hints for better IDE support

## Installation

Using pip:
```bash
pip install query-builder-sql-alchemy
```

Using Poetry:
```bash
poetry add query-builder-sql-alchemy
```

## Quick Start

```python
from QueryBuilderSqlAlchemy import QueryBuilder, Condition, ConditionGroup, Operator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

# Define your SQLAlchemy model
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

# Create a query builder
qb = QueryBuilder()

# Build a simple query
query = (qb
    .select([User.id, User.name])
    .from_table(User)
    .where(Condition(User.name, Operator.LIKE, 'John%'))
    .limit(10)
    .build())

print(query)
# Output: SELECT `users`.`id`, `users`.`name` FROM `users` WHERE `users`.`name` LIKE 'John%' LIMIT 10
```

## Advanced Usage

### Complex Conditions

```python
# Using AND/OR conditions
query = (qb
    .select([User.id, User.name, User.email])
    .from_table(User)
    .where(
        ConditionGroup([
            Condition(User.name, Operator.LIKE, 'John%'),
            Condition(User.email, Operator.LIKE, '%@gmail.com')
        ], 'AND')
    )
    .build())
```

### Joins

```python
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    title = Column(String)

# Join query
query = (qb
    .select([User.name, Post.title])
    .from_table(User)
    .join(User.id, Post.user_id)
    .build())
```

### Aggregations

```python
query = (qb
    .select([(User.id, 'COUNT')])
    .from_table(User)
    .where(Condition(User.name, Operator.LIKE, 'John%'))
    .build())
```

## Available Operators

- `EQ`: Equals (=)
- `NE`: Not Equals (<>)
- `LT`: Less Than (<)
- `LE`: Less Than or Equal (<=)
- `GT`: Greater Than (>)
- `GE`: Greater Than or Equal (>=)
- `LIKE`: LIKE operator
- `BETWEEN`: Between two values
- `IN`: IN operator

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see the [LICENSE](LICENSE) file for details.

## Author

- Sourabh Sharma (sourabhsharma.dev@gmail.com)
- GitHub: [@sourabhsharma-dev](https://github.com/sourabhsharma-dev)

## Support

If you encounter any issues or have questions, please file an issue on the [GitHub repository](https://github.com/sourabhsharma-dev/query-builder-sql-alchemy/issues).
