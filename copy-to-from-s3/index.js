const moment = require('moment');
const request = require('request');
const { S3, Lambda } = require('aws-sdk');
const s3 = new S3();
const lambda = new Lambda({region: 'us-east-1'});

const baseUrl = 'https://openaq-data.s3.amazonaws.com'

const bucketName = 'aimeeb-datasets';
const bucketPrefix = 'openaq/source';

async function handler(event, context, cb) {
  const currentDate = moment(event.date || '2015-06-29');
  // If you want an exclusive end date (half-open interval)
  const currentDateString = currentDate.format('YYYY-MM-DD');
  await request(`${baseUrl}/${currentDateString}.csv`, function (error, response, body) {
    if (error) {
      console.log('error:', error);
      return cb(error);
    }; // Print the error if one occurred
    const csvStr = body;
    const keyName = `${bucketPrefix}/${currentDateString}.csv`;
    const params = {Bucket: bucketName, Key: keyName, Body: body};
    s3.putObject(params, function(err, data) {
      if (err) cb(err);
    });
  });
  return cb(null, 'Success'); 
};

async function invoker(event, context, cb) {
  const startDate = moment(event.startDate || '2015-06-29');
  const endDate = moment(event.endDate || '2015-06-30');

  let currentDate = startDate;
  for (let currentDate = moment(startDate); currentDate.isBefore(endDate); currentDate.add(1, 'days')) {
    console.log('invoking function')
    const currentDateString = currentDate.format('YYYY-MM-DD');  
    const params = {
      FunctionName: 'copyToFromS3', 
      InvocationType: 'Event', 
      Payload: JSON.stringify({date: currentDateString})
    };
    await lambda.invoke(params, (err, data) => {
      if (err) {
        cb(err);
        console.log(err);
      }
    });
  }
  return cb(null, 'Success');
}

exports.handler = handler;
exports.invoker = invoker;
invoker({startDate: '2016-05-31', endDate: '2016-12-31'}, {}, (err, result) => {
  if (err) console.log(err);
  return result;
});
