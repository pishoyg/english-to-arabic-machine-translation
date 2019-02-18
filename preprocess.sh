# Set default values.
INSTALL_DIR="stanford-corenlp-full-2018-10-05"
PROPS="StanfordCoreNLP-arabic.properties"
INPUT_PATH=""
WORK_DIR="/tmp/split_word_dir"
OUT_PREFIX="tmp-0"

# Parsing flags.
while [ $# -gt 0 ]; do
  case "${1}" in
    --install_dir=*)
      INSTALL_DIR="${1#*=}"
      ;;
    --props=*)
      PROPS="${1#*=}"
      ;;
    --input_path=*)
      INPUT_PATH="${1#*=}"
      ;;
    --work_dir=*)
      WORK_DIR="${1#*=}"
      ;;
    --out_prefix=*)
      OUT_PREFIX="${1#*=}"
      ;;
    *)
      echo "Unknown flag: ${1}" && exit 1
  esac
  shift
done

# Input validation.
if [[ -d ${WORD_DIR} ]]; then
  echo "Work directory must be nonexistent." && exit 1
fi
if [[ -z ${INPUT_PATH} ]]; then
  echo "Input file nonexistent!" && exit 1
fi

# Set up Stanford CoreNLP tool
cd "${INSTALL_DIR}"

for file in `find . -name "*.jar"`; do
  export CLASSPATH="$CLASSPATH:`realpath $file`";
done

for file in `find . -name "*.jar"`; do
  export CLASSPATH="$CLASSPATH:`realpath $file`";
done

cd

# Make operations visible to user.
set -o xtrace

# Process input corpus.
mkdir -p "${WORK_DIR}" || exit

split \
  -l 1 \
  -d \
  "${INPUT_PATH}" \
  "${WORK_DIR}/${OUT_PREFIX}" || exit 1

FILELIST="${WORK_DIR}/filelist.txt"
ls -1a ${WORK_DIR}/${OUT_PREFIX}* > "${FILELIST}" || exit 1

java \
  -mx3g \
  edu.stanford.nlp.pipeline.StanfordCoreNLP \
  -filelist "${FILELIST}" \
  -outputFormat "json" \
  -outputExtension ".tokens.json" \
  -outputDirectory "${WORK_DIR}" \
  -props "${INSTALL_DIR}/StanfordCoreNLP-arabic.properties" \
  -annotators "tokenize" \
  -replaceExtension || exit 1

# DO NOT SUBMIT
# rm -r "${WORD_DIR}"
# DO NOT SUBMIT
