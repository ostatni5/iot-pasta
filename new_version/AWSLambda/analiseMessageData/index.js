'use strict'
const AWS = require("aws-sdk");
const DB_API_VERSION = "2012-10-08";
const AWS_REGION = "us-east-1";

AWS.config.update({ region: AWS_REGION});

exports.handler = async (event, context)  => {
    const DDB = new AWS.DynamoDB({ apiVersion: DB_API_VERSION});
    const documentClient = new AWS.DynamoDB.DocumentClient({ region: AWS_REGION});

    const params = {
        TableName: "Messages",
        Key: {
            // TODO
        }
    }

    try {
        const data = await documentClient.get(params).promise();
        console.log(data);
        // TODO analise
    } catch(err){
        console.log(err);
    }
}