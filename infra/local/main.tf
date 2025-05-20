provider "aws" {
  region                      = "ap-northeast-1"
  access_key                  = "test"
  secret_key                  = "test"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    cloudwatch = "http://host.docker.internal:4566"
    logs       = "http://host.docker.internal:4566"
  }
}


resource "aws_cloudwatch_log_group" "local_log_group" {
  name              = "/localstack/app"
  retention_in_days = 7
}

resource "aws_cloudwatch_log_stream" "local_log_stream" {
  name           = "app-stream"
  log_group_name = aws_cloudwatch_log_group.local_log_group.name
}
