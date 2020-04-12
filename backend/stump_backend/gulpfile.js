/* jshint node: true */
'use strict';

var gulp = require('gulp');
// https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/
var AWS = require('aws-sdk');
var fs = require('fs');
var os = require('os');
var path = require('path');
var mkpath = require('mkpath');

function listS3Buckets() {
    var s3 = new AWS.S3();
    s3.listBuckets(function(err, data) {
        if (err) console.log(err, err.stack); // an error occurred
        else console.log(data); // successful response
    });
}

function displayCredentials() {
    // Carlos laptop only
    var myHostname = os.hostname();
    var validHostnames = ['oryx'];
    if (validHostnames.indexOf(myHostname) < 0) {
        console.log("displayCredentials() not supported on this host: " + myHostname);
        return;
    }

    AWS.config.getCredentials(function(err) {
        if (err) console.log(err.stack);
        // credentials not loaded
        else {
            console.log("Access key:", AWS.config.credentials.accessKeyId);
            console.log("Secret access key:", AWS.config.credentials.secretAccessKey);
        }
    });
}

function writeFile(filePath, dataBody, bucketKey) {
    var dirname = path.dirname(filePath);
    // This makes nested directory structure, e.g., path/to/subdir1/subdir2
    mkpath(dirname, function (err) {
        if (err) throw err;
        // console.log("Directory structure '" + dirname + "' created");
        // Next, write the file to the file system
        fs.writeFile(filePath, dataBody, function() {
            console.log("Finished: " + bucketKey);
        });
    });
}

// Courtesy of Wogan May
// https://github.com/woganmay/s3-download-bucket/blob/master/download.js
function downloadFromS3(bucketName, targetDirectory) {
    var s3 = new AWS.S3();
    var targetDirectoryWithBuckeName = targetDirectory + "/" + bucketName;

    // Create a bucket subfolder
    fs.mkdirSync(targetDirectoryWithBuckeName);

    // Go!
    s3.listObjects({ Bucket: bucketName }, function(err, data) {
        if (err) console.log(err, err.stack); // an error occurred
        else {
            console.log(data.Contents.length + " files found in '" + bucketName + "' bucket");

            data.Contents.forEach(function(currentValue, index, array) {

                // Check if the file already exists?
                fs.exists(targetDirectoryWithBuckeName + "/" + currentValue.Key, function(exists) {
                    if (exists) {
                        console.log("Skipping: " + currentValue.Key);
                    } else {
                        console.log("Retrieving: " + currentValue.Key);
                        s3.getObject({ Bucket: bucketName, Key: currentValue.Key }, function(err, data) {
                            if (err) console.log(err, err.stack); // an error occurred
                            else {
                                // Make sure the directory exists
                                var filename = targetDirectoryWithBuckeName + "/" + currentValue.Key
                                writeFile(filename, data.Body, currentValue.Key);
                            }
                        }); // s3.getObject
                    } // else
                }); // fs.exists
            }); // foreach
        } // else
    }); // s3.listObjects
} // function download()

function defaultTask(cb) {
    // Debugging only. Don't uncomment unless running on your laptop as the secret credentials
    // will be exposed to the console.
    // displayCredentials();

    downloadFromS3("stump-vote-frontend-demo", "stump_backend/static");

    cb();
}

exports.default = defaultTask;