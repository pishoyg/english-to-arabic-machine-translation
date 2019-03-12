# Set default values.
# Directory where Stanford CoreNLP is installed.
INSTALL_DIR="stanford-corenlp-full-2018-10-05"
# Path to language model.
MODEL="stanford-arabic-corenlp-2018-10-05-models/edu/stanford/nlp/models/segmenter/arabic/arabic-segmenter-atb+bn+arztrain.ser.gz"
# Corpus prefix. That is, corpus path missing the language extension.
CORPUS_PREFIX=""
# Language extension.
LANGUAGE="ara"
# Language extension according to the Stanford CoreNLP program.
TOKENIZE_LANGUAGE="ar"
# Temporary work directory.
WORK_DIR="/tmp/tmp"
# Output extension.
EXTENSION="stanford"

# Parsing flags.
while [ $# -gt 0 ]; do
  case "${1}" in
    --install_dir=*)
      INSTALL_DIR="${1#*=}"
      ;;
    --model=*)
      MODEL="${1#*=}"
      ;;
    --corpus_prefix=*)
      CORPUS_PREFIX="${1#*=}"
      ;;
    --language=*)
      LANGUAGE="${1#*=}"
      ;;
    --tokenize_language=*)
      TOKENIZE_LANGUAGE="${1#*=}"
      ;;
    --work_dir=*)
      WORK_DIR="${1#*=}"
      ;;
    --extension=*)
      EXTENSION="${1#*=}"
      ;;
    *)
      echo "Unknown flag: ${1}" && exit 1
  esac
  shift
done

# Set up Stanford CoreNLP tool
cd "${INSTALL_DIR}"

for file in `find . -name "*.jar"`; do
  export CLASSPATH="$CLASSPATH:`realpath $file`";
done

for file in `find . -name "*.jar"`; do
  export CLASSPATH="$CLASSPATH:`realpath $file`";
done

cd

# Input validation.
if [[ -z "${CORPUS_PREFIX}.${LANGUAGE}" ]]; then
  echo "\${CORPUS_PREFIX}.\${LANGUAGE}: ${CORPUS_PREFIX}.${LANGUAGE} nonexistent!" && exit 1
fi
if [[ -d "${WORK_DIR}" ]]; then
  echo "\${WORK_DIR}: ${WORK_DIR} exists." && exit 1
fi
if [[ "${EXTENSION}" == "${LANGUAGE}" ]] ||
    [[ "${EXTENSION}" == "split" ]] ||
    [[ "${LANGUAGE}" == "split" ]]; then
  echo "Extension and Language must be nonequal, and neither can be 'split'." && exit 1
fi

# Make operations visible to user.
set -o xtrace

mkdir -p "${WORK_DIR}"
cp "${CORPUS_PREFIX}.${LANGUAGE}" "${WORK_DIR}" || exit 1
WORK_DIR_CORPUS="${WORK_DIR}/$(basename ${CORPUS_PREFIX}.${LANGUAGE})"
sed -i 's/\./ /g' "${WORK_DIR_CORPUS}" || exit 1
sed -i ':a;N;$!ba;s/\n/\.\n/g' "${WORK_DIR_CORPUS}" || exit 1

split \
  --suffix-length=7 \
  --additional-suffix=".split" \
  --lines=1000 \
  "${WORK_DIR_CORPUS}" \
  "${WORK_DIR}/tmp-" \
   || exit 1

java \
  -mx3g \
  edu.stanford.nlp.pipeline.StanfordCoreNLP \
  -file "${WORK_DIR}" \
  -extension ".split" \
  -outputExtension ".${EXTENSION}" \
  -outputFormat "conll" \
  -output.prettyPrint false \
  -outputDirectory "${WORK_DIR}" \
  -output.columns word \
  -annotators tokenize,ssplit \
  -tokenize.language "${TOKENIZE_LANGUAGE}" \
  -ssplit.eolonly true \
  -segment.model "${MODEL}" \
  -replaceExtension true \
  || exit 1


FINAL="${WORK_DIR}/$(basename ${CORPUS_PREFIX}).${EXTENSION}.${LANGUAGE}"

cat ${WORK_DIR}/tmp-*.${EXTENSION} > "${FINAL}"

sed -i ':a;N;$!ba;s/\./\n/g' "${FINAL}"
sed -i ':a;N;$!ba;s/\n\n/\n/g' "${FINAL}"

cp "${FINAL}" "$(dirname ${CORPUS_PREFIX})"

rm -r "${WORK_DIR}"

