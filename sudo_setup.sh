set -o xtrace

# TODO: Install pip.
# TODO: Install tf-nightly.
# TODO: Install git.

sudo apt-get install default-jre
sudo apt install python-pip
pip install tf-nightly
sudo apt install git

# Disable power-saving options, to keep the internet working (optional).
echo "TODO:
sudo iwconfig wlp3s0 power off
sudo systemctl stop NetworkManager.service
sudo systemctl disable NetworkManager.service"
