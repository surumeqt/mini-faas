def one_function_multiply(event):
    a = event.get("a")
    b = event.get("b")
    product = a * b
    return { "result" : f"{a} * {b} = {product}" }