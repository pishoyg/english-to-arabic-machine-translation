DATA_PREFIX="/home/bishoyboshra/corpora/CorporaDec07/LDC2007T08/isi_ara_eng_parallel_corpus/data/ISI_ara_eng_parallel_corpus"
MODEL_DIR="${HOME}/models/nmt_model_${RANDOM}"
NUM_LAYERS=2
NUM_UNITS=128
DROPOUT=0.2

set -o xtrace
mkdir -p ${MODEL_DIR}

python -m nmt.nmt.nmt \
    --src="eng" --tgt="ara" \
    --vocab_prefix="${DATA_PREFIX}.vocab" \
    --train_prefix="${DATA_PREFIX}.clean_train_head" \
    --dev_prefix="${DATA_PREFIX}.clean_dev_head" \
    --test_prefix="${DATA_PREFIX}.clean_test_head" \
    --out_dir="${MODEL_DIR}" \
    --num_train_steps=12000000 \
    --steps_per_stats=100 \
    --num_layers="${NUM_LAYERS}" \
    --num_units="${NUM_UNITS}" \
    --dropout="${DROPOUT}" \
    --metrics=bleu
