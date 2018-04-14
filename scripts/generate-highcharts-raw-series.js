const fs = require('fs');
const dataFolder = './data/dontcommit/Shanghai';

let data = [];
fs.readdirSync(dataFolder).forEach(file => {
  const dailyData = JSON.parse(fs.readFileSync(`${dataFolder}/${file}`));
  dailyData.forEach((measurement) => {
    const timestamp = new Date(measurement.local).getTime();
    const value = measurement.value;
    data.push([timestamp, value]);
  });
});

fs.writeFileSync('./data/commit/Shanghai/highcharts-series-raw.json', JSON.stringify(data, null, 2));
