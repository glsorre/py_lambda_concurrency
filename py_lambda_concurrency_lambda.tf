provider "aws" {
  region  = "eu-west-1"
  shared_credentials_file = "~/.aws/config"
  version = "~> 2.54"
}

resource "aws_iam_role" "py_lambda_concurrency_role" {
  name = "py_lambda_concurrency_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_lambda_function" "py_lambda_concurrency_lambda" {
  filename      = "py_lambda_concurrency_lambda.zip"
  function_name = "py_lambda_concurrency_lambda"
  role          = "${aws_iam_role.py_lambda_concurrency_role.arn}"
  handler       = "app.lambda_handler"

  source_code_hash = "${filebase64sha256("py_lambda_concurrency_lambda.zip")}"

  timeout = "120"
  memory_size = "2560"
  runtime = "python3.8"
}
