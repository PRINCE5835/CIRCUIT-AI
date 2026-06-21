#!/usr/bin/env bash
set -euo pipefail

echo "Health Check:"
echo "-------------"

check() {
    local name=$1 url=$2
    if curl -sf "$url" > /dev/null 2>&1; then
        echo "✓ $name is healthy"
    else
        echo "✗ $name is unreachable"
    fi
}

check "Backend" "http://localhost:8000/health"
check "AI Engine" "http://localhost:8001/health"
check "Ollama" "http://localhost:11434/api/tags"
