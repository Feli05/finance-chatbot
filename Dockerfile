FROM node:18-alpine

# Set working directory
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

EXPOSE ${PORT}

ENV NODE_ENV=production

# Start the application
CMD ["npm", "start"] 