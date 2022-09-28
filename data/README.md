# Readme

This folder contains code necessary to query and preprocess the blockchain data used in this analysis.

You can use the code in `./get_blocks.py` to query the necessary blocks from https://etherscan.io . You need
a registered account and API key.

The code in `./processBlockData.nim` should be compiled with Nim and provides basic functionality to process a range of
blocks downloaded with the previous script and make a big JSON file with them. It will also clean-up some unnecessary fields
that occupy a lot of weight and are not used in the analysis (e.g., transactions in each block). It's written in Nim
to perform this operation much faster than could be done in Python. You should create a big file with the Proof of Work 
blocks you want to analyze and another with the Proof of Stake blocks. These can be used in the Python scripts
you can find in the analysis folder.

Or you could query your own node if you have it available. Create 2 JSON files with the data of the Proof of Work and
Proof of Stake following the response format described in https://docs.etherscan.io/api-endpoints/geth-parity-proxy#eth_getblockbynumber