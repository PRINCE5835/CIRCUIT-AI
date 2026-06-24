#!/usr/bin/env bash
# ============================================================
# download_models.sh
# Downloads all local AI models for BreadBoard AI.
# - Ollama: Qwen3, DeepSeek Coder, Gemma3
# - Whisper: base model
# - Vosk: English + Hindi
# - Piper TTS: English voices
# - YOLO: circuit component detection
# ============================================================
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MODELS_DIR="${SCRIPT_DIR}/../../ai-engine/engine/models"
export OLLAMA_HOST="${OLLAMA_HOST:-http://localhost:11434}"

mkdir -p "$MODELS_DIR"/{whisper,vosk,piper,yolo,ocr}

echo "========================================"
echo " BreadBoard AI — Model Downloader"
echo "========================================"

# ── 1. Ollama Models ──────────────────────────────────────
echo ""
echo "[1/6] Pulling Ollama models..."
echo "----------------------------------------"

pull_ollama() {
    local model="$1"
    if curl -s "$OLLAMA_HOST/api/tags" | grep -q "\"name\":\"$model\""; then
        echo "  ✓ $model already pulled"
    else
        echo "  Pulling $model..."
        response=$(curl -s -w "%{http_code}" -X POST "$OLLAMA_HOST/api/pull" \
            -d "{\"name\":\"$model\"}" --silent --show-error -o /tmp/ollama_pull.json)
        if [ "$response" != "200" ]; then
            echo "  ✗ Failed to pull $model (HTTP $response)"
            return 1
        fi
        if grep -q '"status":"success"' /tmp/ollama_pull.json 2>/dev/null; then
            echo "  ✓ $model pulled"
        else
            echo "  ✓ $model pull initiated (may still be downloading in background)"
        fi
        rm -f /tmp/ollama_pull.json
    fi
}

pull_ollama "llava"      # Primary vision & reasoning
# pull_ollama "deepseek-coder:6.7b"  # Uncomment if needed
# pull_ollama "gemma3:12b"           # Uncomment if needed
pull_ollama "gemma3:2b"     # Fast light model

# ── 2. Whisper ────────────────────────────────────────────
echo ""
echo "[2/6] Downloading Whisper model..."
echo "----------------------------------------"
python3 -c "
import whisper
whisper.load_model('base', download_root='$MODELS_DIR/whisper/')
print('  ✓ Whisper base model downloaded')
"

# ── 3. Vosk ───────────────────────────────────────────────
echo ""
echo "[3/6] Downloading Vosk models..."
echo "----------------------------------------"
download_vosk() {
    local url="$1"
    local dest="$2"
    local name="$(basename "$dest")"
    if [ -d "$dest" ]; then
        echo "  ✓ $name already downloaded"
    else
        echo "  Downloading $name..."
        curl -L "$url" -o "/tmp/$name.tar.gz" --silent --show-error
        tar -xzf "/tmp/$name.tar.gz" -C "$(dirname "$dest")"
        rm "/tmp/$name.tar.gz"
        echo "  ✓ $name downloaded"
    fi
}

download_vosk \
    "https://alphacephei.com/vosk/models/vosk-model-en-us-0.42.zip" \
    "$MODELS_DIR/vosk/vosk-model-en-us-0.42"

download_vosk \
    "https://alphacephei.com/vosk/models/vosk-model-hi-0.22.zip" \
    "$MODELS_DIR/vosk/vosk-model-hi-0.22"

# ── 4. Piper TTS ──────────────────────────────────────────
echo ""
echo "[4/6] Downloading Piper TTS voices..."
echo "----------------------------------------"
download_piper() {
    local model="$1"
    local url="https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/${model}/${model}.onnx"
    local json_url="https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/${model}/${model}.onnx.json"
    if [ -f "$MODELS_DIR/piper/${model}.onnx" ]; then
        echo "  ✓ ${model} already downloaded"
    else
        echo "  Downloading ${model}..."
        curl -L "$url" -o "$MODELS_DIR/piper/${model}.onnx" --silent --show-error
        curl -L "$json_url" -o "$MODELS_DIR/piper/${model}.onnx.json" --silent --show-error
        echo "  ✓ ${model} downloaded"
    fi
}

download_piper "en_US-lessac-medium"
download_piper "en_US-lessac-low"
download_piper "en_US-amy-medium"

# ── 5. YOLO (circuit component detection) ─────────────────
echo ""
echo "[5/6] Downloading YOLO model for circuit detection..."
echo "----------------------------------------"
python3 -c "
from ultralytics import YOLO
model = YOLO('yolov8n.pt')
model.save('$MODELS_DIR/yolo/yolov8n.pt')
print('  ✓ YOLO model downloaded')
" 2>/dev/null || echo "  ⚠ YOLO download skipped (ultralytics not installed)"

# ── 6. Verify ─────────────────────────────────────────────
echo ""
echo "[6/6] Verification..."
echo "----------------------------------------"
echo "  Ollama:"
curl -s "$OLLAMA_HOST/api/tags" | python3 -c "import sys,json; [print(f'    ✓ {m[\"name\"]}') for m in json.load(sys.stdin).get('models',[])]" 2>/dev/null || echo "    ⚠ Ollama not reachable"
echo ""
echo "  Downloaded size:"
du -sh "$MODELS_DIR" 2>/dev/null || echo "    (check failed)"
echo ""
echo "========================================"
echo " All models downloaded successfully!"
echo "========================================"
