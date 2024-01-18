# SQLite-AWS-EFS-AWS-Lambda

I was investigating the feasibility of using an AWS lambda function to interact with a SQLite database on AWS EFS. 

I've dumped all of my testing code into this repo, in case that it is useful for someone.

I found it all a bit of a mission to set up (VPC, subnet, access point, security, IAM roles etc.) but it worked eventually (I followed [this guide](https://aws.amazon.com/blogs/compute/using-amazon-efs-for-aws-lambda-in-your-serverless-applications/))

You can see my lambda function code in [lambda_function.py](./lambda_function.py). This code is very dirty - I was using it by 
commenting and uncommenting different bits as needed - but there are useful code snippets in there. 

I load-tested by sending concurrent write requests using [load_test.py](./load_test.py).  
e.g. you can run 100 concurrent requests using
```bash
python load_test.py 100
```

Attempting more than 1 concurrent write to the database (even as few as 10), I was hit immediately with 'disk I/O' and 'database locked' errors. 
I've confirmed that the issue is not related to SQLite (you can see my code [here](https://github.com/J-sephB-lt-n/sqlite-concurrent-writes-investigation) showing that SQLite can handle thousands of concurrent write and read connections) but rather with EFS.

Incidentally, the solution that we actually went with was data on S3 queried with Amazon Athena. 

# Useful references 

* https://aws.amazon.com/blogs/compute/using-amazon-efs-for-aws-lambda-in-your-serverless-applications/
