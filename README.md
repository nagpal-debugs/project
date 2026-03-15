​🛡️ Project Vajra:Offline Police Emergency System
​Developed for Electrothon 2026 Team Location: NIT Hamirpur
​📌 Project Overview
​Rakshak is a dedicated hardware safety device designed to provide an instant, offline link to local police stations. Unlike mobile apps that require internet connectivity and screen interaction, Rakshak uses a physical "Panic Button" to send GPS coordinates via GSM (SMS) to a centralized police dashboard.
​Why Rakshak?
​Zero Internet Dependency: Works in remote areas using 2G/GSM.
​One-Touch Response: No need to unlock phones or open apps.
​Real-time Mapping: Automatically opens coordinates on the Police Station's portal.
​🛠️ Hardware Stack
​Microcontroller: Arduino Uno
​Shield: Arduino Base Shield (for modular connections)
​Modules (Planned): SIM800L (GSM) & NEO-6M (GPS)
​Triggers: 2x Tactile Push Buttons (Emergency & System Check)
​Wires: Male-to-Male, Female-to-Female, and Male-to-Female Jumper Wires.
​💻 Software Architecture
​The system utilizes a Full-Stack Serial Bridge:
​Firmware (C++): An interrupt-driven Arduino script that monitors button states and handles serial data transmission.
​Bridge (Python/PySerial): A script that acts as the "GSM Modem," listening to the hardware via the COM port and processing the SOS signal.
​Dashboard (Python/Webbrowser): A software handler that automatically triggers visualization (Google Maps) for the dispatcher.
​🚀 Installation & Setup
​1. Arduino Setup
​Connect the Red Button to Pin D2 and GND.
​Connect the Green Button to Pin D3 and GND.
​Upload the rakshak_trigger.ino code to your Arduino Uno.
​2. Python Setup