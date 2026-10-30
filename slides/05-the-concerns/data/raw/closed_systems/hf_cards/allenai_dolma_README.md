---
license: odc-by
viewer: false
task_categories:
- text-generation
language:
- en
tags:
- language-modeling
- casual-lm
- llm
pretty_name: Dolma
size_categories:
- n>1T
---

# Dolma

<img alt="Dolma's official logo. It's dolma written in yellow, round lowercase letters over a blue background." src="https://raw.githubusercontent.com/allenai/dolma/main/docs/assets/AI2_Blog_1400x685_2x.webp" width="100%">

Dolma is a dataset of 3 trillion tokens from a diverse mix of web content, academic publications, code, books, and encyclopedic materials.

More information:

- Read Dolma **manuscript** and its **Data Sheet** [on ArXiv](https://arxiv.org/abs/2402.00159);
- Explore the [**open source tools**](https://github.com/allenai/dolma) we created to curate Dolma.
- Want to request removal of personal data? Use [this form](https://forms.gle/q4BNUUxUxKwKkfdT6) to notify us of documents containing PII about a specific user.

To learn more about the toolkit used to create Dolma, including how to replicate this dataset, head over our [GitHub project page](https://github.com/allenai/dolma/tree/main/docs)!

**2024-04-17: Dolma v1.7 Release.** We have released an updated version of Dolma that we used to train our latest [OLMo 7B-v1.7](https://huggingface.co/allenai/OLMo-7b-v1.7) model.

**2024-04-15: License Change.** We have updated the license of Dolma to [ODC-BY](https://opendatacommons.org/licenses/by/1-0/). Please see this [blog post](https://blog.allenai.org/making-a-switch-dolma-moves-to-odc-by-8f0e73852f44) for more information.


## Versions

At the moment, there are six versions of Dolma available:

| **Version** | **Default?** | **Release Date** | **Size** (gzip) | **Description** |
|--|:--:|--|--|--|
| `v1_7` | ✅ | 2024-04-15 | 4.5 TB | Used to train [OLMo-7B-v1.7](https://huggingface.co/allenai/OLMo-7b-v1.7). New sources, more quality filtering, fuzzy deduplication. |
| `v1_6` |  | 2024-01-31 | 5.4 TB | An update to v1.5 with some deduplication of documents with too few tokens or too many repeated n-grams. |
| `v1_6-sample` | | 2024-01-31 | 16.4 GB | A smaller sample of Dolma, with roughly 10 billion tokens. Useful for data exploration. |
| `v1_5` | | 2023-10-31 | 6.4 TB | Used to train [OLMo-1B](https://huggingface.co/allenai/OLMo-1B). Roughly 3 trillion tokens. |
| `v1_5-sample` | | 2023-10-31 | 2.9 TB | A sample of roughly 1.9 trillion tokens used to train [OLMo-7B](https://huggingface.co/allenai/OLMo-7B) |
| `v1` | | 2023-08-18 | 6.0 TB | The first version of Dolma. |


## Summary Statistics (v1.7)

| **Source** | **Provenance** | **New?** | **Documents** (millions) |  **OLMo tokens** (billions) | **Sample Proportion** | **Cutoff Date** | **Processing**
|--|--|--|--|--|--|--|--|
| Dolma's CC | [Common Crawl](https://commoncrawl.org/) via Dolma v1.6 | Updated | 875.2 | 1,195.5 | 50% | Mar 2023 | Extracted using the Dolma pipeline; new quality filtering and deduplication steps. |
| Refined Web | [Refined Web](https://huggingface.co/datasets/tiiuae/falcon-refinedweb) | Yes | 664.0 | 456.4  | 100% | Feb 2023 | Filtered using the Dolma pipeline; new quality filtering and deduplication steps.  |
| StarCoder | [StarCoder](https://huggingface.co/blog/starcoder) | Yes |  206.6 | 263.8  | 100% | May 2023 | No further processing. |
| C4 | [C4](https://huggingface.co/datasets/c4) via Dolma v1.6 | Updated | 249.9 | 138.4 | 50% | Apr 2019 | Filtered using the Dolma pipeline; new quality filtering and deduplication steps. |
| Reddit | [PushShift API](https://github.com/pushshift/api) | Updated | 377.4 | 79.9 | 100% | Mar 2023 | Extracted using the Dolma pipeline; new quality filtering and deduplication steps. |
| Semantic Scholar ([S2ORC](https://aclanthology.org/2020.acl-main.447/) & [S2AG](https://www.semanticscholar.org/product/api)) | [peS2o](https://huggingface.co/datasets/allenai/peS2o) via Dolma v1.6 | No | 38.8  | 57.2 | 100% | Mar 2023 | Same as Dolma v1.6 |
| arXiv | [RedPajama v1](https://huggingface.co/datasets/togethercomputer/RedPajama-Data-1T) | Yes | 1.5 | 28.0 | 100% | Mar 2023 | No further processing. |
| StackExchange | [RedPajama v1](https://huggingface.co/datasets/togethercomputer/RedPajama-Data-1T) | Yes | 29.3 | 19.6 | 100%  | Mar 2023  | No further processing.  |
| Flan | [Flan Collection](https://arxiv.org/abs/2301.13688), reproduced following the [original code](https://github.com/google-research/FLAN/tree/main/flan/v2), as performed by [Dettmers et al., (2023)](https://openreview.net/forum?id=OUIFPHEgJU)   | Yes | 52.1 | 16.5 | 100%  | Feb 2023  | After reproducing Flan, sampled to balance different Flan subsets. Reformatted for pretraining with newlines separating instruction and demonstration. |
| CC News | [Common Crawl](https://commoncrawl.org/blog/news-dataset-available) | Yes | 22.0 | 14.3  | 100%  | Mar 2023  | Extracted using the Dolma pipeline; new quality filtering and deduplication steps. |
| OpenWebMath | [OpenWebMath](https://huggingface.co/datasets/open-web-math/open-web-math) via [Proof Pile II](https://huggingface.co/datasets/EleutherAI/proof-pile-2) | Yes | 2.9 |  12.6 | 100% | May 2023 | Training subset; no further processing. |
| Algebraic Stack | [Proof Pile II](https://huggingface.co/datasets/EleutherAI/proof-pile-2) | Yes | 2.8 |  12.6 | 100% | Oct 2023 | Training subset; no further processing. |
| Project Gutenberg | [Project Gutenberg](https://www.gutenberg.org) via Dolma v1.6 | No |  0.0556 | 5.3 | 100% | Mar 2023 | Same as Dolma v1.6 |
| MegaWika | [MetaWika](https://huggingface.co/datasets/hltcoe/megawika) | Yes | 3.2 | 4.6 | 100%  | Jul 2023  | English web pages cited from Wikipedia; curated using the full Dolma pipeline.  |
| Wikipedia & Wikibooks | [Wikimedia](https://dumps.wikimedia.org) via Dolma v1.6 | No |  6.2 |  3.7 | 200%  | Mar 2023 |  Same as Dolma v1.6 |
| **Total** | | | **2532.0** | **2,308.5** | **1,715.1** | **Oct 2023** | |

(A subset of total data was used for training of OLMo 7B-v1.7. The token counts are based on the full dataset, whereas taking into account sampling proportion gives the final actual token counts used for training --- 1.715 trillion tokens.)


## Summary Statistics (v1.6)

| **Source** | **Doc Type** | **UTF-8 bytes** (GB) | **Documents** (millions) | **Unicode words** (billions) | **Llama tokens** (billions) |
|--|--|--|--|--|--|
| Common Crawl | web pages | 9,022 | 3,370 | 1,775 | 2,281 |
| The Stack | code| 1,043| 210 | 260| 411 |
| C4 | web pages | 790 | 364 | 153| 198 |
| Reddit| social media| 339 | 377| 72| 89 |
| PeS2o | STEM papers| 268 | 38.8| 50| 70 |
| Project Gutenberg | books | 20.4 | 0.056 | 4.0 | 6.0 |
| Wikipedia, Wikibooks | encyclopedic | 16.2 | 6.2 | 3.7 | 4.3 |
| **Total** | | **11,519** | **4,367** | **2,318** | **3,059** |


## Download

The fastest way to download Dolma is to clone this repository and use the files in the `url` directory.
We recommend using wget in parallel mode to download the files. For example:

```bash
DATA_DIR="<path_to_your_data_directory>"
PARALLEL_DOWNLOADS="<number_of_parallel_downloads>"
DOLMA_VERSION="<version_of_dolma_to_download>"

git clone https://huggingface.co/datasets/allenai/dolma
mkdir -p "${DATA_DIR}"


cat "dolma/urls/${DOLMA_VERSION}.txt" | xargs -n 1 -P "${PARALLEL_DOWNLOADS}" wget -q -P "$DATA_DIR"
```

Then, to load this data using HuggingFace's `datasets` library, you can use the following code:

```python
import os
from datasets import load_dataset

os.environ["DATA_DIR"] = "<path_to_your_data_directory>"
dataset = load_dataset("allenai/dolma", split="train")
```

### Licensing Information

We are releasing this dataset under the terms of [ODC-BY](https://opendatacommons.org/licenses/by/1-0/).
By using this dataset, you are also bound any license agreements and terms of use of the original data sources.

## Bibtex

If you use our dataset or tooling, please cite us at:

```bibtex
@article{dolma,
  title = {{Dolma: an Open Corpus of Three Trillion Tokens for Language Model Pretraining Research}},
  author={
    Luca Soldaini and Rodney Kinney and Akshita Bhagia and Dustin Schwenk and David Atkinson and
    Russell Authur and Ben Bogin and Khyathi Chandu and Jennifer Dumas and Yanai Elazar and
    Valentin Hofmann and Ananya Harsh Jha and Sachin Kumar and Li Lucy and Xinxi Lyu and
    Nathan Lambert and Ian Magnusson and Jacob Morrison and Niklas Muennighoff and Aakanksha Naik and
    Crystal Nam and Matthew E. Peters and Abhilasha Ravichander and Kyle Richardson and Zejiang Shen and
    Emma Strubell and Nishant Subramani and Oyvind Tafjord and Pete Walsh and Luke Zettlemoyer and
    Noah A. Smith and Hannaneh Hajishirzi and Iz Beltagy and Dirk Groeneveld and Jesse Dodge and Kyle Lo
  },
  year = {2024},
  journal={arXiv preprint},
}
```
