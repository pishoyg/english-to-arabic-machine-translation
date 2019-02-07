INPUT_PATH="$1"
LANGS="ara eng"
VOCAB_SIZES="40000 20000"
PARTITIONS="test dev train"
PARTITION_SIZES="10000 10000 250000"

if [[ ${INPUT_PATH} == "" ]]; then
  echo 'Error: Input path not specified!!' && exit 1
fi

LANGS=(${LANGS})
VOCAB_SIZES=(${VOCAB_SIZES})
PARTITIONS=(${PARTITIONS})
PARTITION_SIZES=(${PARTITION_SIZES})

if [[ ${#PARTITIONS[@]} != ${#PARTITION_SIZES[@]} ]]; then
  echo 'Error: mismatching partitions and numbers array sizes!!' && exit 1
fi

set -o xtrace

for i in ${!LANGS[@]}; do
  LANG=${LANGS[$i]}
  for j in ${!PARTITIONS[@]}; do
    PARTITION=${PARTITIONS[$j]}
    PARTITIONS_SIZE=${PARTITION_SIZES[$j]}
    head -${PARTITIONS_SIZE} ${INPUT_PATH}.clean.${PARTITION}.${LANG} > ${INPUT_PATH}.clean.${PARTITION}.head.${LANG}
  done
  VOCAB_SIZE=${VOCAB_SIZES[$i]}
  head -${VOCAB_SIZE} ${INPUT_PATH}.vocab.${LANG} > ${INPUT_PATH}.vocab.head.${LANG}
done
