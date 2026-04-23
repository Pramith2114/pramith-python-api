#!/usr/bin/env sh
set -e

API_URL=${API_URL:-http://api:8000/api/users}
USER_NAME=${USER_NAME:-Alice Smith}
USER_MOBILE=${USER_MOBILE:-+919876543211}
USER_EMAIL=${USER_EMAIL:-alice@example.com}
USER_PASSWORD=${USER_PASSWORD:-password123}
USER_ROLE=${USER_ROLE:-patient}

cat <<EOF > /tmp/user_payload.json
{
  "name": "${USER_NAME}",
  "mobile": "${USER_MOBILE}",
  "email": "${USER_EMAIL}",
  "password": "${USER_PASSWORD}",
  "role": "${USER_ROLE}"
}
EOF

curl -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d @/tmp/user_payload.json
