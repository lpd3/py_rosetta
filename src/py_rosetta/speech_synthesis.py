# Speech Synthesis

''' SPEECH SYNTHESIS

Render the text "This is an example of speech synthesis." as speech.'''

# The external pyttsx3 library searches for a text to speech engine
# in the local operating system and employs it to generate speech
# from text. However, this relies on espeak for Linux, which is not
# available here.

# The external gTTS library may be a useable solution

# Ultimately, I could not get this to work here. I cannot figure out
# how to get access to the Android sound engine.

import pyttsx3
from gtts import gTTS
import os


def main_with_pyttsx3():
    engine = pyttsx3.init()
    engine.say("This is an example of speech synthesis.")
    engine.runAndWait()


def main_with_gtts():
    the_text = 'This is an example of speech synthesis.'
    language = 'en'
    obj = gTTS(text=the_text, lang=language, slow=False)
    obj.save('text_to_speech.mp3')
    os.system('play text_to_speech.mp3')

    
if __name__ == '__main__':
    main_with_gtts()
