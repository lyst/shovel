# Shovel

You can version-control your code, you want to version-control your datasets too.
Very many data science workflows can be broken down into working on three stages of data:
- "input": the dataset as provided to you, a query against Redshift, a query against Postgres, a query against your favourite API...
- "working": various transformations that you do.
- "output": various results, such as the accuracy of an ML algorithm on this dataset, summary graphs, etc.

The principle of `shovel` is to help store and version your "input", when combined with versioned code all of your results can be reproducible.
How you manage your "working" and your "output" is out-of-scope, and up to you.
This is the first major goal of `shovel`: making it easier to reproduce results in the future.

The second major goal is to store our datasets centrally (on S3 for now), so that everyone may access everything.
This is good for collaboration.
This is also good for organising our datasets, and for backing them up.

## Installation

To install,
```bash
python setup.py install
```

(For development, `python setup.py develop` works.)

If you want to install directly from git, use:
```bash
pip install git+https://github.com/lyst/shovel.git#egg=shovel
```

Shovel reads its config from the environment. As a minimum, you need the following environment variables defines:
- AWS_ACCESS_KEY_ID - for boto
- AWS_SECRET_ACCESS_KEY - for boto 
- SHOVEL_DEFAULT_BUCKET - the bucket in which to store your data
 
In addition:
- SHOVEL_DEFAULT_ROOT (bottomless-pit) - the root prefix for the default Pit your data will be stored in (shovel will always include this as the prefix when writing to your bucket. 

## Fetching datasets from your Pit

`shovel` imposes that datasets should live in a namespace `PROJECT/DATASET/VERSION`.
- PROJECT is the top-level project a dataset belongs to, e.g. `google-ngrams`...
- DATASET is the name of the dataset. This is intended to contain different datasets e.g. `eng-all-20120701`  
- VERSION is the version number and shold be in the format `f"v{int(n)"` and is intended to be used if errors are found in the dataset and they need updating. It should always make sense to re-run some analyses on the latest version of the dataset.

You should consider using a pre-existing dataset over creating a new one, if an appropriate one exists.

Using the `shovel` command-line tool, fetch existing datasets with
```bash
shovel dig <LOCAL_DIRECTORY> <PROJECT> <DATASET> <VERSION>
```

to fetch the dataset into `LOCAL_DIRECTORY`. For example `shovel dig ~/google-ngrams/english2012 google-ngrams eng-all-20120701 v0`

Or from python
```python
from shovel import dig

dig('~/google-ngrams/english2012', 'google-ngrams', 'eng-all-20120701', 'v0')
```

## Preparing and pushing datasets to S3

Push a local directory containing a dataset to S3 with
```bash
shovel bury ~/google-ngrams/english2012 google-ngrams eng-all-20120701 v0
```

Or from python
```python
from shovel import dig

bury('~/google-ngrams/english2012', 'google-ngrams', 'eng-all-20120701', 'v0')
```

`bury` will fail if the version already exists.

Enough talk...

![Shovel][shovel]

[shovel]: https://www.mememaker.net/static/images/memes/4104864.jpg
