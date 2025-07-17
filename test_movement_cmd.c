/*
** Simple test program to demonstrate sending movement commands to sample_app
** and reading the telemetry response
*/

#include <stdio.h>
#include <string.h>
#include <stdint.h>

/* Mock the basic cFS structures for demonstration */
typedef struct {
    uint16_t streamId;
    uint16_t length;
    uint16_t sequence;
    uint8_t  seconds;
    uint16_t subsecs;
} CFE_MSG_CommandHeader_t;

typedef struct {
    double x_coord;
    double y_coord; 
    double z_coord;
} SAMPLE_APP_MovementCmd_Payload_t;

typedef struct {
    CFE_MSG_CommandHeader_t           CommandHeader;
    SAMPLE_APP_MovementCmd_Payload_t  Payload;
} SAMPLE_APP_MovementCmd_t;

typedef struct {
    uint8_t CommandErrorCounter;
    uint8_t CommandCounter;
    uint8_t spare[2];
    double current_x;
    double current_y;
    double current_z;
} SAMPLE_APP_HkTlm_Payload_t;

/* Function to simulate sending a movement command */
void send_movement_command(double x, double y, double z) {
    SAMPLE_APP_MovementCmd_t cmd;
    
    printf("\n=== SENDING MOVEMENT COMMAND ===\n");
    printf("Command: SAMPLE_APP_MOVEMENT_CC (Function Code 4)\n");
    printf("X Coordinate: %.6f\n", x);
    printf("Y Coordinate: %.6f\n", y);
    printf("Z Coordinate: %.6f\n", z);
    
    /* Populate the command structure */
    memset(&cmd, 0, sizeof(cmd));
    cmd.Payload.x_coord = x;
    cmd.Payload.y_coord = y;
    cmd.Payload.z_coord = z;
    
    printf("Command Size: %zu bytes\n", sizeof(cmd));
    printf("Payload Size: %zu bytes\n", sizeof(cmd.Payload));
    printf("\nThis command would be sent via CFE_SB_TransmitMsg() to MID: SAMPLE_APP_CMD_MID\n");
}

/* Function to simulate receiving telemetry */
void simulate_telemetry_response(double x, double y, double z) {
    SAMPLE_APP_HkTlm_Payload_t tlm;
    
    printf("\n=== TELEMETRY RESPONSE ===\n");
    printf("Housekeeping Telemetry from sample_app:\n");
    
    /* Simulate the telemetry response */
    tlm.CommandCounter = 1;
    tlm.CommandErrorCounter = 0;
    tlm.current_x = x;
    tlm.current_y = y;
    tlm.current_z = z;
    
    printf("Command Counter: %d\n", tlm.CommandCounter);
    printf("Error Counter: %d\n", tlm.CommandErrorCounter);
    printf("Current X: %.6f\n", tlm.current_x);
    printf("Current Y: %.6f\n", tlm.current_y);
    printf("Current Z: %.6f\n", tlm.current_z);
    printf("Telemetry Size: %zu bytes\n", sizeof(tlm));
}

int main() {
    printf("=== SAMPLE APP MOVEMENT COMMAND TEST ===\n");
    printf("This demonstrates the external command interface for setting coordinates\n");
    
    /* Test Case 1: Move to position 1.5, 2.7, 3.9 */
    send_movement_command(1.5, 2.7, 3.9);
    simulate_telemetry_response(1.5, 2.7, 3.9);
    
    printf("\n" "==================================================\n");
    
    /* Test Case 2: Move to position -10.123, 25.456, 0.0 */
    send_movement_command(-10.123, 25.456, 0.0);
    simulate_telemetry_response(-10.123, 25.456, 0.0);
    
    printf("\n=== HOW TO USE IN REAL cFS SYSTEM ===\n");
    printf("1. Build and run the cFS system with the modified sample_app\n");
    printf("2. Send commands using ground station software or cmdUtil:\n");
    printf("   - Message ID: SAMPLE_APP_CMD_MID\n");
    printf("   - Function Code: 4 (SAMPLE_APP_MOVEMENT_CC)\n");
    printf("   - Payload: 24 bytes (3 doubles for x, y, z)\n");
    printf("3. Subscribe to telemetry MID: SAMPLE_APP_HK_TLM_MID\n");
    printf("4. Coordinate values will appear in housekeeping telemetry\n");
    printf("5. Event messages will show received coordinates\n");
    
    return 0;
}
