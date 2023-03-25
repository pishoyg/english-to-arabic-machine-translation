# english-to-arabic-machine-translation
## Neural Machine Translation.
The training platform that we are using is [Google seq2seq](https://github.com/tensorflow/nmt). Run the following command to obtain it.
``` shell
git clone https://github.com/tensorflow/nmt.git
touch nmt/__init__.py
```
It's highly advised to familiarize yourself with this tool before moving forward. Familiarity with Bash and Python will also be beneficial.
## Requirements.
No exceptional requirements exist for duplicating any part of the training process. The main requirements are as simple as a Linux machine with git, python3, and tensorflow.
*A personalized requirement-installation script can be found in [**sudo_setup.sh**](sudo_setup.sh) and [**setup.sh**](setup.sh), however this is provided as a guide, and is not intended for duplication.*
## Corpus.
## Preprocessing.
### Orthographic normalization.
### Morphology-aware tokenization.
## Dataset partitioning.
## Extracting vocabulary.
### Plotting vocabulary popularity histograms.
## Training.
## Inference.
