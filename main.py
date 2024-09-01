import os
import random
import hashlib
import string
import psutil

USE_MEMORY = "3G"

def parse_memory_limit(memory_str):
    size = int(memory_str[:-1])
    unit = memory_str[-1].upper()
    if unit == 'G':
        return size * 1024**3
    elif unit == 'M':
        return size * 1024**2
    elif unit == 'K':
        return size * 1024
    else:
        raise ValueError("Invalid memory unit. Use 'G' for GB, 'M', or 'K' for KB.")

target_memory_usage = parse_memory_limit(USE_MEMORY)
large_memory_usage = []

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_gui():
    clear_terminal()
    print("--------------- Is-a.space Token Miner v6 ---------------")
    print("1 > Start mining Tokens")
    print("2 > Print last token mined")
    print("3 > Mine a specific number of tokens")
    print("4 > Exit")
    print("-----------------------------------------------------------")

def print_mining_log(logs, last_printed_index):
    for i in range(last_printed_index + 1, len(logs)):
        print(f"{logs[i][0]} Token(s) mined | Token: {logs[i][1]}")
    return len(logs) - 1

def generate_token(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def encrypt_token(token):
    hasher = hashlib.sha256()
    hasher.update(token.encode())
    return hasher.hexdigest()

def get_last_mined_token(filename):
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
            if not lines:
                return 0, ""
            last_line = lines[-1]
            try:
                number, token = last_line.split("|")
                return int(number), token.strip()
            except ValueError:
                return 0, ""
    except FileNotFoundError:
        try:
            with open(filename, "x") as file:
                file.write("0 | 0\n")
        except OSError:
            print("Error: Could not create file 'tokens.txt'. Check write permissions.")
        return 0, ""

def monitor_memory_usage():
    memory_usage = psutil.virtual_memory().used
    return memory_usage

def allocate_memory(size):
    global large_memory_usage
    if sum(len(chunk) for chunk in large_memory_usage) > target_memory_usage:
        large_memory_usage = large_memory_usage[-(len(large_memory_usage) // 2):]
    large_memory_usage.append('X' * size)

def mine_tokens(logs, num_tokens=None):
    try:
        last_number, _ = get_last_mined_token("tokens.txt")
        if last_number is None:
            last_number = 0
        else:
            last_number += 1

        last_printed_index = -1

        if num_tokens is None:
            while True:
                token = generate_token()
                encrypted_token = encrypt_token(token)
                logs.append((last_number, encrypted_token))

                if len(logs) > last_printed_index + 8:
                    last_printed_index = print_mining_log(logs, last_printed_index)

                with open("tokens.txt", "a") as file:
                    file.write(f"{last_number} | {encrypted_token}\n")

                last_number += 1
                allocate_memory(target_memory_usage // 10)
        else:
            for _ in range(num_tokens):
                token = generate_token()
                encrypted_token = encrypt_token(token)
                logs.append((last_number, encrypted_token))

                if len(logs) > last_printed_index + 8:
                    last_printed_index = print_mining_log(logs, last_printed_index)

                with open("tokens.txt", "a") as file:
                    file.write(f"{last_number} | {encrypted_token}\n")

                last_number += 1
                allocate_memory(target_memory_usage // 10)

    except KeyboardInterrupt:
        print("\nStopped Mining (Ctrl+C pressed).")
    except Exception as e:
        print(f"An error occurred: {e}")

def print_last_mined_token(filename="tokens.txt"):
    last_number, last_token = get_last_mined_token(filename)
    if last_number is not None:
        print(f"Last Mined Token: {last_number} | Token id: {last_token}")
    else:
        print("No tokens mined yet.")
    input("Press Enter to continue...")

def main():
    logs = []

    try:
        while True:
            print_gui()
            choice = input("> ")

            if choice == "1":
                mine_tokens(logs)
            elif choice == "2":
                print_last_mined_token()
            elif choice == "3":
                num_tokens = int(input("Enter number of tokens to mine > "))
                mine_tokens(logs, num_tokens)
            elif choice == "4":
                print("Exiting...")
                break
            else:
                print("Invalid option, Please enter a valid option.")
    except KeyboardInterrupt:
        print("\nExited (Ctrl+C pressed).")

if __name__ == "__main__":
    main()
