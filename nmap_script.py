#!/usr/bin/python3  # Shebang to specify the Python 3 interpreter

import nmap  # Import the python-nmap module for using Nmap via Python

# Function to display a welcome banner
def display_welcome():
    print("""
    ****************************************
    *        Nmap Scanner Project           *
    ****************************************
    """)

# Function to get the IP address from the user
def get_ip_address():
    return input("Please Enter the IP Address to Scan: ")

# Function to ask user which scan type they want to run
def get_scan_type():
    print('''\nPlease Enter the type of scan you wish to perform:
    1. SYN Scan
    2. UDP Scan
    3. Comprehensive Scan''')
    return input("Choose (1/2/3): ")

# Function to perform the scan based on user's input
def perform_scan(ip_addr, scan_type):
    sc = nmap.PortScanner()  # Create a PortScanner object

    # Dictionary mapping scan types to Nmap arguments and protocol
    scan_options = {
        '1': ['-sS -sV', 'tcp'],               # SYN scan with version detection
        '2': ['-sU -sV', 'udp'],               # UDP scan with version detection
        '3': ['-sS -sV -p- -O -sC', 'tcp']     # Comprehensive scan: full ports, OS detection, scripts
    }

    # Check for valid option
    if scan_type not in scan_options.keys():
        print("Invalid Option. Please restart and choose a valid scan type.")
        return

    # Display Nmap version being used
    print("Nmap Version: ", sc.nmap_version())
    print("Scanning in progress... Please wait.")

    try:
        # Run the scan using the appropriate Nmap arguments
        sc.scan(ip_addr, arguments=scan_options[scan_type][0])

        # Check if host is found
        if ip_addr in sc.all_hosts():
            print("\nHost is Up. Scan Results:")
            proto = scan_options[scan_type][1]  # tcp or udp

            # If the protocol was detected during scan
            if proto in sc[ip_addr].all_protocols():
                # Print header
                print(f"{'Port':<10}{'Service':<20}{'State':<10}")
                print("-" * 40)

                # Loop through ports and display their state and service name
                for port, info in sc[ip_addr][proto].items():
                    print(f"{port:<10}{info['name']:<20}{info['state']:<10}")
            else:
                print("No Open Ports Detected.")
        else:
            print("Host is Down or Unreachable.")

    except Exception as e:
        print(f"An error occurred: {e}")  # Handle unexpected errors

# Main function that controls the flow of the program
def main():
    display_welcome()          # Show welcome banner
    ip_addr = get_ip_address() # Ask user for IP
    scan_type = get_scan_type()# Ask user for scan type
    perform_scan(ip_addr, scan_type)  # Execute scan

# Entry point of the script
if __name__ == "__main__":
    main()
