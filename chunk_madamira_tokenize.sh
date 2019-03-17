## FLAGS.
# Input test set containing sentences in Arabic, one per line.
INPUT_FILE=""
# Output file containing tokenized sentences, one per line.
# Defaults to "${INPUT_FILE}.madamira" if not set.
OUTPUT_FILE=""
# Temporary work directory. It's preferred for it to be nonexistent.
WORK_DIR="${HOME}/tmp/chunk_madamira_tokenize"
# Size of each chunk, in number of sentences.
CHUNK_SIZE="100000"
# MADAMIRA jar.
MADAMIRA_JAR="MADAMIRA-release-20170403-2.1/MADAMIRA-release-20170403-2.1.jar"
# MADAMIRA config.
MADAMIRA_RAWCONFIG="MADAMIRA-release-20170403-2.1/samples/sampleConfigFile.xml"

# Parsing flags.
while [ $# -gt 0 ]; do
  case "${1}" in
    --input_file=*)
      INPUT_FILE="${1#*=}"
      ;;
    --output_file=*)
      OUTPUT_FILE="${1#*=}"
      ;;
    --work_dir=*)
      WORK_DIR="${1#*=}"
      ;;
    --chunk_size=*)
      CHUNK_SIZE="${1#*=}"
      ;;
    --madamira_jar=*)
      MADAMIRA_JAR="${1#*=}"
      ;;
    --madamira_rawconfig=*)
      MADAMIRA_RAWCONFIG="${1#*=}"
      ;;
    *)
      echo "Unknown flag: ${1}" && exit 1
  esac
  shift
done

# Input validation and preprocessing.
if [[ -d "${WORK_DIR}" ]]; then
  echo "WARNING: \${WORK_DIR}: ${WORK_DIR} exists."
else
  # Create work directory if nonexistent.
  mkdir -p "${WORK_DIR}" || exit 1
fi
if [[ -z "${OUTPUT_FILE}" ]]; then
  # Assign default value to OUTPUT_FILE, if not set by flags.
  OUTPUT_FILE="${INPUT_FILE}.madamira"
fi


## MAIN
# Make operations visible to user.
set -o xtrace

# Chunk the input dataset, potentially overriding already existing chunks.
split \
  --numeric-suffixes=0 \
  --suffix-length=7 \
  --additional-suffix=".split" \
  --lines="${CHUNK_SIZE}" \
  "${INPUT_FILE}" \
  "${WORK_DIR}/tmp-" \
   || exit 1

# Tokenize each chunk separately.
for CHUNK in $(ls ${WORK_DIR}/tmp-*.split); do
  OUT_CHUNK="${CHUNK}.MyD3.tok"
  # Check if the output chunk exists, and whether it has the expected
  # number of lines to ensure it's not partially written.
  if [[ ! -f ${OUT_CHUNK} ]] ||
      [[ $(wc ${OUT_CHUNK} | awk '{print $1}') != $(wc ${CHUNK} | awk '{print $1}') ]]; then
    # Tokenize.
    java \
        -Xmx2500m \
        -Xms2500m \
        -XX:NewRatio=3 \
        -jar "${MADAMIRA_JAR}" \
        -rawinput "${CHUNK}" \
        -rawoutdir "${WORK_DIR}" \
        -rawconfig "${MADAMIRA_RAWCONFIG}" \
      || exit 1
  fi
done

cat ${WORK_DIR}/tmp-*.split.MyD3.tok > "${OUTPUT_FILE}" || exit 1

echo "WARNING: \${WORK_DIR}: ${WORK_DIR} needs to be cleaned up manually."
