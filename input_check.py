from datetime import date

def looks_like_float(n: str) -> bool:
    try:
        float(n)
        return True
    except:
        return False

def looks_like_int(n: str) -> bool:
    try:
        int(n)
        return True
    except:
        return False

def looks_like_iso_date(n: str) -> bool:
    try:
        date.fromisoformat(n)
        return True
    except:
        return False

