# Sourced by the deploy-cf*.sh scripts. Loads the Cloudflare credentials unless
# they are already in the environment. Never echo the values.
if [[ -z "${CLOUDFLARE_API_TOKEN:-}" || -z "${CLOUDFLARE_ACCOUNT_ID:-}" ]]; then
  CLOUDFLARE_ENV_FILE="${CLOUDFLARE_ENV_FILE:-/data/projects/sciscend/.private/cloudflare.env}"
  [[ -f "$CLOUDFLARE_ENV_FILE" ]] || { echo "✗ No Cloudflare credentials: set CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID, or CLOUDFLARE_ENV_FILE"; exit 1; }
  set -a
  # shellcheck disable=SC1090
  source "$CLOUDFLARE_ENV_FILE"
  set +a
fi
