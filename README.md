# OpenAQ Tools

OpenAQ Tools is a repository for scripts and visualizations built on top of OpenAQ data.

## Target Audience

The target audience of OpenAQ tools is data journalists and the general public with an interest in air inequality and data transparency.

## How to use

The contents of this repository include:

* `index.html`: A visualization of some data generated using OpenAQ
* `scripts/`: Scripts for downloading, cleaning and managing OpenAQ data

### Interface

The current interface is the very first iteration and only represents pm2.5 data from Shanghai over the latter half of 2015.

It is viewable at [datakind-dc.github.io/openaq-tools/](https://datakind-dc.github.io/openaq-tools/).

You can also run it locally if you have python or another web server installed on your computer:

```bash
git clone https://github.com/datakind-dc/openaq-tools
cd openaq-tools
python -m SimpleHTTPServer # <- or another web server
```

Open your browser at the local port your web server is running.

### Data Generation

#### Prerequisites

* [node](https://nodejs.org/en/) >= 8.9
* [nvm](https://github.com/creationix/nvm)

#### Installation

```bash
nvm use
npm install
```

#### Backfilling data for the dashboard

The dashboard was generated using 2 lambda functions (detailed below) deployed into an AWS account.

![backfill architecture](https://docs.google.com/drawings/d/e/2PACX-1vT6pOQnU8IEfwjha92XBe8-uqvf-g9uq1uxqnMmpPGTFJbRyV_2SWOC9ZKQlrxkMyXD6H69MeiTZGQ1/pub?w=1277&h=567)

#### Scripts

**[`scripts/lambdas/copy-to-from-s3/`](./scripts/lambdas/copy-to-from-s3)**

AWS Lambda code for getting data from openaq's s3 and dumping it into another S3 bucket. Used to trigger generate_highcharts lambda for generating data for the dashboard. Currently, the S3 bucket is hardcoded to `aimeeb-datasets`.

There is also code to invoke (see `function invoker`) the copy-to-from-s3 lambda function, so the lambda handler function can be invoked many times, e.g. once for every day in a period of days, to maximize parallelization of copy data from one s3 to another. HERE BE DRAGONS $$.

**[`scripts/lambdas/generate_highcharts.py`](./scripts/lambdas/generate_highcharts.py)**

The `generate_highcharts` lambda function is designed to be triggered when new data lands in S3 as deliverd by `copy-to-from-s3`. It loads the "just arrived" data (which is really old data, its just a copy operation to create a trigger event), which it expects to be a daily CSV export, generates data in the format that highcharts expets, and then stores this data in S3 for the dashboard to find. Right now, the S3 bucket in use by the dashboard and this function is hardcoded as `aimeeb-datasets-public`.

**[`scripts/request-and-clean.js`](./scripts/request-and-clean.js)**

* Requests daily data files from `https://openaq-data.s3.amazonaws.com`.
* Downloads all data from dates defined in that script.
* Currently filters data to measurements of metric pm25.
* Groups data by location and writes daily values, by location to `data/dontcommit/<location>/<date>.json`.
* Includes option `locationsFilter` which limits data saved to disk to only locations defined in that list.

To download data, update the date range in [`scripts/request-and-clean.js`](./scripts/request-and-clean.js) if required.

```bash
node scripts/request-and-clean.js
```

**[`scripts/generate-highcharts-raw-series.js`](./scripts/generate-highcharts-raw-series.js)**

Concatenates pm2.5 values and timestamps in `dontcommit/Shanghai` - which may or may not exists to generate `data/commit/highcharts-series-raw.json` which is used in the current visualization.

