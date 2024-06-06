# Link prediction on real and generated social networks

Models and features chosen are based on: [Link Prediction in Social Networks using
Computationally Efficient Topological Features](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=9f3c2d5364aab82a24e24e56f6013cfc4c404e13)
## Data used from:

1. [Condense Matter collaboration network](https://snap.stanford.edu/data/ca-CondMat.html)
2. [General Relativity and Quantum Cosmology collaboration network](https://snap.stanford.edu/data/ca-GrQc.html)
3. Generated networks are generated using netwrokX


## Libraries used:

1. [NetworkX](https://networkx.org/)
2. [PyTorch](https://pytorch.org/)
3. [scikit-learn](https://scikit-learn.org/stable/)
4. [seaborn](https://seaborn.pydata.org/)
5. [pandas](https://pandas.pydata.org/)

## Project structure explanation

1. data folder - contains calculated features for the networks in a csv file for each networks
2. networks folder - contains network files from which networks are created in the program
3. neuralnetworks folder - contains save files of neural networks trained: NetworkName/NetworkName_[percentage_of_data_in_training]_chosen_features.pt
4. performance folder - contains performances of models based on features used
5. classification_models notebook - used for training every model except neural network
6. network_data python script - used for calculating features from networks
7. neural_network notebook - used for training a neural network
8. report notebook - used for ploting performance data and conclusion

