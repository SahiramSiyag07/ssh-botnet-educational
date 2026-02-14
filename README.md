# SSH Botnet - Educational Project

## ⚠️ DISCLAIMER

**This project is for educational and ethical hacking purposes only!**

Unauthorized access to computer systems without explicit permission is:
- **Illegal** under computer fraud and abuse laws
- **Unethical** and violates privacy rights
- **Punishable** by fines and imprisonment

**Always obtain written permission before testing these techniques on any system.**

This tool is designed to help students and security professionals understand:
- How botnets operate using SSH connections
- Network attack vectors like SYN flooding
- SSH security vulnerabilities
- Defense mechanisms against botnet attacks

---

## 📋 Project Overview

This Python-based SSH Botnet demonstrates key cybersecurity concepts:

| Feature | Description |
|---------|-------------|
| **List Bots** | View all connected SSH bots and their status |
| **Execute Commands** | Send commands to all bots simultaneously |
| **Interactive Shell** | Real-time bash shell for command execution |
| **Add Bots** | Connect to new SSH clients |
| **DDoS Simulation** | SYN flood attack demonstration |
| **Persistence** | Save/load botnet configuration |

---

## 🛠️ Installation

### Prerequisites
- Python 3.7+
- pip package manager
- Linux/Unix environment (for Scapy)

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install pexpect scapy
```

**Note:** Scapy requires root/administrator privileges for packet crafting.

---

## 🚀 Usage

### Starting the Botnet Controller

```bash
sudo python3 main.py
```

**Note:** `sudo` is required for DDoS simulation features using Scapy.

### Main Menu Options

```
[1] List Bots              - Display all connected bots
[2] Execute Command        - Run command on all bots
[3] Interactive Shell      - Real-time command interface
[4] Add Bot                - Connect to new SSH client
[5] DDoS Attack            - SYN flood simulation
[6] Save Botnet            - Save configuration to JSON
[7] Load Botnet            - Restore from JSON file
[8] Remove Bot             - Disconnect specific bot
[9] Disconnect All         - Close all connections
[0] Exit                   - Quit application
```

---

## 📖 Step-by-Step Guide

### 1. Adding Bots

```
Select option [0-9]: 4
Enter host (IP/hostname): 192.168.1.100
Enter username: admin
Enter password: password123
```

### 2. Listing Connected Bots

```
Select option [0-9]: 1

============================================================
CONNECTED BOTS
============================================================
1. 192.168.1.100 (admin) - ✓ Connected
2. 192.168.1.101 (root) - ✓ Connected
============================================================
Total bots: 2
```

### 3. Executing Commands

```
Select option [0-9]: 2
Enter command to execute: uname -a

[*] Sending command to 2 bot(s): uname -a
============================================================

[+] Output from 192.168.1.100:
Linux bot1 5.4.0-generic #1 SMP ...

[+] Output from 192.168.1.101:
Linux bot2 5.4.0-generic #1 SMP ...

============================================================
```

### 4. Interactive Shell

```
Select option [0-9]: 3

============================================================
INTERACTIVE BASH SHELL
Type 'exit' to quit, 'list' to show bots
============================================================

botnet-shell> whoami
[+] Output from 192.168.1.100:
root

[+] Output from 192.168.1.101:
admin

botnet-shell> exit
[*] Exiting interactive shell...
```

### 5. DDoS Attack Simulation (SYN Flood)

```
Select option [0-9]: 5

--- DDoS Attack (SYN Flood) ---
WARNING: Only use on systems you own or have permission to test!
Enter target IP: 192.168.1.200
Enter target port [default: 80]: 80
Enter duration in seconds [default: 60]: 30
Enter number of threads per bot [default: 10]: 5

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
WARNING: EDUCATIONAL USE ONLY!
Ensure you have permission to test this target!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Target: 192.168.1.200:80 for 30s. Confirm? (yes/no): yes

[*] Initiating SYN flood attack on 192.168.1.200:80
[*] Using 2 bot(s) with 5 threads each
[*] Attack duration: 30 seconds
[*] Press Ctrl+C to stop early

[*] Attacking... Elapsed: 15s | Remaining: 15s
```

### 6. Saving Botnet Configuration

```
Select option [0-9]: 6
Enter filename [default: botnet.json]: my_botnet.json
[+] Botnet saved to my_botnet.json
[*] Saved 2 bot(s)
```

The JSON file format:
```json
{
    "bots": [
        {
            "host": "192.168.1.100",
            "username": "admin",
            "password": "password123"
        }
    ],
    "saved_at": "2024-01-15 10:30:00"
}
```

---

## 🔧 Technical Details

### Architecture

```
┌─────────────────┐
│   Botnet        │
│   Controller    │
│   (main.py)     │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐  ┌──▼────┐
│ Bot 1 │  │ Bot 2 │  ...
│(SSH)  │  │(SSH)  │
└───────┘  └───────┘
```

### Key Components

| File | Purpose |
|------|---------|
| `botnet.py` | Core botnet logic, SSH connections, DDoS |
| `main.py` | CLI interface and user interaction |
| `botnet.json` | Persistent storage for bot credentials |

### Technologies Used

- **pxssh** (pexpect): SSH client automation
- **Scapy**: Packet crafting for DDoS simulation
- **threading**: Concurrent command execution
- **JSON**: Configuration persistence

---

## 🎓 Learning Objectives

By completing this project, you will understand:

1. **Botnet Structure**
   - How command & control (C&C) servers operate
   - Bot recruitment and management
   - Distributed attack coordination

2. **SSH Exploitation**
   - Weak credential vulnerabilities
   - Automated SSH authentication
   - Session management

3. **Network Attacks**
   - SYN flood mechanics
   - TCP handshake exploitation
   - Resource exhaustion techniques

4. **Defense Strategies**
   - SSH hardening (key-based auth, disable root)
   - Fail2ban for brute-force protection
   - Network monitoring for botnet detection
   - Rate limiting and DDoS mitigation

---

## 🛡️ Security Countermeasures

### Protecting Against SSH Botnets

1. **Use SSH Keys Instead of Passwords**
   ```bash
   ssh-keygen -t ed25519
   ssh-copy-id user@host
   ```

2. **Disable Password Authentication**
   ```bash
   # /etc/ssh/sshd_config
   PasswordAuthentication no
   PubkeyAuthentication yes
   ```

3. **Implement Fail2ban**
   ```bash
   sudo apt install fail2ban
   sudo systemctl enable fail2ban
   ```

4. **Change Default SSH Port**
   ```bash
   # /etc/ssh/sshd_config
   Port 2222  # Non-standard port
   ```

5. **Use Firewall Rules**
   ```bash
   sudo ufw allow from 192.168.1.0/24 to any port 22
   sudo ufw deny 22
   ```

6. **Monitor for Botnet Activity**
   - Check for multiple failed login attempts
   - Monitor unusual outbound traffic
   - Review system logs regularly

---

## 🔬 Advanced Topics

### Future Enhancements

1. **Encryption**
   - Implement asymmetric encryption for C&C communication
   - Use TLS/SSL for botnet traffic

2. **Persistence Mechanisms**
   - Auto-reconnect after system reboot
   - Process hiding techniques
   - Registry modifications (Windows)

3. **Advanced Attacks**
   - UDP flooding
   - ICMP flooding
   - HTTP/HTTPS layer 7 attacks
   - Slowloris attacks

4. **Evasion Techniques**
   - Domain Generation Algorithms (DGA)
   - Fast-flux DNS
   - Protocol tunneling
   - Timing-based evasion

5. **Anti-Botnet Detection**
   - Network traffic analysis
   - Behavioral detection algorithms
   - Honeypot deployment

---

## 📚 Resources

### Educational Materials
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [SANS Institute - Botnet Detection](https://www.sans.org)

### Tools for Defense
- **Wireshark**: Network traffic analysis
- **Snort**: Intrusion detection system
- **OSSEC**: Host-based intrusion detection
- **Suricata**: Network threat detection

---

## ⚖️ Legal Notice

This software is provided for educational purposes only. The authors assume no liability for:

- Misuse of this software
- Damage to computer systems
- Violation of laws or regulations
- Any criminal activities

By using this software, you agree to:
- Only test on systems you own or have explicit permission to test
- Follow all applicable laws and regulations
- Use this knowledge for defensive and educational purposes only

---

## 🤝 Contributing

This is an educational project. Contributions that improve:
- Documentation
- Defensive techniques
- Detection methods
- Educational content

are welcome.

---

## 📞 Support

For educational questions and discussions:
- Open an issue on the project repository
- Consult cybersecurity course materials
- Engage with security communities

---

**Remember: With great power comes great responsibility. Use this knowledge to make systems more secure, not to cause harm.**

---

*Last Updated: 2026*
*Version: 1.0*
*License: Educational Use Only*
