#!/bin/python3
import sys

def generate_command(domain):
    # Example logic to generate a command
    command = f"echo 'Processing: {domain}'"
    return command

if __name__ == "__main__":
    if len(sys.argv) != 2:
        # print("Usage: python my_script.py <domain>")
        print("Usage: python my_script.py <command>")
        sys.exit(1)
    command = sys.argv[1]
    # domain = sys.argv[1]
    # command = generate_command(domain)
    print(command)  # This will output the command to stdout