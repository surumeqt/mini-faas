# def handler(event):
#     name = event.get("name", "world")
#     return {"message": f"Hello {name}"}

def handler(event):
    a = event.get("a")
    b = event.get("b")
    sum = a + b
    return { "result" : f"{a} + {b} = {sum}" }