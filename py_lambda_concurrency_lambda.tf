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

  # The filebase64sha256() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the base64sha256() function and the file() function:
  # source_code_hash = "${base64sha256(file("lambda_function_payload.zip"))}"
  source_code_hash = "${filebase64sha256("py_lambda_concurrency_lambda.zip")}"

  memory_size = 1024
  runtime = "python3.8"
}
