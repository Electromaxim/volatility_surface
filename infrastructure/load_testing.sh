#!/bin/bash
# Load testing for 5x peak volume (Zurich region)

# Environment setup
export AWS_REGION="eu-central-2"
export LOAD_FACTOR=5
export TEST_DURATION=3600  # 1 hour

# Start GPU cluster
aws autoscaling set-desired-capacity \
  --auto-scaling-group-name vol-calibration-asg \
  --desired-capacity $LOAD_FACTOR \
  --region $AWS_REGION

# Execute load test
python -m locust -f load_tests/calibration_load.py \
  --headless \
  -u $((100 * $LOAD_FACTOR)) \
  -r 10 \
  -t ${TEST_DURATION}s \
  --csv=load_test_results

# Validate success criteria
FAILURE_RATE=$(awk -F, 'END{print $6}' load_test_results_stats.csv)
if (( $(echo "$FAILURE_RATE > 0.01" | bc -l) )); then
  echo "Load test failed: $FAILURE_RATE% failure rate"
  exit 1
else
  echo "Load test passed: $FAILURE_RATE% failure rate"
  exit 0
fi