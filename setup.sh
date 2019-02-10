# Go to home directory.
cd

# email_specs.json.
if [[ ! -f "${HOME}/email_specs.json" ]]; then
  echo "Please create email specs!" && exit 1
fi

# corpora.
if [[ ! -d "${HOME}/corpora" ]]; then
  echo "Please obtain corpora!" && exit 1
fi

# english-to-arabic-machine-translation.
if [[ ! -d "${HOME}/english-to-arabic-machine-translation" ]]; then
  git clone https://github.com/bishoyboshra/english-to-arabic-machine-translation.git
fi

# nmt.
if [[ ! -d "${HOME}/nmt" ]]; then
  git clone https://github.com/tensorflow/nmt.git
fi

NMT_INIT="${HOME}/nmt/__init__.py"
if [[ ! -f  "${NMT_INIT}" ]]; then
  touch "${NMT_INIT}"
fi

# Disable power-saving options, to keep the internet working.
echo "TODO:
su - mluser
sudo iwconfig wlp3s0 power off
sudo systemctl stop NetworkManager.service
sudo systemctl disable NetworkManager.service
exit"
