# Use an official Node.js runtime as the base image
FROM node:20-alpine

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the the application code to the container
COPY ./frontend .

# Install bash
RUN apk add --no-cache bash

# Install pnpm globally
RUN npm install -g pnpm

# Install dependencies using pnpm
#RUN pnpm install --frozen-lockfile
RUN pnpm install

# Build the Vite app
#RUN pnpm run build
