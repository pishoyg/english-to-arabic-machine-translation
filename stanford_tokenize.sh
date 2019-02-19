# Set default values.
INSTALL_DIR="stanford-corenlp-full-2018-10-05"
MODEL="stanford-arabic-corenlp-2018-10-05-models/edu/stanford/nlp/models/segmenter/arabic/arabic-segmenter-atb+bn+arztrain.ser.gz"
INPUT_PATH=""
LANGUAGE="ara"
WORK_DIR="/tmp/tmp"
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
    --input_path=*)
      INPUT_PATH="${1#*=}"
      ;;
    --language=*)
      LANGUAGE="${1#*=}"
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
if [[ -z "${INPUT_PATH}.${LANGUAGE}" ]]; then
  echo "Input file nonexistent!" && exit 1
fi
if [[ -d "${WORK_DIR}" ]]; then
  echo "Work directory must be nonexistent." && exit 1
fi

# Make operations visible to user.
set -o xtrace

mkdir -p "${WORK_DIR}"
cp "${INPUT_PATH}.${LANGUAGE}" "${WORK_DIR}" || exit 1
WORK_DIR_CORPUS="${WORK_DIR}/$(basename ${INPUT_PATH}.${LANGUAGE})"
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
  -tokenize.language ar \
  -ssplit.eolonly true \
  -segment.model "${MODEL}" \
  -replaceExtension true \
  || exit 1


FINAL="${WORK_DIR}/$(basename ${INPUT_PATH}).${EXTENSION}.${LANGUAGE}"

cat ${WORK_DIR}/tmp-*.${EXTENSION} > "${FINAL}"

sed -i ':a;N;$!ba;s/\./\n/g' "${FINAL}"
sed -i ':a;N;$!ba;s/\n\n/\n/g' "${FINAL}"

cp "${FINAL}" "$(dirname ${INPUT_PATH})"
