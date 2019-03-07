set -o xtrace

sudo apt install python3-pip
sudo apt install git
sudo apt install python3-tk
sudo apt install virtualenv
# python-pip
# sudo apt install cuda-9.0
# sudo apt-get install default-jre

if [[ ! -f /etc/apt/sources.list.d/google-chrome.list ]]; then
  wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  sudo dpkg -i google-chrome-stable_current_amd64.deb
fi
