#/usr/bin/python3

import re

import pandas as pd

# from gutenberg import acquire
# from gutenberg import cleanup

from tensor2tensor.data_generators import problem
from tensor2tensor.data_generators import text_problems
from tensor2tensor.utils import registry

@registry.register_problem
class SandhiSplitter(text_problems.Text2TextProblem):
  """Split sandhi. From Gutenberg texts."""

  @property
  def approx_vocab_size(self):
    return 2**13  # ~8k

  @property
  def is_generate_per_split(self):
    # generate_data will shard the data into TRAIN and EVAL for us.
    return False

  @property
  def dataset_splits(self):
    """Splits of data to produce and number of output shards for each."""
    # 10% evaluation data
    return [{
        "split": problem.DatasetSplit.TRAIN,
        "shards": 9,
    }, {
        "split": problem.DatasetSplit.EVAL,
        "shards": 1,
    }]

  def generate_samples(self, data_dir, tmp_dir, dataset_split):
    filename = '/home/yzk/Dropbox/univ/JMC/code/data/rv_samhita-pada.tsv'
    dt = pd.read_csv(filename, delimiter='\t')
    for key, row in dt.iterrows():
        s, p = row['samhita'], row['pada']
        if not s or not p:
            continue
        yield{
            'inputs': s.strip(),
            'targets': p.strip()
        }