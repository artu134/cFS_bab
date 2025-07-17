#!/usr/bin/env python3
"""
Test script for SAMPLE_APP movement commands
Demonstrates how to send movement commands and verify telemetry
"""

import struct
import socket
import time

# cFS Configuration (adjust these to match your system)
CFS_IP = "127.0.0.1"  # localhost
CFS_CMD_PORT = 1234   # Command port (adjust as needed)
CFS_TLM_PORT = 1235   # Telemetry port (adjust as needed)

# Message IDs (these would come from your build configuration)
SAMPLE_APP_CMD_MID = 0x1882      # Sample app command MID
SAMPLE_APP_HK_TLM_MID = 0x0883   # Sample app telemetry MID

# Function codes
SAMPLE_APP_MOVEMENT_CC = 4       # Movement command code

class MovementCommandTest:
    def __init__(self):
        self.cmd_socket = None
        self.tlm_socket = None
    
    def create_movement_command(self, x, y, z):
        """
        Create a movement command packet
        Structure: CFE_MSG_CommandHeader_t + MovementCmd_Payload_t
        """
        # CFE Message Header (simplified)
        stream_id = SAMPLE_APP_CMD_MID
        length = 32  # Header + 3 doubles (8 bytes each)
        sequence = 0
        seconds = int(time.time())
        subsecs = 0
        function_code = SAMPLE_APP_MOVEMENT_CC
        checksum = 0
        
        # Pack the command header (this is a simplified version)
        header = struct.pack('>HHHHHBB', 
                           stream_id,    # StreamId
                           length,       # Length
                           sequence,     # Sequence
                           seconds,      # Seconds
                           subsecs,      # Subseconds
                           function_code, # Function Code
                           checksum)     # Checksum
        
        # Pack the movement payload (3 doubles)
        payload = struct.pack('>ddd', x, y, z)
        
        return header + payload
    
    def send_command(self, x, y, z):
        """Send a movement command"""
        try:
            cmd_data = self.create_movement_command(x, y, z)
            print(f"\n=== SENDING MOVEMENT COMMAND ===")
            print(f"Target: {CFS_IP}:{CFS_CMD_PORT}")
            print(f"X: {x:.6f}")
            print(f"Y: {y:.6f}")
            print(f"Z: {z:.6f}")
            print(f"Command size: {len(cmd_data)} bytes")
            print(f"Function Code: {SAMPLE_APP_MOVEMENT_CC}")
            
            # Create UDP socket and send command
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.sendto(cmd_data, (CFS_IP, CFS_CMD_PORT))
                print("✓ Command sent successfully!")
                
        except Exception as e:
            print(f"✗ Error sending command: {e}")
    
    def listen_for_telemetry(self, timeout=5):
        """Listen for telemetry response"""
        try:
            print(f"\n=== LISTENING FOR TELEMETRY ===")
            print(f"Listening on port {CFS_TLM_PORT} for {timeout} seconds...")
            
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.bind(('', CFS_TLM_PORT))
                sock.settimeout(timeout)
                
                data, addr = sock.recvfrom(1024)
                print(f"✓ Received telemetry from {addr}")
                print(f"Data length: {len(data)} bytes")
                
                # Try to parse the telemetry (simplified)
                if len(data) >= 32:  # Minimum expected size
                    # Skip header, extract payload (assuming it starts at byte 16)
                    payload_start = 16
                    if len(data) >= payload_start + 24:  # 3 doubles = 24 bytes
                        cmd_counter, err_counter = struct.unpack('>BB', data[payload_start:payload_start+2])
                        x, y, z = struct.unpack('>ddd', data[payload_start+4:payload_start+28])
                        
                        print(f"Command Counter: {cmd_counter}")
                        print(f"Error Counter: {err_counter}")
                        print(f"Current X: {x:.6f}")
                        print(f"Current Y: {y:.6f}")
                        print(f"Current Z: {z:.6f}")
                        return True
                
        except socket.timeout:
            print("⚠ Timeout waiting for telemetry")
        except Exception as e:
            print(f"✗ Error receiving telemetry: {e}")
        
        return False
    
    def run_test(self):
        """Run the complete test"""
        print("=" * 60)
        print("SAMPLE_APP MOVEMENT COMMAND TEST")
        print("=" * 60)
        
        test_coordinates = [
            (1.5, 2.7, 3.9),
            (-10.123, 25.456, 0.0),
            (100.0, -50.0, 75.25)
        ]
        
        for i, (x, y, z) in enumerate(test_coordinates, 1):
            print(f"\n🧪 TEST CASE {i}")
            self.send_command(x, y, z)
            
            # Wait a moment for processing
            time.sleep(1)
            
            # Listen for telemetry response
            if self.listen_for_telemetry():
                print("✓ Test case passed!")
            else:
                print("⚠ No telemetry received")
            
            print("-" * 40)

def show_cfs_launch_instructions():
    """Show instructions for launching cFS"""
    print("\n" + "=" * 60)
    print("CFS LAUNCH INSTRUCTIONS")
    print("=" * 60)
    
    print("\n1. BUILD THE CFS SYSTEM:")
    print("   cd /home/administrator/sats/cFS_bab/build/i686-linux-gnu/default_cpu1")
    print("   make")
    
    print("\n2. LAUNCH THE CFS CORE:")
    print("   cd /home/administrator/sats/cFS_bab/build/i686-linux-gnu/default_cpu1/cpu1")
    print("   ./core-cpu1")
    
    print("\n3. VERIFY SAMPLE_APP IS LOADED:")
    print("   Look for these messages in the cFS output:")
    print("   - 'Sample App Initialized'")
    print("   - App loading messages")
    
    print("\n4. CONFIGURE NETWORKING (if needed):")
    print("   Edit the cFS configuration files to set:")
    print("   - Command input port (TO_LAB)")
    print("   - Telemetry output port (CI_LAB)")
    
    print("\n5. RUN THIS TEST SCRIPT:")
    print("   python3 test_movement.py")
    
    print("\n6. MONITOR CFS OUTPUT:")
    print("   Watch for event messages like:")
    print("   'SAMPLE_APP: Movement command received - X=1.500000, Y=2.700000, Z=3.900000'")

def show_manual_test_commands():
    """Show manual commands for testing"""
    print("\n" + "=" * 60)
    print("MANUAL TESTING WITH CMDUTIL")
    print("=" * 60)
    
    print("\n1. Navigate to cmdUtil directory:")
    print("   cd /home/administrator/sats/cFS_bab/build/tools/cFS-GroundSystem/Subsystems/cmdUtil")
    
    print("\n2. Send a movement command:")
    print("   ./cmdUtil --host=127.0.0.1 --port=1234 \\")
    print("            --mid=0x1882 --cc=4 \\")
    print("            --file=movement_cmd.dat")
    
    print("\n3. Create movement_cmd.dat with hex data:")
    print("   # X=1.5, Y=2.7, Z=3.9 as IEEE 754 doubles")
    print("   echo '3FF8000000000000 4005999999999999 400F333333333333' | xxd -r -p > movement_cmd.dat")
    
    print("\n4. Monitor telemetry:")
    print("   Look for housekeeping telemetry packets")
    print("   Check event messages for confirmation")

if __name__ == "__main__":
    # Show launch instructions first
    show_cfs_launch_instructions()
    show_manual_test_commands()
    
    # Ask if user wants to run the test
    print("\n" + "=" * 60)
    response = input("Do you want to run the movement command test now? (y/n): ")
    
    if response.lower() == 'y':
        test = MovementCommandTest()
        test.run_test()
    else:
        print("Test skipped. Launch cFS first, then run this script again.")
