#!/bin/bash
set -x
set -e

AWS_ACCESS_KEY_ID='' AWS_SECRET_ACCESS_KEY='' SHOVEL_DEFAULT_BUCKET='test_bucket' SHOVEL_DEFAULT_ROOT='test_root' py.test --strict $@
