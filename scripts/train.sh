# Data parameters.
DATA_PREFIX="$1"
SRC_V=40000
TGT_V=40000
SRC="eng"
TGT="ara"
# Model parameters.
NUM_LAYERS=$2
NUM_UNITS=$3
DROPOUT=0.2
INFER_MODE="beam_search"
BEAM_WIDTH=10
# Stats parameters.
NUM_TRAIN_STEPS=12000000
STEPS_PER_STATS=100
METRICS="bleu"

OUT_DIR="${HOME}/models/${SRC}-${SRC_V}_${TGT}-${TGT_V}_${NUM_LAYERS}x${NUM_UNITS}_${DROPOUT}_${BEAM_WIDTH}"

# Perform some argument validation!
for ARGUMENT in "${DATA_PREFIX}" "${NUM_LAYERS}" "${NUM_UNITS}" "${BEAM_WIDTH}" "${INFER_MODE}"; do
  if [[ "${ARGUMENT}" == "" ]]; then
    echo 'Missing command line arguments!!' && exit 1
  fi
done

# Because I use Python 3 on machines where my username is 'bishoy',
# and Python 2.7 on machines where my username is 'bishoyboshra'!
if [[ ${USER} == "bishoy" ]]; then
  THREE="3"
elif [[ ${USER} == "bishoyboshra" ]]; then
  THREE=""
fi

# Make operations visible to user.
set -o xtrace

# Set up directory and datasets.
mkdir -p ${OUT_DIR}

VOCAB_PREFIX="${OUT_DIR}/$(basename ${DATA_PREFIX}).vocab-head"
PARTITION_PREFIX="${OUT_DIR}/$(basename ${DATA_PREFIX}).clean"
head -${SRC_V} ${DATA_PREFIX}.vocab.${SRC} > ${VOCAB_PREFIX}.${SRC}
head -${TGT_V} ${DATA_PREFIX}.vocab.${TGT} > ${VOCAB_PREFIX}.${TGT}
for LANGUAGE in "${SRC}" "${TGT}"; do
  for PARTITION in train dev test; do
    cp ${DATA_PREFIX}.clean.${PARTITION}.${LANGUAGE} ${OUT_DIR}
  done
done

# Start training.
python${THREE} -m nmt.nmt.nmt \
    --src="${SRC}" --tgt="${TGT}" \
    --vocab_prefix="${VOCAB_PREFIX}" \
    --train_prefix="${PARTITION_PREFIX}.train" \
    --dev_prefix="${PARTITION_PREFIX}.dev" \
    --test_prefix="${PARTITION_PREFIX}.test" \
    --out_dir="${OUT_DIR}" \
    --num_train_steps="${NUM_TRAIN_STEPS}" \
    --steps_per_stats="${STEPS_PER_STATS}" \
    --num_layers="${NUM_LAYERS}" \
    --num_units="${NUM_UNITS}" \
    --dropout="${DROPOUT}" \
    --metrics="${METRICS}" \
    --infer_mode="${INFER_MODE}" \
    --beam_width="${BEAM_WIDTH}"
