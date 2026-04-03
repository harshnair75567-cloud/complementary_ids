# complementary_ids
a python code which works as a complement to a traditional ids system . This can see through incoming traffic sent a message of connection accepted to the attacker and move the attackers ip address to a text file and then cut off the connection the file name and port can be customised inside the code

🛡️ Python NIDS Engine (Version 3.1)
A multi-threaded Network Intrusion Detection System (NIDS) developed in Python for monitoring unauthorized port access and analyzing packet payloads for known attack signatures.

🚀 Overview
This project is a functional security tool designed to act as a "Honeypot" and "Packet Analyzer." It combines connection-based heuristics (to detect port scanning) with Deep Packet Inspection (DPI) (to detect specific bitwise flag anomalies).

Key Features
Multi-Threaded Sensors: Utilizes background "Worker" threads to monitor multiple ports (21, 4444, 7777, etc.) simultaneously without blocking the main engine.

Heuristic Detection: Tracks unique port hits per IP address. If an IP exceeds a threshold (3+ ports), it is flagged with a HIGH severity "PORT SCAN" event.

Signature Engine: Analyzes raw hex payloads using bitwise logic to identify malicious TCP flag combinations, such as Null Scans and SYN-FIN Anomalies.

JSON Logging: All security events are structured in JSON format for easy ingestion into SIEM tools like Microsoft Sentinel or Splunk.

🛠️ System Architecture
The system follows a classic Sensor-Analyzer-Logger pipeline:

Sensor (socket.py): Background workers listen for incoming TCP handshakes.

Analyzer (anal_pack): Captures the raw hex payload and compares it against signatures.json.

Logger (log_event): Writes a thread-safe entry to ids_log.json using threading.Lock.

📂 Project Structure
nids_v3.py: The main detection engine and multi-threaded listener.

signatures.json: The "Threat Intelligence" file containing known malicious byte patterns.

offense.py: A testing utility to simulate TCP attacks and verify engine alerts.

ids_log.json: The persistent log file for security incidents.

🚦 How to Run
Prerequisites
Linux Environment (Tested on Kali Linux)

Python 3.x

Root/Sudo privileges (Required to bind to privileged ports like 21)

Execution
Start the NIDS Engine:

Bash
sudo python3 nids_v3.py
Launch a Simulation (New Terminal):

Bash
python3 offense.py
📊 Sample Detection Log
JSON

{
  "timestamp": "2026-04-03 20:05:12.441",
  
  "attacker_ip": "127.0.0.1",
  
  "target_port": 7777,
  
  "event_type": "PORT SCAN",
  
  "severity": "HIGH"
  
}
🛡️ Security Alignment (SC-900 / AZ-500)
This project implements core Zero Trust principles by:

Verifying Explicitly: Inspecting every packet payload rather than just trusting the connection.

Least Privilege: Monitoring restricted ports and flagging lateral movement attempts.

Logging & Monitoring: Providing the raw data necessary for incident response and digital forensics.
