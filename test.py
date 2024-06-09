from art import text2art

def print_hello_world_ascii():
    ascii_art = text2art("Hello, World!")
    print(ascii_art)

if __name__ == "__main__":
    print_hello_world_ascii()