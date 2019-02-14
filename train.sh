# Parameterized train launcher.
#
# Example usage:
# bash train.sh \
#   --corpus_prefix="/home/isi_corpus" \
#   --batch_size=32
#
# The '--corpus_prefix' flag must be set int the command line. Other
# hyperparameters have default values that will be assigned unless overriden
# through the command line. Please refer to nmt/nmt.py for the interpretations
# of the present parameters.
#
# The script does the following:
# - Assign a meaningful name to the experiment.
# - Create an output directory bearing the name of the experiment.
# - Copy train, dev, and test date into the output directory.
# - Copy a prefix of the vocabulary into the output directory.
# - Launch tensorboard.
# - Launch google-chrome.
# - Launch email_update.
# - Start training.
# - Wait until training is finished, and kill background jobs.


# Default values for model parameters.
SRC="eng"
TGT="ara"
SRC_V=40000
TGT_V=40000
CORPUS_PREFIX=""
BATCH_SIZE=128
EMBED_PREFIX=""
NUM_LAYERS=2
NUM_UNITS=128
UNIT_TYPE="lstm"
ENCODER_TYPE="bi"
DROPOUT=0.2
INFER_MODE="beam_search"
BEAM_WIDTH=10
ATTENTION="scaled_luong"
ATTENTION_ARCHITECTURE="standard"
OPTIMIZER="sgd"
LEARNING_RATE=1.0
DECAY_SCHEME=""
SUBWORD_OPTION="bpe"
NUM_KEEP_CKPTS=5
AVG_CKPTS="true"
NUM_TRAIN_STEPS=10000000
STEPS_PER_STATS=100
METRICS="bleu"
TENSORBOARD_PORT=22222


# Override default values using command line flags.
while [ $# -gt 0 ]; do
  case "${1}" in
    --src=*)
      SRC="${1#*=}"
      ;;
    --tgt=*)
      TGT="${1#*=}"
      ;;
    --src_v=*)
      SRC_V="${1#*=}"
      ;;
    --tgt_v=*)
      TGT_V="${1#*=}"
      ;;
    --corpus_prefix=*)
      CORPUS_PREFIX="${1#*=}"
      ;;
    --batch_size=*)
      BATCH_SIZE="${1#*=}"
      ;;
    --embed_prefix=*)
      EMBED_PREFIX="${1#*=}"
      ;;
    --num_layers=*)
      NUM_LAYERS="${1#*=}"
      ;;
    --num_units=*)
      NUM_UNITS="${1#*=}"
      ;;
    --unit_type=*)
      UNIT_TYPE="${1#*=}"
      ;;
    --encoder_type=*)
      ENCODER_TYPE="${1#*=}"
      ;;
    --dropout=*)
      DROPOUT="${1#*=}"
      ;;
    --infer_mode=*)
      INFER_MODE="${1#*=}"
      ;;
    --beam_width=*)
      BEAM_WIDTH="${1#*=}"
      ;;
    --attention=*)
      ATTENTION="${1#*=}"
      ;;
    --attention_architecture=*)
      ATTENTION_ARCHITECTURE="${1#*=}"
      ;;
    --optimizer=*)
      OPTIMIZER="${1#*=}"
      ;;
    --learning_rate=*)
      LEARNING_RATE="${1#*=}"
      ;;
    --decay_scheme=*)
      DECAY_SCHEME="${1#*=}"
      ;;
    --subword_option=*)
      SUBWORD_OPTION="${1#*=}"
      ;;
    --num_keep_ckpts=*)
      NUM_KEEP_CKPTS="${1#*=}"
      ;;
    --avg_ckpts=*)
      AVG_CKPTS="${1#*=}"
      ;;
    --num_train_steps=*)
      NUM_TRAIN_STEPS="${1#*=}"
      ;;
    --steps_per_stats=*)
      STEPS_PER_STATS="${1#*=}"
      ;;
    --metrics=*)
      METRICS="${1#*=}"
      ;;
    --tensorboard_port=*)
      TENSORBOARD_PORT="${1#*=}"
      ;;
    *)
      echo "Unknown flag: ${1}" && exit 1
  esac
  shift
done

combine_if_non_empty() {
  if [[ "${1}" != "" && "${2}" != "" ]]; then
    echo "${1}${2}"
  else
    echo ""
  fi
}

# Assign a meaningful name to the output directory.
OUT_DIR="${HOME}/models/${SRC}-${SRC_V}_${TGT}-${TGT_V}\
_${NUM_LAYERS}x${NUM_UNITS}-${UNIT_TYPE}\
_${OPTIMIZER}-${LEARNING_RATE}-${NUM_TRAIN_STEPS}$(combine_if_non_empty - ${DECAY_SCHEME})\
_EN-${ENCODER_TYPE}\
_DO-${DROPOUT}\
_${INFER_MODE}-${BEAM_WIDTH}\
_BT-${BATCH_SIZE}\
$(combine_if_non_empty _AT- $(combine_if_non_empty ${ATTENTION} -${ATTENTION_ARCHITECTURE}))\
$(combine_if_non_empty _SW- ${SUBWORD_OPTION})\
$(combine_if_non_empty _EM- $(basename ${EMBED_PREFIX}))\
$(combine_if_non_empty $([[ ${AVG_CKPTS} = 'true' ]] && echo _AVG- || echo '') ${NUM_KEEP_CKPTS})"

# Set Python version based on OS release.
if [[ $(cat /etc/os-release | grep 'VERSION_ID' | grep -o '[[:digit:]]*\.[[:digit:]]*') == "18.04" ]]; then
  THREE="3"
else
  THREE=""
fi

# Make operations visible to user.
set -o xtrace

# Set up directory and datasets.
mkdir -p ${OUT_DIR}/data || exit
DATA_PREFIX="${OUT_DIR}/data/$(basename ${CORPUS_PREFIX})"
VOCAB_PREFIX=${DATA_PREFIX}.vocab-head
if [[ ! -f ${DATA_PREFIX}.vocab-head.${SRC} ]]; then
  head -${SRC_V} ${CORPUS_PREFIX}.vocab.${SRC} > ${VOCAB_PREFIX}.${SRC} || exit
fi
if [[ ! -f ${DATA_PREFIX}.vocab-head.${TGT} ]]; then
  head -${TGT_V} ${CORPUS_PREFIX}.vocab.${TGT} > ${VOCAB_PREFIX}.${TGT} || exit
fi
for LANGUAGE in "${SRC}" "${TGT}"; do
  for PARTITION in "train" "dev" "test"; do
    cp --no-clobber ${CORPUS_PREFIX}.clean.${PARTITION}.${LANGUAGE} ${OUT_DIR}/data/ || exit
  done
done

# Construct train command.
COMMAND="python${THREE} -m nmt.nmt.nmt \\
  --src=${SRC} \\
  --tgt=${TGT} \\
  --out_dir=${OUT_DIR} \\
  --vocab_prefix=${VOCAB_PREFIX} \\
  --train_prefix=${DATA_PREFIX}.clean.train \\
  --dev_prefix=${DATA_PREFIX}.clean.dev \\
  --test_prefix=${DATA_PREFIX}.clean.test \\
  --batch_size=${BATCH_SIZE} \\
  --embed_prefix=${EMBED_PREFIX} \\
  --num_layers=${NUM_LAYERS} \\
  --num_units=${NUM_UNITS} \\
  --unit_type=${UNIT_TYPE} \\
  --encoder_type=${ENCODER_TYPE} \\
  --dropout=${DROPOUT} \\
  --infer_mode=${INFER_MODE} \\
  --beam_width=${BEAM_WIDTH} \\
  --attention=${ATTENTION} \\
  --attention_architecture=${ATTENTION_ARCHITECTURE} \\
  --optimizer=${OPTIMIZER} \\
  --learning_rate=${LEARNING_RATE} \\
  --num_train_steps=${NUM_TRAIN_STEPS} \\
  --avg_ckpts=${AVG_CKPTS} \\
  --num_keep_ckpts=${NUM_KEEP_CKPTS} \\
  --decay_scheme=${DECAY_SCHEME} \\
  --subword_option=${SUBWORD_OPTION} \\
  --steps_per_stats=${STEPS_PER_STATS} \\
  --metrics=${METRICS}
"

# Save command in file in the output directory, for future reference.
echo "${COMMAND}" > "${OUT_DIR}/command.txt"

# Start background jobs.
tensorboard \
  --port="${TENSORBOARD_PORT}" \
  --logdir="${OUT_DIR}" \
  &

google-chrome-stable \
  "http://$(hostname):${TENSORBOARD_PORT}/#scalars&_smoothingWeight=0" \
  &

python3 \
  english-to-arabic-machine-translation/email_update.py \
  --out_dir=${OUT_DIR} \
  &

# Execute command to start training.
${COMMAND}

# After training ends, kill the background job.
kill $(jobs -p)

