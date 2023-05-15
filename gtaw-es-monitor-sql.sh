#!/bin/bash

# Stop script on error
set -e

# Import environment variables
set -a
source ./.env
set +a

readonly DISCORD_BOT_AUTHORIZATION="authorization: Bot $DISCORD_TOKEN"

send_discord_message() {
	local message="$1"
	local payload=""
	payload+='{"content":"'
	payload+="$message"
	payload+='","tts":false,"flags":0}'
	echo "send_discord_message: $message"
	curl 'https://discord.com/api/v9/channels/103087705637893598/messages' \
		-H "$DISCORD_BOT_AUTHORIZATION" \
		-H 'content-type: application/json' \
		--data-raw "$payload" \
		--compressed
}

file_removed() {
	local message="The file $1$2 was removed"
	send_discord_message "$message"
}

file_modified() {
	local message="The file $1$2 was modified"
	send_discord_message "$message"
}

file_created() {
	local message="The file $1$2 was created"
	send_discord_message "$message"
}

# Check script arguments
if [[ $# -ne 1 ]]; then
	echo "USAGE: $0 <path>" >&2
	exit 1
fi

inotifywait -q -m -r -e modify,delete,create $1 | while read DIRECTORY EVENT FILE; do
	case $EVENT in
		MODIFY*)
			file_modified "$DIRECTORY" "$FILE"
			;;
		CREATE*)
			file_created "$DIRECTORY" "$FILE"
			;;
		DELETE*)
			file_removed "$DIRECTORY" "$FILE"
			;;
	esac
done
