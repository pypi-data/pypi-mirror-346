_mode = "auto"

def set_mode(mode):
    global _mode
    assert mode in ["auto", "lite", "parallel"]
    _mode = mode

def get_mode():
    return _mode