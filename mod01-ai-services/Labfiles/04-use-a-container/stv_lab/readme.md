# Language Detection Web Application

This is a simple Flask web application that detects the language of the input text using Azure AI Text Analytics.

## Prerequisites

- Docker
- Docker Compose (if using multiple containers)

## Setup

1. Clone this repository:
    ```sh
    git clone https://github.com/yourusername/language-detection-app.git
    cd language-detection-app
    ```

2. Create a `.env` file and add your Azure AI service endpoint and key:
    ```
    AI_SERVICE_ENDPOINT=your_ai_service_endpoint
    AI_SERVICE_KEY=your_ai_service_key
    ```

3. Build and run the Docker container:
    ```sh
    docker-compose up --build
    ```

4. Open your web browser and go to `http://localhost:5000`.

## Files

- `app.py`: The main Flask application.
- `templates/index.html`: The HTML template for the web interface.
- `Dockerfile`: The Dockerfile to build the Flask application.
- `requirements.txt`: The list of Python dependencies.
- `docker-compose.yml`: The Docker Compose file (optional).

## Usage

Enter some text in the provided text area and click "Detect Language". The detected language will be displayed on the web page.
