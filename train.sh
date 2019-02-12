# Parameterized train launcher.
#
# Example usage:
# CORPUS_PREFIX=/home/isi_corpus \
#   NUM_LAYERS=2 \
#   NUM_UNITS=128 \
#   bash train.sh
#
# Hyperparameters are defined through the command line.
# The three hyper parameters above are mandatory for each experiment.
# Other hyperparameters will default to predefined values if not assigned
# through the command line.
#
# The script does the following functions:
# - Assign a meaningful name (<name>)to the experiment.
# - Create a directory called <out_dir> bearing the name of the experiment.
# - Copy train, dev, and test date into <out_dir>.
# - Copy a prefix of the vocabulary into <out_dir>.
# - Launch tensorboard.
# - Launch google-chrome.
# - Launch email_update.
# - Start training.
# - Kill background jobs after training is finished.
#


# Validate the mandatory arguments are present!
if [[ -z "${CORPUS_PREFIX}" ]]; then
  echo "CORPUS_PREFIX must be defined." && exit 1
fi
if [[ -z "${NUM_LAYERS}" ]]; then
  echo "NUM_LAYERS must be defined." && exit 1
fi
if [[ -z "${NUM_UNITS}" ]]; then
  echo "NUM_UNITS must be defined." && exit 1
fi

# Assign default values.
if [[ -z "${SRC}" ]]; then
  SRC="eng"
fi
if [[ -z "${TGT}" ]]; then
  TGT="ara"
fi
if [[ -z "${SRC_V}" ]]; then
  SRC_V=40000
fi
if [[ -z "${TGT_V}" ]]; then
  TGT_V=40000
fi
if [[ -z "${EMBED_PREFIX}" ]]; then
  # No embedding.
  EMBED_PREFIX=""
fi
if [[ -z "${UNIT_TYPE}" ]]; then
  UNIT_TYPE="lstm"
fi
if [[ -z "${ENCODER_TYPE}" ]]; then
  ENCODER_TYPE="bi"
fi
if [[ -z "${DROPOUT}" ]]; then
  DROPOUT=0.2
fi
if [[ -z "${INFER_MODE}" ]]; then
  INFER_MODE="beam_search"
fi
if [[ -z "${BEAM_WIDTH}" ]]; then
  BEAM_WIDTH=10
fi
if [[ -z "${ATTENTION}" ]]; then
  # No attention.
  ATTENTION=""
fi
if [[ -z "${ATTENTION_ARCHITECTURE}" ]]; then
  ATTENTION_ARCHITECTURE="standard"
fi
if [[ -z "${OPTIMIZER}" ]]; then
  OPTIMIZER="sgd"
fi
if [[ -z "${LEARNING_RATE}" ]]; then
  LEARNING_RATE=1.0
fi
if [[ -z "${DECAY_SCHEME}" ]]; then
  # No decay.
  DECAY_SCHEME=""
fi
if [[ -z "${SUBWORD_OPTION}" ]]; then
  # No subwording.
  SUBWORD_OPTION=""
fi
if [[ -z "${NUM_KEEP_CKPTS}" ]]; then
  NUM_KEEP_CKPTS=5
fi
if [[ -z "${AVG_CKPTS}" ]]; then
  AVG_CKPTS="true"
fi
if [[ -z "${NUM_TRAIN_STEPS}" ]]; then
  NUM_TRAIN_STEPS=10000000
fi
if [[ -z "${STEPS_PER_STATS}" ]]; then
  STEPS_PER_STATS=100
fi
if [[ -z "${METRICS}" ]]; then
  METRICS="bleu"
fi
if [[ -z "${TENSORBOARD_PORT}" ]]; then
  TENSORBOARD_PORT=22222
fi


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
$(combine_if_non_empty _AT- $(combine_if_non_empty ${ATTENTION} -${ATTENTION_ARCHITECTURE}))\
$(combine_if_non_empty _SW- ${SUBWORD_OPTION})\
$(combine_if_non_empty _EM- $(basename ${EMBED_PREFIX}))\
$(combine_if_non_empty $([[ ${AVG_CKPTS} = 'true' ]] && echo _AVG- || echo '') ${NUM_KEEP_CKPTS})"


# Set Python release based on OS release.
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
