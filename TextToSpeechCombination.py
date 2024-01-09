# Section 1: Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

from pydub import AudioSegment, silence
import os

# Define the path for temporary storage of audio files
TEMP_FOLDER = '/content/drive/MyDrive/x/www'
OUTPUT_FOLDER = '/content/drive/MyDrive/x/www'
TARGET_DURATION_MS = 3000  # Set your desired duration in milliseconds

# Make sure temp folder and output folder exist
for folder in [TEMP_FOLDER, OUTPUT_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Function to clean up audio
def preprocess_audio(audio_path):
    try:
        # Load audio file
        audio = AudioSegment.from_file(audio_path)

        # Find non-silent chunks
        non_silent_chunks = silence.detect_nonsilent(audio, min_silence_len=400, silence_thresh=-40)

        # Combine non-silent chunks
        combined_audio = AudioSegment.empty()
        for start, end in non_silent_chunks:
            combined_audio += audio[start:end]

        # Export cleaned audio
        combined_audio.export(audio_path, format="wav")

        return audio_path

    except Exception as e:
        print(e)
        return None

# Function to adjust audio duration
def adjust_audio_duration(audio_path, target_duration):
    # Load WAV file
    audio = AudioSegment.from_file(audio_path, format="wav")

    # Adjust duration
    if len(audio) > target_duration:
        # Trim if longer than target duration
        audio = audio[:target_duration]
    else:
        # Pad with silence if shorter than target duration
        silence_duration = target_duration - len(audio)
        silence = AudioSegment.silent(duration=silence_duration)
        audio = audio + silence

    # Export adjusted audio
    audio.export(audio_path, format="wav")

    return audio_path

# Function to process audio file
def process_audio(input_file_path, output_folder, target_duration):
    try:
        # Process audio
        clean_audio_path = preprocess_audio(input_file_path)

        # Adjust audio duration
        adjusted_audio_path = adjust_audio_duration(clean_audio_path, target_duration)

        # Move adjusted audio to the output folder
        adjusted_audio_name = os.path.basename(adjusted_audio_path)
        adjusted_audio_destination = os.path.join(output_folder, adjusted_audio_name)
        os.rename(adjusted_audio_path, adjusted_audio_destination)

        return adjusted_audio_destination

    except Exception as e:
        print(e)
        return None

# Process all audio files in the input folder
input_folder = '/content/drive/MyDrive/y'
for filename in os.listdir(input_folder):
    if filename.endswith('.wav'):
        input_file_path = os.path.join(input_folder, filename)
        output_file_path = process_audio(input_file_path, OUTPUT_FOLDER, TARGET_DURATION_MS)
        if output_file_path:
            print(f"Processed audio saved at: {output_file_path}")
        else:
            print(f"An error occurred while processing {filename}")
