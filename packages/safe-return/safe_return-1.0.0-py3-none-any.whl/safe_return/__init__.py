

# Safe expression return
def s_return(data):
    # Check if empty
    if not data:
        raise ValueError(f"Data is empty")

    # Allowed math chars
    allowed_ch = ' ()+-*/%.0123456789'
    
    # Safety check
    for ch in data:
        if ch not in allowed_ch:
            raise ValueError(f"Character is not allowed: {ch}")
    
    # Get result
    return u_return(data)


# Unsafe expression return
def u_return(data):
    return eval(data)

