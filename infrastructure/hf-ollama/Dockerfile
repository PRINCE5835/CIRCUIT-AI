FROM ollama/ollama:latest

ENV OLLAMA_HOST=0.0.0.0:7860

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 7860

ENTRYPOINT ["/entrypoint.sh"]
