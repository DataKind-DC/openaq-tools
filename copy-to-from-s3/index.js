const moment = require('moment');
const request = require('request');
const { S3 } = require('aws-sdk');
const s3 = new S3();

const baseUrl = 'https://openaq-data.s3.amazonaws.com'

const startDate = moment(process.env.START_DATE || '2015-06-29');
const endDate = moment(process.env.END_DATE || '2015-06-30');
let currentDate = startDate;
const bucketName = 'aimeeb-datasets';
const bucketPrefix = 'openaq/source';

async function handler(event, context, cb) {

  // If you want an exclusive end date (half-open interval)
  for (let currentDate = moment(startDate); currentDate.isBefore(endDate); currentDate.add(1, 'days')) {
    const currentDateString = currentDate.format('YYYY-MM-DD');
    console.log('startDate')
    console.log(startDate)
    console.log('endDate')
    console.log(endDate)

    await request(`${baseUrl}/${currentDateString}.csv`, function (error, response, body) {
      if (error) {
        console.log('error:', error);
        return cb(error);
      }; // Print the error if one occurred
      console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
      console.log(`Downloaded data for ${currentDateString}`);
      const csvStr = body;
      const keyName = `${bucketPrefix}/${currentDateString}.csv`;
      const params = {Bucket: bucketName, Key: keyName, Body: body};
      s3.putObject(params, function(err, data) {
        if (err) {
          console.log(err)
        } else {
          console.log(`Successfully uploaded data to ${keyName}.json`);
        }
      });
    });
  };
  return cb(null, 'Success'); 
};

exports.handler = handler;
// for testing
// handler({}, {}, (err, result) => {
//   console.log(result);
// });
