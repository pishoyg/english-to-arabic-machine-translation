# Set default values.
INSTALL_DIR="stanford-corenlp-full-2018-10-05"
INPUT_PATH=""
EXTENSION="stanford"
# Parsing flags.
while [ $# -gt 0 ]; do
  case "${1}" in
    --install_dir=*)
      INSTALL_DIR="${1#*=}"
      ;;
    --input_path=*)
      INPUT_PATH="${1#*=}"
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
if [[ -z ${INPUT_PATH} ]]; then
  echo "Input file nonexistent!" && exit 1
fi

# Make operations visible to user.
set -o xtrace

java \
  -mx3g \
  edu.stanford.nlp.pipeline.StanfordCoreNLP \
  -file "${INPUT_PATH}" \
  -outputExtension ".${EXTENSION}" \
  -outputFormat "conll" \
  -outputDirectory "$(dirname ${INPUT_PATH})" \
  -ssplit.eolonly true \
  -output.prettyPrint false \
  -output.columns word \
  -annotators tokenize,ssplit \
  -tokenize.language ar \
  -segment.model "stanford-corenlp-full-2018-10-05/edu/stanford/nlp/models/segmenter/arabic/arabic-segmenter-atb+bn+arztrain.ser.gz" \
  || exit 1

sed -i 's/\./\n/g' "${INPUT_PATH}.${EXTENSION}"

