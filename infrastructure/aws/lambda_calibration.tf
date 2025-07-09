module "vol_calibration_lambda" {
  source = "terraform-aws-modules/lambda/aws"
  
  function_name = "rothschild-vol-calibration"
  handler       = "pricing.handler"
  runtime       = "python3.10"
  timeout       = 900  # 15-minute FINMA limit

  environment_variables = {
    S3_BUCKET     = "rothschild-options-data"
    REDIS_ENDPOINT = aws_elasticache_cluster.vol_surface.cache_nodes[0].address
  }

  vpc_config = {
    subnet_ids         = var.zurich_subnets
    security_group_ids = [aws_security_group.lambda_sg.id]
  }
}