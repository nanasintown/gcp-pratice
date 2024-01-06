#!/bin/bash
echo -e "##################################################################################\n\n"
echo -e "TEST: Python version\n" 
python3.11 -c 'import sys; print(sys.version)'

echo -e "\n\n##################################################################################\n\n"
echo -e "TEST: Dependencies installation\n" 
pip3 install -r ./audio_tag/requirements.txt

echo -e "\n\n##################################################################################\n\n"
echo -e "TEST: Application compilation\n" 
python3.11 -m compileall ./audio_tag

echo -e "\n\n##################################################################################\n\n"
cd ./audio_tag
echo -e "TEST: pytest\n" 
python3.11 -m pytest

echo -e "\n\n##################################################################################\n\n"
cd ../notebooks
echo -e "TEST: pytest with notebooks\n" 
python3.11 -m pytest --nbmake

echo -e "\n\n##################################################################################\n\n"
cd ../audio_tag
echo -e "TEST: pylint\n" 
pylint tagreader.py

echo -e "\n\n##################################################################################\n\n"
cd /application
echo -e "TEST: Wheel building\n" 
python3.11 setup.py sdist; pip3 install .
