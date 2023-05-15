
#!/bin/bash

# Stop script on error
set -e

# Import environment variables
set -a
source ./.env
set +a

cd "$GTAW_REPO_DIR/build"
echo "Copying local build files to QA server"
scp -i ~/.ssh/gtaw-qa-server-ssh-key ./GTALife* gtaw@gtaw-qa-server:/home/gtaw/ragemp-srv/dotnet/resources/GTALife
