#!/bin/bash

stdout=$(python3.10 -c 'import sys; print(sys.version)' 2>&1)
echo $stdout
if echo "$stdout" | grep -q "command not found"; then
    echo "ERROR: python 3.10 is not installed."
else
    if echo "$stdout" | grep -q "3.10"; then
        echo "\n\n=> python 3.10 installed successfully.\n\n"
        ./test-py3.10.sh
    fi
fi

stdout=$(python3.11 -c 'import sys; print(sys.version)' 2>&1)
if echo "$stdout" | grep -q "command not found"; then
    echo "ERROR: python 3.11 is not installed."
else
    if echo "$stdout" | grep -q "3.11"; then
        echo -e "\n\n=> python 3.11 installed successfully.\n\n"
        ./test-py3.11.sh
    fi
fi

#echo $stdout

