This repository aims at helping with clustering of Catalyst proposals,
in order to split the reviewing work load.

This was made possible thanks to the efforts and discussions with @theeldermillenial ([GitHub][elder-gh], [twitter][elder-twitter]).
Please reference this attribution if this repository is useful to you,
and also support their projects.

[elder-gh]: https://github.com/theeldermillenial
[elder-twitter]: https://x.com/ElderM

## Initialization

Let’s first install `uv` if you don’t have it yet on your computer.
It’s the best package manager for python.
Follow the installation guide there: https://docs.astral.sh/uv/getting-started/installation/

Now let’s setup this project.

```sh
# Install deps
uv sync

# Download and post-process fund category proposals.
# This will generate a catalyst_proposals_f13_open_dev folder with proposals inside,
# paginated by 50 proposals per json file.
#
# PS: Change X-CSRF-TOKEN value in download script with a value
# that you would get from running for example the "challenges" API end point
# https://www.lidonation.com/catalyst-explorer/api#/challenge/challenges
# Also change the challenge_id for the one you want.
uv run download_proposals.py

# Now this will process those downloaded files to only extract the relevant fields.
uv run process_proposals.py
```

## First approach: local clustering with emmbeddings with code

```sh
# Classify proposals
uv run classify.py
```

TODO: improve with Elder Millenial feedback:

1. For minimalist open source embedding models, I would recommend nomic
2. I would highly recommend using a hierarchical clustering strategy, especially when you don't know the number of clusters you have (e.g. hdbscan)
3. I think that UMAP will probably give you better results than tsne. Depending on what you're interested in doing,  you might want to switch to PCA.
4. High dimensional clustering can be frought with all kinds of issues, especially if you're not careful about selecting and parameterizing your distance function well. I'd recommend doing dimension reduction and then clustering.

## Alternative approach: prompting an LLM directly

First, let’s create a minimal json file containing only the `id`, `title`, and `problem` fields.
```sh
jq '[.[] | {id, title, problem}]' aggregated_catalyst_data.json > small.json
```

Now, let’s use that `small.json` file in a prompt:
```
Here is a json file containing data with an id, a title, and a problem for each item. I want to cluster that data into roughly 10 clusters that are semantically close. Beware that all these items are related to the cardano blockchain, so this cannot be a differentiating factor for the clustering. Use more precise themes inside the context of the Cardano blockchain. Please output a new json file with for each cluster, a summary of the category content, and the list of id of every item in that cluster.
Here is the input json file.
```

The output to download will have the following shape:
```json
{ "0": { "summary": "Summary of category 0", "ids": [14920, 42273, ...] }, "1": { ... } }
```

Let’s say, we call that clustered json `clustered_data.json`.

Now we can group the original aggregated data with the ids returned by the LLM, using jq like this:
```sh
jq -n '
   (input | .) as $categories |
   (input | .) as $data |
   $categories | to_entries | map({
     category: .key,
     summary: .value.summary,
     items: [ .value.ids[] as $id | $data[] | select(.id == $id) ]
   })
 ' clustered_data.json aggregated_catalyst_data.json > grouped.json
```
