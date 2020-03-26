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
      "Effect": "Allow"
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

  timeout = "900"
  memory_size = "2560"
  runtime = "python3.8"
}

resource "aws_lambda_function" "py_lambda_concurrency_stress_256" {
  filename      = "py_lambda_concurrency_lambda.zip"
  function_name = "py_lambda_concurrency_stress_256"
  role          = "${aws_iam_role.py_lambda_concurrency_role.arn}"
  handler       = "stress.lambda_handler"

  source_code_hash = "${filebase64sha256("py_lambda_concurrency_lambda.zip")}"

  timeout = "900"
  memory_size = "256"
  runtime = "python3.8"
}

resource "aws_lambda_function" "py_lambda_concurrency_stress_768" {
  filename      = "py_lambda_concurrency_lambda.zip"
  function_name = "py_lambda_concurrency_stress_768"
  role          = "${aws_iam_role.py_lambda_concurrency_role.arn}"
  handler       = "stress.lambda_handler"

  source_code_hash = "${filebase64sha256("py_lambda_concurrency_lambda.zip")}"

  timeout = "900"
  memory_size = "768"
  runtime = "python3.8"
}

resource "aws_lambda_function" "py_lambda_concurrency_stress_1280" {
  filename      = "py_lambda_concurrency_lambda.zip"
  function_name = "py_lambda_concurrency_stress_1280"
  role          = "${aws_iam_role.py_lambda_concurrency_role.arn}"
  handler       = "stress.lambda_handler"

  source_code_hash = "${filebase64sha256("py_lambda_concurrency_lambda.zip")}"

  timeout = "900"
  memory_size = "1280"
  runtime = "python3.8"
}

resource "aws_lambda_function" "py_lambda_concurrency_stress_1792" {
  filename      = "py_lambda_concurrency_lambda.zip"
  function_name = "py_lambda_concurrency_stress_1792"
  role          = "${aws_iam_role.py_lambda_concurrency_role.arn}"
  handler       = "stress.lambda_handler"

  source_code_hash = "${filebase64sha256("py_lambda_concurrency_lambda.zip")}"

  timeout = "900"
  memory_size = "1792"
  runtime = "python3.8"
}

resource "aws_lambda_function" "py_lambda_concurrency_stress_2304" {
  filename      = "py_lambda_concurrency_lambda.zip"
  function_name = "py_lambda_concurrency_stress_2304"
  role          = "${aws_iam_role.py_lambda_concurrency_role.arn}"
  handler       = "stress.lambda_handler"

  source_code_hash = "${filebase64sha256("py_lambda_concurrency_lambda.zip")}"

  timeout = "900"
  memory_size = "2304"
  runtime = "python3.8"
}


resource "aws_lambda_function" "py_lambda_concurrency_stress_2816" {
  filename      = "py_lambda_concurrency_lambda.zip"
  function_name = "py_lambda_concurrency_stress_2816"
  role          = "${aws_iam_role.py_lambda_concurrency_role.arn}"
  handler       = "stress.lambda_handler"

  source_code_hash = "${filebase64sha256("py_lambda_concurrency_lambda.zip")}"

  timeout = "900"
  memory_size = "2816"
  runtime = "python3.8"
}
