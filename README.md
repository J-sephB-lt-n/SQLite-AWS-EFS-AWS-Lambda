# SQLite-AWS-EFS-AWS-Lambda

I was investigating the feasibility of using an AWS lambda function to interact with a SQLite database saved onto AWS EFS. 

I've dumped all of my testing code into this repo, in case that it is useful for someone.

I found it a bit of a mission to set up (VPC, subnet, access point, security, IAM roles etc.) but it worked eventually (I followed [this guide](https://aws.amazon.com/blogs/compute/using-amazon-efs-for-aws-lambda-in-your-serverless-applications/))

You can see my lambda function code in [lambda_function.py](./lambda_function.py). This code is very dirty - I was using it by 
commenting and uncommenting different bits as needed - but there are useful code snippets in there. 

I load-tested by sending concurrent write requests using [load_test.py](./load_test.py).  
e.g. you can run 100 concurrent requests using
```bash
python load_test.py 100
```

Attempting more than 1 concurrent write to the database (even as few as 10), I was hit immediately with 'disk I/O' and 'database locked' errors. 
I couldn't immediately solve these problems with WAL and locking_mode=EXCLUSIVE, so I've given up for now. I'd like to return to this pattern at
some later stage and work it out.

# Useful references 

* https://aws.amazon.com/blogs/compute/using-amazon-efs-for-aws-lambda-in-your-serverless-applications/
