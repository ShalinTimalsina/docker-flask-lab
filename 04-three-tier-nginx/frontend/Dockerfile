# ==========================================
# Stage 1: Build stage (compile React with Node.js)
# ==========================================
FROM node:22-alpine AS build

# Set working directory inside build container
WORKDIR /app

# Copy package descriptors first to cache npm dependencies
COPY package.json .

# Install frontend dependencies
RUN npm install

# Copy application source files
COPY index.html vite.config.js ./
COPY src/ ./src/

# Build static production assets into dist/
RUN npm run build

# ==========================================
# Stage 2: Production runtime stage (Nginx web server)
# ==========================================
FROM nginx:alpine

# Copy static-only Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy compiled static assets from build stage to Nginx web root
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80 for web traffic
EXPOSE 80

# Run Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
