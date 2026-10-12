"""轻量数据库迁移：让 MySQL 实际表结构与 SQLAlchemy 模型保持一致。

只做「加表 / 加列」这种幂等且安全的操作，不会删表、删列、改类型，
所以可以反复执行。

用法（在项目根目录 fastapixxxmmm 下）：
    .venv/Scripts/python.exe -m BizFlow.shujuku.migrate
"""

from sqlalchemy import inspect, text

from BizFlow.shujuku.Management import Base, engine
import BizFlow.shujuku.user  # noqa: F401  触发模型注册到 Base.metadata


def _safe_default(column) -> str | None:
    """给 NOT NULL 的新列算一个能兼容已有行的默认值，否则 ALTER 会失败。"""
    if column.nullable:
        return None
    if column.default is not None or column.server_default is not None:
        return None
    try:
        python_type = column.type.python_type
    except NotImplementedError:
        return None
    if python_type is str:
        return "''"
    if python_type in (int, float):
        return "0"
    return None


def migrate() -> tuple[list[str], list[str], list[str]]:
    """返回 (新建的表, 新增的列, 需要人工处理的列)。"""
    created_tables: list[str] = []
    added_columns: list[str] = []
    manual_columns: list[str] = []

    insp = inspect(engine)
    db_tables = set(insp.get_table_names())

    # 1) 模型里有、数据库里没有的表，直接建
    missing_tables = sorted(set(Base.metadata.tables) - db_tables)
    if missing_tables:
        Base.metadata.create_all(
            engine, tables=[Base.metadata.tables[t] for t in missing_tables]
        )
        created_tables = missing_tables

    # 2) 已存在的表，补齐模型里有、数据库里没有的列
    insp = inspect(engine)
    with engine.begin() as conn:
        for table_name in sorted(Base.metadata.tables):
            if table_name not in db_tables:
                continue
            table = Base.metadata.tables[table_name]
            db_columns = {c["name"] for c in insp.get_columns(table_name)}
            for column in table.columns:
                if column.name in db_columns:
                    continue
                ddl_type = column.type.compile(engine.dialect)
                nullable = "" if column.nullable else " NOT NULL"
                default = _safe_default(column)
                if not column.nullable and default is None:
                    manual_columns.append(f"{table_name}.{column.name}")
                clause = (
                    f"ALTER TABLE `{table_name}` "
                    f"ADD COLUMN `{column.name}` {ddl_type}{nullable}"
                )
                if default is not None:
                    clause += f" DEFAULT {default}"
                conn.execute(text(clause))
                added_columns.append(f"{table_name}.{column.name}")

    return created_tables, added_columns, manual_columns


def main() -> None:
    created, added, manual = migrate()

    print("=== migrate result ===")
    print(f"新建表: {created or '无'}")
    print(f"新增列: {added or '无'}")
    if manual:
        print(f"需人工处理(NOT NULL 且无默认值，请手动补数据): {manual}")
    print("=== done ===")


if __name__ == "__main__":
    main()
