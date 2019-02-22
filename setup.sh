# Rather-personalized script for setting up work environment.
# WARNING: This is not meant for generic use. It's rather a guide
#          pointing out to what your machine should have in order
#          to be able to run training.


# Go to home directory.
cd

# Flags.
while [ $# -gt 0 ]; do
  case "${1}" in
    --git_user_email=*)
      GIT_USER_EMAIL="${1#*=}"
      ;;
    --git_user_name=*)
      GIT_USER_NAME="${1#*=}"
      ;;
    *)
      echo "Unknown flag: ${1}" && exit 1
  esac
  shift
done

# Make operations visible to user.
set -o xtrace

pip3 install \
  tensorflow \
  tf-nightly \
#  tensorflow-gpu \
#  tf-nightly-gpu

# english-to-arabic-machine-translation.
EAMT="${HOME}/english-to-arabic-machine-translation"
if [[ ! -d "${EAMT}" ]]; then
  git clone https://github.com/bishoyboshra/english-to-arabic-machine-translation.git
fi
cd "${EAMT}"
git pull origin master
cd

# GitHub account (optional).
if [[ ! -z ${GIT_USER_EMAIL} ]]; then
  git config --global user.email ${GIT_USER_EMAIL}
fi
if [[ ! -z ${GIT_USER_NAME} ]]; then
  git config --global user.name ${GIT_USER_NAME}
fi

# nmt.
if [[ ! -d "${HOME}/nmt" ]]; then
  git clone https://github.com/tensorflow/nmt.git
fi

NMT_INIT="${HOME}/nmt/__init__.py"
if [[ ! -f  "${NMT_INIT}" ]]; then
  touch "${NMT_INIT}"
fi

# email_specs.json.
if [[ ! -f "${HOME}/email_specs.json" ]]; then
  echo "Please create email specs!" && MISSING_DATA=true
fi

# corpora.
if [[ ! -d "${HOME}/corpora" ]]; then
  echo "Please obtain corpora!"  && MISSING_DATA=true
fi

if [[ -z "${MISSING_DATA}" ]]; then
  echo "SUCCESS"
fi
