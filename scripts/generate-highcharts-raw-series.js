const fs = require('fs');
const dataFolder = './data/dontcommit/Shanghai';

let data = [];
fs.readdirSync(dataFolder).forEach(file => {
  try {
    const dailyData = JSON.parse(fs.readFileSync(`${dataFolder}/${file}`));
    dailyData.forEach((measurement) => {
      const timestamp = new Date(measurement.local).getTime();
      const value = measurement.value;
      data.push([timestamp, value]);
    });
  } catch (e) {
    console.log(`caught error: ${e}`)
  }
});

fs.writeFileSync('./data/commit/Shanghai/highcharts-series-raw-2016.json', JSON.stringify(data, null, 2));

// data = fs.readFileSync('/Users/aimeebarciauskas/Downloads/highcharts-series-raw-kathmandu.json')
// data = JSON.parse(data)
// data = data.filter(x => x[1] !== -999)
// data = data.sort()
// data = data.filter((x, idx) => data[idx+1] && x[0] !== data[idx+1][0])
// fs.writeFileSync('data/commit/kathmandu/highcharts-series-raw.json', JSON.stringify(data, null, 2))
