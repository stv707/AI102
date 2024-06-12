from dotenv import load_dotenv
import os
import azure.cognitiveservices.speech as speech_sdk
import keyboard
import time

def main():
    try:
        global speech_config
        global translation_config

        # Get Configuration Settings
        load_dotenv()
        ai_key = os.getenv('SPEECH_KEY')
        ai_region = os.getenv('SPEECH_REGION')

        # Configure translation
        translation_config = speech_sdk.translation.SpeechTranslationConfig(ai_key, ai_region)
        translation_config.speech_recognition_language = 'en-US'
        translation_config.add_target_language('fr')
        translation_config.add_target_language('es')
        translation_config.add_target_language('ms')
        print('Ready to translate from', translation_config.speech_recognition_language)

        # Configure speech
        speech_config = speech_sdk.SpeechConfig(ai_key, ai_region)

        # Get user input
        targetLanguage = ''
        while targetLanguage != 'quit':
            targetLanguage = input('\nEnter a target language\n fr = French\n es = Spanish\n ms = Malay\n Enter anything else to stop\n').lower()
            if targetLanguage in translation_config.target_languages:
                Translate(targetLanguage)
            else:
                targetLanguage = 'quit'

    except Exception as ex:
        print(ex)

def Translate(targetLanguage):
    translation = ''

    # Wait for the user to press a key
    print("Press 'space' to start speaking...")
    keyboard.wait('space')  # Wait until the user presses the 'space' key

    # Translate speech
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config=audio_config)

    def recognized(evt):
        nonlocal translation
        if evt.result.reason == speech_sdk.ResultReason.TranslatedSpeech:
            print('Recognized: "{}"'.format(evt.result.text))
            translation = evt.result.translations[targetLanguage]
            print('Translation: {}'.format(translation))
        elif evt.result.reason == speech_sdk.ResultReason.NoMatch:
            print("No speech could be recognized")

    def session_started(evt):
        print("Session started")

    def session_stopped(evt):
        print("Session stopped")

    def canceled(evt):
        print(f"Canceled: {evt.reason}")
        if evt.reason == speech_sdk.CancellationReason.Error:
            print(f"Error details: {evt.error_details}")

    translator.recognized.connect(recognized)
    translator.session_started.connect(session_started)
    translator.session_stopped.connect(session_stopped)
    translator.canceled.connect(canceled)

    print("Speak now...")
    translator.start_continuous_recognition()
    time.sleep(5)  # Listen for 15 seconds / Change to make it faster
    translator.stop_continuous_recognition()

    # Synthesize translation
    if translation:
        voices = {
            "fr": "fr-FR-HenriNeural",
            "es": "es-ES-ElviraNeural",
            "ms": "ms-MY-YasminNeural"
        }
        speech_config.speech_synthesis_voice_name = voices.get(targetLanguage)
        speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)
        speak = speech_synthesizer.speak_text_async(translation).get()
        if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
            print(speak.reason)

if __name__ == "__main__":
    main()
