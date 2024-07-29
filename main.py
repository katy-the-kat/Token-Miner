import os
import random
import hashlib
import string
import psutil
import time
import threading

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
        raise ValueError("Invalid memory unit. Use 'G' for GB, 'M' for MB, or 'K' for KB.")

target_memory_usage = parse_memory_limit(USE_MEMORY)
large_memory_usage = []

cpu_hogger_thread = None
cpu_hogger_running = False

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_gui():
    clear_terminal()
    print("--------------- Is-a.space Token Miner v5 ---------------")
    print("1 > Start mining Tokens")
    print("2 > Print last token mined")
    print("3 > Get an address")
    print("4 > Mine a specific number of tokens")
    print("5 > List addresses")
    print("6 > Get an existing address")
    print("7 > Exit")
    print("-----------------------------------------------------------")

def print_mining_log(logs, last_printed_index):
    for i in range(last_printed_index + 1, len(logs)):
        print(f"{logs[i][0]} Token(s) mined | Token: {logs[i][1]}")
    return len(logs) - 1

def generate_address(name, last_token_number, last_token_id):
    rand_num = random.randint(0, 9999999999999999)
    address_info = f"{name}{last_token_number}{last_token_id}{rand_num}"
    address_hash = hashlib.sha256(address_info.encode()).hexdigest()
    return address_hash

def generate_token(length=16):
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
    time.sleep(0.1)

def cpu_hogger():
    global cpu_hogger_running
    while cpu_hogger_running:
        result = sum(i**2 for i in range(100000))

def start_cpu_hogger():
    global cpu_hogger_thread, cpu_hogger_running
    if cpu_hogger_thread is None or not cpu_hogger_thread.is_alive():
        cpu_hogger_running = True
        cpu_hogger_thread = threading.Thread(target=cpu_hogger, daemon=True)
        cpu_hogger_thread.start()
        print("--------------- Mining Started ---------------")

def stop_cpu_hogger():
    global cpu_hogger_running
    cpu_hogger_running = False
    if cpu_hogger_thread:
        cpu_hogger_thread.join()

def mine_tokens(logs, num_tokens=None):
    try:
        start_cpu_hogger()
        last_number, _ = get_last_mined_token("tokens.txt")
        if last_number is None:
            last_number = 0
        else:
            last_number += 1

        last_printed_index = -1

        if num_tokens is None:
            while cpu_hogger_running:
                token = generate_token()
                encrypted_token = encrypt_token(token)
                logs.append((last_number, encrypted_token))

                if len(logs) > last_printed_index + 8:
                    last_printed_index = print_mining_log(logs, last_printed_index)

                with open("tokens.txt", "a") as file:
                    file.write(f"{last_number} | {encrypted_token}\n")

                last_number += 1198836244055076906
                allocate_memory(target_memory_usage // 10)  # Adjust the memory allocation if needed
        else:
            for _ in range(num_tokens):
                token = generate_token()
                encrypted_token = encrypt_token(token)
                logs.append((last_number, encrypted_token))

                if len(logs) > last_printed_index + 8:
                    last_printed_index = print_mining_log(logs, last_printed_index)

                with open("tokens.txt", "a") as file:
                    file.write(f"{last_number} | {encrypted_token}\n")

                last_number += 1198836244055076906
                allocate_memory(target_memory_usage // 10)  # Adjust the memory allocation if needed

        stop_cpu_hogger()
    except KeyboardInterrupt:
        print("\nStopped Mining (Ctrl+C pressed).")
        stop_cpu_hogger()
    except Exception as e:
        print(f"An error occurred: {e}")
        stop_cpu_hogger()

def print_last_mined_token(filename="tokens.txt"):
    last_number, last_token = get_last_mined_token(filename)
    if last_number is not None:
        print(f"Last Mined Token: {last_number} | Token id: {last_token}")
    else:
        print("No tokens mined yet.")

def get_address():
    name = input("Enter a name for address (Will be encrypted) > ")
    last_number, last_token_id = get_last_mined_token("tokens.txt")
    address = generate_address(name, last_number, last_token_id)
    with open("address.txt", "w") as file:
        file.write(address)
    print(f"Address generated and saved to 'address.txt': {address}")

def list_addresses():
    try:
        with open("address.txt", "r") as file:
            addresses = file.readlines()
            if not addresses:
                print("No addresses found.")
            else:
                print("--------------- Is-a.space Token Miner v5 ---------------")
                for i, address in enumerate(addresses, start=1):
                    print(f"{i} > Address {i} | Address: {address.strip()}")
                if len(addresses) > 5:
                    print("[2] Go to previous page")
                    print("[1] Go to next page")
                print("-----------------------------------------------------------")
    except FileNotFoundError:
        print("No addresses found.")

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
                get_address()
            elif choice == "4":
                num_tokens = int(input("Enter number of tokens to mine > "))
                mine_tokens(logs, num_tokens)
            elif choice == "5":
                list_addresses()
                input("Press Enter to return to the main menu > ")
            elif choice == "6":
                # Assuming get_existing_address is implemented somewhere
                get_existing_address()
            elif choice == "7":
                print("Exiting...")
                break
            else:
                print("Invalid option, Please enter a valid option.")
    except KeyboardInterrupt:
        print("\nExited (Ctrl+C pressed).")

if __name__ == "__main__":
    main()
