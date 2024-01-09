import os
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

def create_combined_mp3_from_training_data(training_data_filename, combined_mp3_filename):
    # Initialize an empty AudioSegment for combining all the audio
    combined_audio = AudioSegment.silent(duration=1000)  # Start with 1 second of silence

    # Read the training data file
    with open(training_data_filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Process each pair of English and Russian sentences
    for i in range(0, len(lines), 2):
        english_text = lines[i].strip()
        russian_text = lines[i+1].strip()

        # Create gTTS objects for each sentence
        tts_english = gTTS(text=english_text, lang='en', tld='com', slow=False)
        tts_russian = gTTS(text=russian_text, lang='ru', tld='com', slow=False)

        # Save each sentence to a temporary file
        tts_english.save('temp_english.mp3')
        tts_russian.save('temp_russian.mp3')

        # Load the temporary files as AudioSegment objects
        english_audio = AudioSegment.from_mp3('temp_english.mp3')
        russian_audio = AudioSegment.from_mp3('temp_russian.mp3')

        # Add each sentence to the combined audio, with a pause in between
        combined_audio += english_audio + AudioSegment.silent(duration=1000) + russian_audio + AudioSegment.silent(duration=2000)

        # Remove the temporary files
        os.remove('temp_english.mp3')
        os.remove('temp_russian.mp3')

    # Save the combined audio to the specified MP3 file
    combined_audio.export(combined_mp3_filename, format="mp3")
    print(f"Saved combined voiced text to {combined_mp3_filename}")

# Specify the training data file and the output MP3 file
training_data_filename = 'training_data.txt'
combined_mp3_filename = 'combined_voiced.mp3'

# Call the function to create the combined MP3 from the training data
create_combined_mp3_from_training_data(training_data_filename, combined_mp3_filename)
