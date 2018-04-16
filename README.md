# OpenAQ Tools

OpenAQ Tools is a repository for scripts and visualizations built on top of OpenAQ data. hi

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

#### Scripts

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

