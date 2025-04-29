# Use Node.js LTS version
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Install dependencies first to leverage Docker cache
COPY package*.json ./
RUN npm install

# Copy the rest of the application
COPY . .

# Build the application
RUN npm run build

# Expose the port from environment variable
EXPOSE ${PORT}

# Set environment variables
ENV NODE_ENV=production

# Start the application
CMD ["npm", "start"] 