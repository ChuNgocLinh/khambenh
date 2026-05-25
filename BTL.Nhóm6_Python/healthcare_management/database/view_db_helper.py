import sys
import traceback
from database.db import execute, fetch_all

def _safe_fetch_all(query, params=()):
    try:
        return fetch_all(query, params) or []
    except Exception as e:
        print(f"[view_db_helper] _safe_fetch_all error executing '{query}': {e}", file=sys.stderr)
        traceback.print_exc()
        return []

def _safe_execute(query, params=()):
    try:
        return bool(execute(query, params))
    except Exception as e:
        print(f"[view_db_helper] _safe_execute error executing '{query}': {e}", file=sys.stderr)
        traceback.print_exc()
        return False
