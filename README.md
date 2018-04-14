# OpenAQ Tools

OpenAQ Tools is a repository for scripts and visualizations built on top of OpenAQ data. hi

## Target Audience

The target audience of OpenAQ tools is data journalists and the general public with an interest in air inequality and data transparency.

## How to use

The contents of this repository include:

* `index.html`: A visualization of some data generated using OpenAQ
* `scripts/`: Scripts for downloading, cleaning and managing OpenAQ data
    * `request-and-clean.js`: Requests

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

* node >= 8.9, nvm


