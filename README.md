## This is the repo for a financial econometrics project, creating portfolios that maximise Sharpe ratio

## About

Written by Jakob Bull, Patrick Dickinson, and Zachary Parsons for info contact <jakob.bull@yahoo.de>

## Setup

To quickly get setup follow these steps in a Terminal:

cd into a file location of your choice amd run:

`git clone https://github.com/JakobBull/chinese_stocks.git`

Once you are cloned into the repo

`conda create --name stocks`

Then activate the environment

`conda activate stocks`

Install the requirements:

`conda install --file requirements.txt`

Once you are set up please refrain from working in the main branch, instead run:

`git checkout -b {insert-name}` with a branch name of your choice

## Usage

For usage example refer to `notebook.ipynb`

The Portfolio class in `portfolio.py` is standard. The `strategies` folder contains various strategies, please add your own here. An example can be found in `nfixedbaskets.py`
For strategies please respect the dictionary return format:

    {
        pd.Timestamp:{'ticker_name_a: time_1_weight_a, 'ticker_name_b: time_1_weight_b, ...}, 
        pd.Timestamp:{'ticker_name_c: time_2_weight_c, 'ticker_name_d: time_1_weight_d, ...}, 
        ...
        }

Where the dictionary must contain a time stamp for every single time period in the testing time frame at current. Additionally all weights at any time point must sum to 1.