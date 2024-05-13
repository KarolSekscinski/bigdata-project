#!/bin/bash

# Command to execute within the Docker container
docker exec -i hive-server /bin/bash <<EOF
# Run the script inside the container
bash /scripts/load-data.sh
EOF