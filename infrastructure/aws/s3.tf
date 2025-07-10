resource "aws_s3_bucket" "audit_logs" {
  bucket = "rothschild-audit-logs"
  
  object_lock_enabled = true
  
  lifecycle_rule {
    enabled = true
    transition {
      days          = 30
      storage_class = "GLACIER"
    }
    expiration {
      days = 2555  # 7 years
    }
  }
}