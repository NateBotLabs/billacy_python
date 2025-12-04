# Use official Python image as build environment
FROM python:3.15-alpine

# Set working directory
WORKDIR /app

# Copy your project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt pyinstaller

# Build the exe
RUN pyinstaller --onefile --noconsole main.py
