# pandas-wheather-anlysis



## Main Goal

Convert sample data to parquet.

### Requirements

These are the requirements for running this project:

* Python 3.8;
* AWS SAM CLI;
* AWS CLI;
* AWS IAM User with permission to access AWS via CLI.


### Steps invoked after uploading a file

* S3 notification using SNS when a new file is uploaded;
* Lambda functions is triggered by SNS and then invoke a step function (for better monitor and for demonstration purposes)
* Step Function calls the first lambda that read csv files, convert to parquet and create/overwrite partitions of a table, moves files to a processed folder
* Step Function calls the second lambda that reads from Athena and show which was the max temperature



### How to run

For creating the stack:
```bash
cd infra
sh deploy.sh {bucket-for-upload-cloudformation} {environment}.properties
```

For upload some sample data:
```bash
sh upload_file.sh {bucket-created-in-the-first-step}
```


### Sample of the result

![Execution result](/images/answer.jpg)