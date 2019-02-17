# english-to-arabic-machine-translation
The training platform that we are using is Google seq2seq: https://github.com/tensorflow/nmt

This repository contains scripts to do the following:
- Preprocessing corpus
  - Orthographic normalization.
  - Partitioning dataset.
- Auxiliary script that facilitates naming, parameter-passing, and launching experiments.
- An email-update code, which runs a background job to send updates by email about performance improvements.
