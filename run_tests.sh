#!/bin/bash

# Navigate to project directory
cd /Users/parthverma/quantium-starter-repo

# Activate virtual environment
source venv/bin/activate

# Run the test suite
pytest test_app.py -v

# Capture pytest exit code
EXIT_CODE=$?

# Return appropriate exit code
if [ $EXIT_CODE -eq 0 ]; then
    echo "All tests passed!"
    exit 0
else
    echo "Tests failed!"
    exit 1
fi