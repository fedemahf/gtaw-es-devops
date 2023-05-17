
#!/bin/bash

# Stop script on error
set -e

# Import environment variables
set -a
source ./.env
set +a

readonly DISCORD_BOT_AUTHORIZATION="authorization: Bot $DISCORD_TOKEN"

# Used to track the last known phase and display it on `handle_error()`
last_known_phase="Starting"

# Update and print the last known phase
# Syntax: set_last_known_phase <text>
set_last_known_phase() {
	last_known_phase=$1
	echo $last_known_phase
}

send_discord_message() {
	local message="$1"
	local payload=""
	payload+='{"content":"'
	payload+="$message"
	payload+='","tts":false,"flags":0}'
	echo "send_discord_message: $message"	
	curl 'https://discord.com/api/v9/channels/1030877056378093598/messages' \
		-H "$DISCORD_BOT_AUTHORIZATION" \
		-H 'content-type: application/json' \
		--data-raw "$payload" \
		--compressed
}

handle_error() {
	local error_code=$1
	if [[ $error_code -ne 0 ]]; then
		send_discord_message "Deploy to QA - ERRNO $error_code - Last known phase: $last_known_phase"
		exit 1
	fi
}

# Catch and handle errors (note the simple quotes!)
trap 'handle_error $?' ERR

send_discord_message "Starting deploy to QA"

set_last_known_phase "Fetching from GitHub"
cd "$GTAW_LOCAL_REPO_DIR"
git fetch origin
git checkout Spain-staging

if [[ ! $(git status -uno) =~ "Your branch is behind" ]]; then
	send_discord_message "The build files are up to date"
	exit 0
fi

set_last_known_phase "Pulling from GitHub"
git pull

set_last_known_phase "Building"
./scripts/docker-builder/docker-builder.sh

set_last_known_phase "Pushing to GitHub"
git add .
git commit -m 'Update build files'
git push

send_discord_message "Copying local build files to QA server"
scp -i $GTAW_SSH_KEY_PATH $GTAW_LOCAL_REPO_DIR/build/GTALife* $GTAW_SSH_USER@$GTAW_SSH_HOST:$GTAW_REMOTE_BUILD_FILES_PATH

send_discord_message "Deploy to QA done"
exit 0
