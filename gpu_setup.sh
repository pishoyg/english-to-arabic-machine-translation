set -o xtrace
virtualenv -p python3 thesis_env
source thesis_env/bin/activate
pip3 install tensorflow-gpu==1.12.0