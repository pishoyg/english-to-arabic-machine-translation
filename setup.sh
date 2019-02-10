# Go to home directory.
cd

# email_specs.json.
EMAIL_SPECS="${HOME}/email_specs.json"
if [[ ! -f "${HOME}/email_specs.json" ]]; then
  echo "Please create ${EMAIL_SPECS}" && exit 1
fi

# corpora.
CORPORA="${HOME}/corpora"
if [[ ! -d "${CORPORA}" ]]; then
  echo "Please create ${CORPORA}" && exit 1
fi

# nmt.
if [[ ! -d ${HOME}/nmt ]]; then
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
exit"
