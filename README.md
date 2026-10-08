> Laboratory TIMC / BCM Grenoble


# Backtrack-Free Walk (BFWalk)

BFWalk is a new network propagation algorithm based on non-backtracking walks and in-degree normalization. The algorithm assigns scores to nodes in the network that represent their proximity to a given list of nodes of interest (i.e. seeds).


## Install BFWalk

BFWalk uses BFWalk-C for heavy-lifting calculations. The C code is compiled automatically during installation, so you need a C compiler (gcc) and the BFWalk-C dependencies (zlib and OpenMP, including the header files, e.g. zlib-devel on RHEL).

We recommend to install BFWalk in a [Python virtual environment](https://docs.python.org/3/library/venv.html), it can be created and activated with:
```
python -m venv --system-site-packages ~/pyEnv_bfwalk
source ~/pyEnv_bfwalk/bin/activate
pip install --upgrade pip
```

Then install BFWalk with:
```
pip install bfwalk
```

Or compile the BFWalk-C code from source:

```
git clone --recurse-submodules https://github.com/jedrzejkubica/BFWalk.git
cd BFWalk/BFWalk-C
make
cd ..
python BFWalk/bfwalk.py --help
```

Then in the examples below, replace `bfwalk` with `python BFWalk.py`.


## Use BFWalk

For details see:
```
bfwalk --help
```

As input, BFWalk requires:

- `--network`: a text file with one interaction per line, in the following format: `node1 weight/interaction_type node2` (3 tab-separated columns). It is a format similar to SIF but allows for weighted networks ([SIF format documentation](https://cytoscape.org/manual/Cytoscape2_5Manual.html#SIF%20Format))
- `--seeds`: a text file with one seed per line

For output, BFWalk prints to stdout the scores in TSV format `node score` (2 tab-separated columns).

Networks are undirected and unweighted by default, but BFWalk can also use a directed and/or weighted network:
- use `--directed` if your network is directed, edges are then seen as node1->node2 (i.e. the source is in the first column and the destination in the third column);
- use `--weighted` if your network is weighted, the second column of the network file must then contain the weight of each interaction (0 < weight <= 1).

If needed, BFWalk allows the user to set the attenuation coefficient `--alpha`  (0 < alpha < 1), although the default = 0.5 should be fine for most use cases.


## Examples

### Weighted network

This example uses a simple "diamond" network with 4 nodes and 4 weighted edges: A, B, C, D. Here A is the seed.

```
bfwalk \
  --network Examples/network_weighted.sif \
  --seeds Examples/seeds.txt \
  --weighted \
  1> scores.tsv \
  2> log.txt
```


### Directed network

This example uses a simple network with 3 nodes and 2 directed edges: C -> A -> B. Here A is the seed.

```
bfwalk \
  --network Examples/network_directed.sif \
  --seeds Examples/seeds.txt \
  --directed \
  1> scores.tsv \
  2> log.txt
```


### Human interactome

We provide additional instructions for interactome-based disease gene prioritization. The instructions and scripts to build a human interactome and prepare a seeds file with known causal genes can be found in the [Interactome/](Interactome/) subdirectory.


## Validation of BFWalk

A manuscript describing BFWalk has been submitted. The code to perform the analyses and generate the figures presented in this manuscript are available on GitHub: [BFWalk-validation](https://github.com/jedrzejkubica/BFWalk-validation).


## How to cite

If you use BFWalk, please cite our [preprint](https://www.biorxiv.org/content/early/2026/09/28/2026.09.22.753510):
```
@article {Kubica2026bfwalk,
	title = {BFWalk: backtrack-free network propagation with in-degree normalization},
	author = {Kubica, J{\k e}drzej and Plewczynski, Dariusz and D{\'e}jean, S{\'e}bastien and Thierry-Mieg, Nicolas},
	journal = {bioRxiv},
	year = {2026},
	doi = {10.64898/2026.09.22.753510},
	publisher = {Cold Spring Harbor Laboratory},
	URL = {https://www.biorxiv.org/content/early/2026/09/28/2026.09.22.753510}
}
```


## Note

Formerly "GBA-centrality" for anyone arriving via old citations.
