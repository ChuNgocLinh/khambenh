from config import DB_TYPE


def is_sqlserver():
    return DB_TYPE != "mysql"


def select_top(limit):
    if not limit or not is_sqlserver():
        return ""
    return f"TOP {int(limit)} "


def limit_clause(limit):
    if not limit or is_sqlserver():
        return ""
    return f" LIMIT {int(limit)}"


def pagination_clause():
    if is_sqlserver():
        return " OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
    return " LIMIT ? OFFSET ?"


def pagination_params(limit, offset):
    if is_sqlserver():
        return (int(offset), int(limit))
    return (int(limit), int(offset))


def today_filter(column):
    if is_sqlserver():
        return f"CAST({column} AS date) = CAST(GETDATE() AS date)"
    return f"DATE({column}) = CURDATE()"


def tomorrow_filter(column):
    if is_sqlserver():
        return f"CAST({column} AS date) = DATEADD(day, 1, CAST(GETDATE() AS date))"
    return f"DATE({column}) = DATE_ADD(CURDATE(), INTERVAL 1 DAY)"


def by_date_filter(column):
    if is_sqlserver():
        return f"CAST({column} AS date) = CAST(? AS date)"
    return f"DATE({column}) = ?"


def string_agg(expression, separator=", "):
    if is_sqlserver():
        return f"COALESCE(STRING_AGG(CAST({expression} AS NVARCHAR(MAX)), '{separator}'), '')"
    return f"COALESCE(GROUP_CONCAT(DISTINCT {expression} ORDER BY {expression} SEPARATOR '{separator}'), '')"
