#!/usr/bin/env python3

#!/usr/bin/env python3

def greet(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    name_input = input("Enter your name: ")
    print(greet(name_input))