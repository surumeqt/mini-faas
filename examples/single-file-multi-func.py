def add(event):
    a = event.get("a")
    b = event.get("b")
    sum = a + b
    return { "result" : f"{a} + {b} = {sum}" }

def subtract(event):
    a = event.get("a")
    b = event.get("b")
    difference = a - b
    return { "result" : f"{a} - {b} = {difference}" }