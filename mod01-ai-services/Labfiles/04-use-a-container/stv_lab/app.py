from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import platform
import psutil
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

app = Flask(__name__)

def GetLanguage(text, ai_endpoint, ai_key):
    # Create client using endpoint and key
    credential = AzureKeyCredential(ai_key)
    client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)

    # Call the service to get the detected language
    detectedLanguage = client.detect_language(documents=[text])[0]
    return detectedLanguage.primary_language.name

@app.route('/', methods=['GET', 'POST'])
def index():
    language = None
    if request.method == 'POST':
        userText = request.form['text']
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')
        language = GetLanguage(userText, ai_endpoint, ai_key)
    
    # Gather system information
    os_info = platform.system() + " " + platform.release()
    container_name = os.getenv('HOSTNAME', 'Unknown')  # Get container name from environment variable or set to 'Unknown'
    cpu_count = psutil.cpu_count()
    memory_info = psutil.virtual_memory().total / (1024 ** 3)  # Convert from bytes to GB

    return render_template('index.html', language=language, os_info=os_info, container_name=container_name, cpu_count=cpu_count, memory_info=memory_info)

if __name__ == "__main__":
    load_dotenv()
    app.run(host='0.0.0.0', port=5000, debug=True)
