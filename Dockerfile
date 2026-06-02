# Use the official Python slim image
FROM python:3.12-slim

# Install UV (Astral's fast Python package installer and resolver)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set up non-root user for security
RUN useradd -m -u 1000 appuser

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Copy dependency configuration
COPY pyproject.toml README.md ./

# Install dependencies into the system python using UV
RUN uv pip install --system .

# Copy the rest of the application code
COPY --chown=appuser:appuser . .

# Create necessary directories and set permissions
RUN mkdir -p uploads outputs && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose Streamlit port
EXPOSE 8501

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Start Streamlit
ENTRYPOINT ["streamlit", "run", "app.py"]