# Set default values.
OUT_DIR=""
INFERENCE_INPUT_FILE=""
INFERENCE_OUTPUT_FILE=""
# Temporary work directory.
WORK_DIR="/tmp/tmp"
CHUNK_SIZE="100000"

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
    *)
      echo "Unknown flag: ${1}" && exit 1
  esac
  shift
done

# Input validation.
if [[ -d "${WORK_DIR}" ]]; then
  echo "WARNING: \${WORK_DIR}: ${WORK_DIR} exists."
else
  mkdir -p "${WORK_DIR}" || exit 1
fi

# Make operations visible to user.
set -o xtrace

split \
  --numeric-suffixes=0 \
  --suffix-length=7 \
  --additional-suffix=".split" \
  --lines="${CHUNK_SIZE}" \
  "${INFERENCE_INPUT_FILE}" \
  "${WORK_DIR}/tmp-" \
   || exit 1

# TODO: add a flag to decide on whether to overwrite existing output.
for CHUNK in $(ls ${WORK_DIR}/tmp-*.split); do
  OUT_CHUNK="${CHUNK}.inference"
  if [[ ! -f ${OUT_CHUNK} ]] ||
      [[ $(wc ${OUT_CHUNK} | awk '{print $1}') != $(wc ${CHUNK} | awk '{print $1}') ]]; then
    sed -i 's/^$/<unk>/g' "${CHUNK}"
    python3 -m nmt.nmt.nmt \
      --out_dir="${OUT_DIR}" \
      --inference_input_file="${CHUNK}" \
      --inference_output_file="${OUT_CHUNK}" \
      || exit 1
  fi
done

cat ${WORK_DIR}/tmp-*.split.inference > "${INFERENCE_OUTPUT_FILE}" || exit 1

# TODO: Arrange for the deletion of the work directory.
# rm -r "${WORK_DIR}"
