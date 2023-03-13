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
The corpus that we are using is ISI LDC2007T08. This is available for download from our [Google Drive folder](https://drive.google.com/open?id=1oofJ0AdYY-r6fiswxNH_CcN-AGHMGZ9d). However, any corpus will do. The format that is expected by our platform is two text files with parallel sentences, one sentence per line.
## Preprocessing.
### Orthographic normalization.
### Morphology-aware tokenization.
## Dataset partitioning.
## Extracting vocabulary.
### Plotting vocabulary popularity histograms.
## Training.
## Inference.
