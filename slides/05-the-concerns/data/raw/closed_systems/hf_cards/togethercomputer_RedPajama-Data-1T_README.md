---
task_categories:
- text-generation
language:
- en
pretty_name: Red Pajama 1T
---
### Getting Started

The dataset consists of 2084 jsonl files.
You can download the dataset using HuggingFace:
```python
from datasets import load_dataset
ds = load_dataset("togethercomputer/RedPajama-Data-1T")
```

Or you can directly download the files using the following command:

```
wget 'https://data.together.xyz/redpajama-data-1T/v1.0.0/urls.txt'
while read line; do
    dload_loc=${line#https://data.together.xyz/redpajama-data-1T/v1.0.0/}
    mkdir -p $(dirname $dload_loc)
    wget "$line" -O "$dload_loc"
done < urls.txt
```

After downloading the files, you can load the dataset from disk by setting the `RED_PAJAMA_DATA_DIR` environment variable to the directory containing the files:

```python
import os
from datasets import load_dataset
os.environ["RED_PAJAMA_DATA_DIR"] = "/path/to/download"
ds = load_dataset("togethercomputer/RedPajama-Data-1T")
```

A smaller 1B-token sample of the dataset can be found [here](https://huggingface.co/datasets/togethercomputer/RedPajama-Data-1T-Sample).

A full set of scripts to recreate the dataset from scratch can be found [here](https://github.com/togethercomputer/RedPajama-Data).

### Dataset Summary

RedPajama is a clean-room, fully open-source implementation of the LLaMa dataset.

| Dataset       | Token Count |
|---------------|-------------|
| Commoncrawl   | 878 Billion        |
| C4            | 175 Billion        |
| GitHub        | 59 Billion         |
| ArXiv         | 28 Billion         |
| Wikipedia     | 24 Billion         |
| StackExchange | 20 Billion         |
| Total         | 1.2 Trillion      |

### Languages

Primarily English, though the Wikipedia slice contains multiple languages.

## Dataset Structure

The dataset structure is as follows:

```json
{
    "text": ...,
    "meta": {"url": "...", "timestamp": "...", "source": "...", "language": "...", ...},
    "red_pajama_subset": "common_crawl" | "c4" | "github" | "arxiv" | "wikipedia" | "stackexchange"
}
```

## Dataset Creation

This dataset was created to follow the LLaMa paper as closely as possible to try to reproduce its recipe.

### Source Data

#### Commoncrawl

We download five dumps from Commoncrawl, and run the dumps through the official `cc_net` pipeline.
We then deduplicate on the paragraph level, and filter out low quality text using a linear classifier trained to 
classify paragraphs as Wikipedia references or random Commoncrawl samples.

#### C4

C4 is downloaded from Huggingface. The only preprocessing step is to bring the data into our own format.

#### GitHub

The raw GitHub data is downloaded from Google BigQuery. We deduplicate on the file level and filter out low quality 
files and only keep projects that are distributed under the MIT, BSD, or Apache license.

#### Wikipedia
We use the Wikipedia dataset available on Huggingface, which is based on the Wikipedia dump from 2023-03-20 and contains
text in 20 different languages. The dataset comes in preprocessed format, so that hyperlinks, comments and other 
formatting boilerplate has been removed.

#### Gutenberg and Books3


<div class="course-tip course-tip-orange bg-gradient-to-br dark:bg-gradient-to-r before:border-orange-500 dark:before:border-orange-800 from-orange-50 dark:from-gray-900 to-white dark:to-gray-950 border border-orange-50 text-orange-700 dark:text-gray-400">
  <p><b>Defunct:</b> The 'book' config is defunct and no longer accessible due to reported copyright infringement for the Book3 dataset contained in this config.</p>
</div>


#### ArXiv
ArXiv data is downloaded from Amazon S3 in the `arxiv` requester pays bucket. We only keep latex source files and 
remove preambles, comments, macros and bibliographies.

#### Stackexchange
The Stack Exchange split of the dataset is download from the 
[Internet Archive](https://archive.org/download/stackexchange). Here we only keep the posts from the 28 largest sites,
remove html tags, group the posts into question-answer pairs, and order answers by their score.

### SHA256 Checksums

SHA256 checksums for the dataset files for each data source are available here:

```
https://data.together.xyz/redpajama-data-1T/v1.0.0/sha256/arxiv_SHA256SUMS.txt
https://data.together.xyz/redpajama-data-1T/v1.0.0/sha256/c4_SHA256SUMS.txt
https://data.together.xyz/redpajama-data-1T/v1.0.0/sha256/common_crawl_SHA256SUMS.txt
https://data.together.xyz/redpajama-data-1T/v1.0.0/sha256/github_SHA256SUMS.txt
https://data.together.xyz/redpajama-data-1T/v1.0.0/sha256/stackexchange_SHA256SUMS.txt
https://data.together.xyz/redpajama-data-1T/v1.0.0/sha256/wikipedia_SHA256SUMS.txt
```

To cite RedPajama, please use:

```
@software{together2023redpajama,
  author = {Together Computer},
  title = {RedPajama: An Open Source Recipe to Reproduce LLaMA training dataset},
  month = April,
  year = 2023,
  url = {https://github.com/togethercomputer/RedPajama-Data}
}
```

### License
Please refer to the licenses of the data subsets you use.

* [Common Crawl Foundation Terms of Use](https://commoncrawl.org/terms-of-use/full/)
* [C4 license](https://huggingface.co/datasets/allenai/c4#license)
* GitHub was limited to MIT, BSD, or Apache licenses only
* [ArXiv Terms of Use](https://info.arxiv.org/help/api/tou.html)
* [Wikipedia License](https://huggingface.co/datasets/wikipedia#licensing-information)
* [StackExchange license on the Internet Archive](https://archive.org/details/stackexchange)

<!--
### Annotations
#### Annotation process
[More Information Needed]
#### Who are the annotators?
[More Information Needed]
### Personal and Sensitive Information
[More Information Needed]
## Considerations for Using the Data
### Social Impact of Dataset
[More Information Needed]
### Discussion of Biases
[More Information Needed]
### Other Known Limitations
[More Information Needed]
## Additional Information
### Dataset Curators
[More Information Needed]
### Licensing Information
[More Information Needed]
### Citation Information
[More Information Needed]
### Contributions
[More Information Needed]
-->