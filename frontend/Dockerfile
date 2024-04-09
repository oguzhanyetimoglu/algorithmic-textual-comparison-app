FROM node:lts-slim

# Create a non-sudo user
RUN useradd -m appuser \
    && mkdir -p /app \
    && chown -R appuser:appuser /app
USER appuser

# Set the working directory
WORKDIR /app

# Copy the application code
COPY --chown=appuser:appuser . .

RUN npm install

# Expose the port
EXPOSE 3000

RUN npm run build
# CMD node .output/server/index.mjs
# CMD npm run dev
