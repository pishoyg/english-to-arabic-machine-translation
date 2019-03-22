# Run a model in inference mode, tolerating outrageously large datasets.
#
# INPUT:
# - Trained NMT model.
# - Dataset in source language.
#
# OUTPUT:
# - Inferred translations in target language.
#
# The input is chunked, and chunks are inferred separately in sequence.
# The final output is the concatenation of the translations of the
# chunks.
# In case of failure, inference can be resumed using the same command.
# Chunks that have already been translated won't be regenerated. Chunks
# that are partially written will be detected and overwritten.
#
# Example:
#   bash english-to-arabic-machine-translation/chunk_infer.sh \
#     --out_dir=${NMT_MODEL}/avg_best_bleu \
#     --inference_input_file=UN.clean.eng \
#     --work_dir=tmp/chunk_infer_UN_clean_eng
#
# WARNING: It's highly recommended to choose a clean work directory,
# and to erase it after inference is done.


## FLAGS.

# NMT model output directory.
# Mandatory argument.
OUT_DIR=""

# Input test set containing sentences in source language, one per line.
# Mandatory argument.
INFERENCE_INPUT_FILE=""

# Output file containing translations in target langauge, one per line.
# Defaults to "${OUT_DIR}/$(basename ${INFERENCE_INPUT_FILE}).infer.${TGT}" if
# not set.
INFERENCE_OUTPUT_FILE=""

# Temporary work directory. It's preferred for it to be nonexistent.
# Defaults to "${HOME}/tmp/chunk_infer/$(basename ${INFERENCE_OUTPUT_FILE})"
# if not set.
WORK_DIR=""

# Size of each chunk, in number of sentences.
# Defaults to 100000.
CHUNK_SIZE="100000"

# Target language, to be used as an extension to the output file.
TGT="ara"

# Parsing flags.
while [ $# -gt 0 ]; do
  case "${1}" in
    --out_dir=*)
      OUT_DIR="${1#*=}"
      ;;
    --inference_input_file=*)
      INFERENCE_INPUT_FILE="${1#*=}"
      ;;
    --inference_output_file=*)
      INFERENCE_OUTPUT_FILE="${1#*=}"
      ;;
    --work_dir=*)
      WORK_DIR="${1#*=}"
      ;;
    --chunk_size=*)
      CHUNK_SIZE="${1#*=}"
      ;;
    --tgt=*)
      TGT="${1#*=}"
      ;;
    *)
      echo "Unknown flag: ${1}" && exit 1
  esac
  shift
done

# Input validation and preprocessing.
if [[ -z "${INFERENCE_OUTPUT_FILE}" ]]; then
  # Assign default value to INFERENCE_OUTPUT_FILE, if not set by flags.
  INFERENCE_OUTPUT_FILE="${OUT_DIR}/$(basename ${INFERENCE_INPUT_FILE}).infer.${TGT}"
fi
if [[ -z "${WORD_DIR}" ]]; then
  # Assign default value to
  WORD_DIR="${HOME}/tmp/chunk_infer/$(basename ${INFERENCE_OUTPUT_FILE})"
fi
if [[ -d "${WORK_DIR}" ]]; then
  echo "WARNING: \${WORK_DIR}: ${WORK_DIR} exists."
else
  # Create work directory if nonexistent.
  mkdir -p "${WORK_DIR}" || exit 1
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
  "${INFERENCE_INPUT_FILE}" \
  "${WORK_DIR}/tmp-" \
   || exit 1

# Infer each chunk separately.
for CHUNK in $(ls ${WORK_DIR}/tmp-*.split); do
  OUT_CHUNK="${CHUNK}.infer.${TGT}"
  # Check if the output chunk exists, and whether it has the expected
  # number of lines to ensure it's not partially written.
  if [[ ! -f ${OUT_CHUNK} ]] ||
      [[ $(wc ${OUT_CHUNK} | awk '{print $1}') != $(wc ${CHUNK} | awk '{print $1}') ]]; then
    # Fill empty lines with the string "<unk>".
    sed -i 's/^$/<unk>/g' "${CHUNK}" || exit 1
    # Infer translations.
    python3 -m nmt.nmt.nmt \
      --out_dir="${OUT_DIR}" \
      --inference_input_file="${CHUNK}" \
      --inference_output_file="${OUT_CHUNK}" \
      || exit 1
  fi
  rm "${CHUNK}"
done

cat ${WORK_DIR}/tmp-*.split.infer.${TGT} > "${INFERENCE_OUTPUT_FILE}" || exit 1

echo "WARNING: \${WORK_DIR}: ${WORK_DIR} needs to be cleaned up manually."
