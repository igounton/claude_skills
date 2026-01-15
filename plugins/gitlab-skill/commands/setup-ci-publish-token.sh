#!/usr/bin/env sh
# setup-ci-publish-token.sh
# Creates or renews CI_PUBLISH_TOKEN for GitLab CI/CD publishing

set -eu

# Constants
TOKEN_NAME="ci-publish-token"
VAR_NAME="CI_PUBLISH_TOKEN"

# Load existing .env if present and non-empty
[ -s .env ] && . ./.env

# Set the token for the environment
GITLAB_TOKEN="${GITLAB_TOKEN:-${GL_TOKEN:-${CI_JOB_TOKEN:-}}}"
export GITLAB_TOKEN

if [ -z "${GITLAB_TOKEN:-}" ]; then
    echo "ERROR: You need a GITLAB_TOKEN set in your environment to do this."
    exit 1
fi

if [ ! -d .git ]; then
    echo "ERROR: You must be in the git root directory to do this."
    exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
    echo "ERROR: You need jq installed. Try 'brew install jq'"
    exit 1
fi

if ! command -v glab >/dev/null 2>&1; then
    echo "ERROR: You need glab installed. Try 'brew install glab'"
    exit 1
fi

in_dotenv() { [ -e .env ] && grep -q "^$1=" .env; }
in_env() { env | grep -q "^$1="; }

# --- Environment variable detection ---

if ! in_env GITLAB_HOST && ! in_dotenv GITLAB_HOST; then
    if [ -z "${CI_SERVER_HOST:-}" ]; then
        GITLAB_HOST="$(sed -n 's/.*url = git@\([^:]*\):.*/\1/p; s/.*url = https:\/\/\([^/]*\)\/.*/\1/p' .git/config | head -1)"
    else
        GITLAB_HOST="${CI_SERVER_HOST}"
    fi
fi

if ! in_env CI_PROJECT_PATH && ! in_dotenv CI_PROJECT_PATH; then
    CI_PROJECT_PATH="$(sed -n 's/.*url = git@[^:]*:\(.*\)\.git$/\1/p; s/.*url = https:\/\/[^/]*\/\(.*\)\.git$/\1/p' .git/config | head -1)"
fi

if ! in_env GITLAB_USER_ID && ! in_dotenv GITLAB_USER_ID; then
    GITLAB_USER_ID="$(glab api user | jq '.id')"
fi

# --- Persist to .env if not in CI ---

if [ -z "${GITLAB_CI:-}" ]; then
    [ ! -e .env ] && touch .env
    [ ! -e .gitignore ] && touch .gitignore
    grep -qE '^\s*/?\.env\s*$' .gitignore || printf "# Ignore localized environment variables\n.env\n" >>.gitignore
    [ -s .env ] && . ./.env
    in_dotenv GITLAB_HOST || echo "GITLAB_HOST=${GITLAB_HOST}" >>.env
    in_dotenv CI_PROJECT_PATH || echo "CI_PROJECT_PATH=${CI_PROJECT_PATH}" >>.env
    in_dotenv GITLAB_USER_ID || echo "GITLAB_USER_ID=${GITLAB_USER_ID}" >>.env
fi

# URL-encode the project path for API calls
CI_PROJECT_PATH_ENCODED=$(printf '%s' "${CI_PROJECT_PATH}" | sed 's/\//%2F/g')

export GITLAB_HOST CI_PROJECT_PATH GITLAB_USER_ID CI_PROJECT_PATH_ENCODED

# --- Permission checks ---

has_api_scope() {
    if glab api personal_access_tokens/self | jq -e '.scopes | index("api")' >/dev/null 2>&1; then
        return 0
    else
        echo "ERROR: The current GITLAB_TOKEN does not have the 'api' scope."
        exit 1
    fi
}

has_maintainer_access() {
    access_level=$(glab api "projects/${CI_PROJECT_PATH_ENCODED}/members/all/${GITLAB_USER_ID}" | jq -r '.access_level')
    if [ "${access_level:-0}" -ge 40 ]; then
        return 0
    else
        echo "ERROR: The current GITLAB_TOKEN does not have Maintainer (40) or higher access to ${CI_PROJECT_PATH}."
        exit 1
    fi
}

has_api_scope
has_maintainer_access

# --- Check token and variable status ---

token_json=$(glab token list --repo "${CI_PROJECT_PATH}" --output json)
token_info=$(echo "${token_json}" | jq -r "if . == null then empty else .[] | select(.name == \"${TOKEN_NAME}\") end")

# Filter out the "Listing variables..." line, default to empty array if no match
var_json=$(glab variable list --repo "${CI_PROJECT_PATH}" --output json 2>/dev/null | grep '^\[' || echo '[]')
if echo "${var_json}" | jq -e ".[] | select(.key == \"${VAR_NAME}\")" >/dev/null 2>&1; then
    var_exists="true"
else
    var_exists="false"
fi

# --- Decision logic ---

# Case 4: No token exists - CREATE NEW
if [ -z "${token_info}" ]; then
    echo "INFO: Creating project access token '${TOKEN_NAME}'..."
    NEW_TOKEN=$(glab token create "${TOKEN_NAME}" \
        --repo "${CI_PROJECT_PATH}" \
        --access-level maintainer \
        --scope api \
        --scope write_repository \
        --duration 8760h \
        --description "CI/CD token for publishing releases and uploading artifacts" \
        --output text)

    echo "INFO: Setting CI variable '${VAR_NAME}'..."
    echo "${NEW_TOKEN}" | glab variable set "${VAR_NAME}" \
        --repo "${CI_PROJECT_PATH}" \
        --masked \
        --protected \
        --description "Project access token for CI/CD release publishing and artifact uploads"

    echo "DONE: Token and variable created."
    exit 0
fi

# Token exists - check expiry
expires_at=$(echo "${token_info}" | jq -r '.expires_at')
today=$(date +%Y-%m-%d)

# Convert YYYY-MM-DD to integer for POSIX-compatible comparison
expires_int=$(echo "${expires_at}" | tr -d '-')
today_int=$(echo "${today}" | tr -d '-')

# Case 2: Token expired - RENEW
if [ "${expires_int}" -lt "${today_int}" ]; then
    echo "INFO: Token expired (${expires_at}). Rotating..."
    NEW_TOKEN=$(glab token rotate "${TOKEN_NAME}" --repo "${CI_PROJECT_PATH}" --output text)

    echo "INFO: Updating CI variable '${VAR_NAME}'..."
    echo "${NEW_TOKEN}" | glab variable update "${VAR_NAME}" --repo "${CI_PROJECT_PATH}"

    echo "DONE: Token rotated and variable updated."
    exit 0
fi

# Case 3: Token valid but variable missing - ROTATE to get new value
if [ "${var_exists}" = "false" ]; then
    echo "INFO: Token '${TOKEN_NAME}' exists (expires ${expires_at}) but CI variable '${VAR_NAME}' is missing."
    echo "INFO: Rotating token to obtain a new value..."
    NEW_TOKEN=$(glab token rotate "${TOKEN_NAME}" --repo "${CI_PROJECT_PATH}" --output text)

    echo "INFO: Setting CI variable '${VAR_NAME}'..."
    echo "${NEW_TOKEN}" | glab variable set "${VAR_NAME}" \
        --repo "${CI_PROJECT_PATH}" \
        --masked \
        --protected \
        --description "Project access token for CI/CD release publishing and artifact uploads"

    echo "DONE: Token rotated and variable created."
    exit 0
fi

# Case 1: Token valid and variable exists - SKIP
echo "OK: Already configured. Token '${TOKEN_NAME}' expires ${expires_at}."
exit 0
