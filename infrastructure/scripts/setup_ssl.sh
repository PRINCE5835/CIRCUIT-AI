#!/usr/bin/env bash
set -euo pipefail

DOMAIN="${1:-breadboard.ai}"
EMAIL="${2:-admin@breadboard.ai}"

if ! command -v certbot &>/dev/null; then
    echo "Installing certbot..."
    apt-get update && apt-get install -y certbot python3-certbot-nginx
fi

certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos -m "$EMAIL"

mkdir -p ./docker/nginx/ssl
cp "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ./docker/nginx/ssl/
cp "/etc/letsencrypt/live/$DOMAIN/privkey.pem" ./docker/nginx/ssl/

echo "SSL certificates for $DOMAIN have been provisioned."
echo "To auto-renew: certbot renew"
