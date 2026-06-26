#!/bin/bash
set -e

ollama serve &

sleep 5

ollama pull qwen2.5:1.5b

wait
