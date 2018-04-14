const _ = require('lodash');
const csv = require('csvtojson');
const fs = require('fs');
const moment = require('moment');
const request = require('request');
const yaml = require('js-yaml');

const baseUrl = 'https://openaq-data.s3.amazonaws.com'
const Flagger = require('../../openaq-quality-checks/lib/flagger');
const config = yaml.safeLoad(fs.readFileSync('scripts/config.yml', 'utf8'));

const startDate = moment('2015-08-03');
const endDate = moment('2015-12-31');
let currentDate = startDate;

// If you want an exclusive end date (half-open interval)
for (let currentDate = moment(startDate); currentDate.isBefore(endDate); currentDate.add(1, 'days')) {
  const currentDateString = currentDate.format('YYYY-MM-DD');

  request(`${baseUrl}/${currentDateString}.csv`, function (error, response, body) {
    console.log('error:', error); // Print the error if one occurred
    console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
    const csvStr = body;
    let measurements = [];

    csv({checkType: true}).fromString(csvStr)
      .on('json', (jsonObj) => {
        measurements.push(jsonObj);
      })
      .on('done',() => {
        // filter pm2.5
        measurements = measurements.filter((measurement) => {
          return measurement.parameter === 'pm25'
        });

        // remove flagged data
        let flaggedData = measurements;
        Object.values(config).forEach((flagConfig) => {
          const flagger = new Flagger(flagConfig);
          flaggedData = flagger.flag(flaggedData);
        });
        const filteredData = flaggedData.filter(datum => !(datum.flags && datum.flags.length > 0));

        // group by location and write to files
        // /data/<location>/<date>.json
        const groups = _.groupBy(filteredData, 'location');
        Object.keys(groups).forEach((locationName) => {
          const locationData = groups[locationName];
          const directory = `./data/${locationName.split(' ').join('_')}`;
          // TODO(aimee): Fix { Error: ENOENT: no such file or directory, mkdir './data/Horst_a/d_Maas-Hoogheide'
          try {
            if (!fs.existsSync(directory)) fs.mkdirSync(directory);

            fs.writeFileSync(
              `${directory}/${currentDateString}.json`,
              JSON.stringify(locationData, null, 2),
              'utf-8'
            ); 
          } catch (e) {
            console.log(e);
          }
        });
      });
  });
};
