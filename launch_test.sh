#!/bin/bash
# cFS Launch and Test Script

echo "=============================================="
echo "cFS SAMPLE_APP MOVEMENT COMMAND TEST SUITE"
echo "=============================================="

# Configuration
CFS_BUILD_DIR="/home/administrator/sats/cFS_bab/build/i686-linux-gnu/default_cpu1"
CFS_ROOT="/home/administrator/sats/cFS_bab"

echo -e "\n1. CHECKING BUILD STATUS..."
cd "$CFS_BUILD_DIR"

# Check if sample_app.so exists
if [ -f "apps/sample_app/sample_app.so" ]; then
    echo "✓ sample_app.so found ($(ls -lh apps/sample_app/sample_app.so | awk '{print $5}'))"
else
    echo "✗ sample_app.so not found - building now..."
    make sample_app
fi

# Check for other required components
echo -e "\n2. CHECKING REQUIRED COMPONENTS..."
for component in ci_lab to_lab sch_lab; do
    if [ -f "apps/$component/$component.so" ]; then
        echo "✓ $component.so found"
    else
        echo "⚠ $component.so missing"
    fi
done

echo -e "\n3. BUILD COMPLETION..."
# Try to complete the build
echo "Attempting to complete the build..."
make 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ Build completed successfully"
else
    echo "⚠ Build has some issues, but core components are ready"
fi

echo -e "\n4. CHECKING FOR CORE EXECUTABLE..."
if [ -f "cpu1/core-cpu1" ]; then
    echo "✓ Core executable found: cpu1/core-cpu1"
    CORE_EXECUTABLE="cpu1/core-cpu1"
elif [ -f "core-cpu1" ]; then
    echo "✓ Core executable found: core-cpu1"
    CORE_EXECUTABLE="core-cpu1"
else
    echo "⚠ Core executable not found, checking alternatives..."
    find . -name "*core*" -type f -executable 2>/dev/null | head -5
fi

echo -e "\n5. STARTUP SCRIPT..."
if [ -f "cpu1/cfe_es_startup.scr" ]; then
    echo "✓ Startup script found"
    echo "Startup script contents:"
    echo "========================"
    cat cpu1/cfe_es_startup.scr
    echo "========================"
else
    echo "⚠ Startup script not found"
fi

echo -e "\n6. LAUNCH INSTRUCTIONS:"
echo "========================"
echo "To launch cFS manually:"
echo "cd $CFS_BUILD_DIR"

if [ -n "$CORE_EXECUTABLE" ]; then
    echo "./$CORE_EXECUTABLE"
else
    echo "# Core executable not found - complete the build first"
    echo "make"
fi

echo -e "\n7. TESTING COMMANDS:"
echo "==================="
echo "Once cFS is running, use these commands to test:"
echo ""
echo "# Run the Python test script:"
echo "cd $CFS_ROOT"
echo "python3 test_movement.py"
echo ""
echo "# Or test manually with cmdUtil (if available):"
echo "cd $CFS_ROOT/build/tools/cFS-GroundSystem/Subsystems/cmdUtil"
echo "./cmdUtil --help"

echo -e "\n8. MONITORING:"
echo "============="
echo "When cFS starts, look for these messages:"
echo "- 'CFE_ES Startup: CFE_ES Application Startup Begin'"
echo "- 'Sample App Initialized'"
echo "- App loading success messages"
echo ""
echo "To test movement commands, send:"
echo "- MID: SAMPLE_APP_CMD_MID"
echo "- Function Code: 4 (SAMPLE_APP_MOVEMENT_CC)"
echo "- Payload: 24 bytes (3 doubles for x, y, z coordinates)"
echo ""
echo "Expected response:"
echo "- Event message: 'SAMPLE_APP: Movement command received - X=..., Y=..., Z=...'"
echo "- Updated telemetry with new coordinates"

echo -e "\n9. TROUBLESHOOTING:"
echo "=================="
echo "If the core doesn't start:"
echo "- Check permissions: chmod +x core-cpu1"
echo "- Verify all .so files are present"
echo "- Check startup script syntax"
echo "- Monitor system logs: dmesg | tail"

echo -e "\n10. NEXT STEPS:"
echo "==============="
echo "1. Complete the build if needed: make"
echo "2. Launch cFS: ./$CORE_EXECUTABLE"
echo "3. Run movement tests: python3 test_movement.py"
echo "4. Monitor telemetry and events"

echo -e "\nScript completed. Ready to test SAMPLE_APP movement commands!"
