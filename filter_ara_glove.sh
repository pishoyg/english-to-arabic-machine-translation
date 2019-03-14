# TODO: have a smarter filter that would only pass the embeddings of
# the words existing in a given vocabulary file.

# Set default values.
INPUT_TXT=""
OUTPUT_TXT=""

# Parsing flags.
while [ $# -gt 0 ]; do
  case "${1}" in
    --input_txt=*)
      INPUT_TXT="${1#*=}"
      ;;
    --output_txt=*)
      OUTPUT_TXT="${1#*=}"
      ;;
    *)
      echo "Unknown flag: ${1}" && exit 1
  esac
  shift
done

cat "${INPUT_TXT}" | grep '^[ءؤئابتثجحخدذرزسشصضطظعغفقكلمنهوي]\+ ' > "${OUTPUT_TXT}"

