# Vanilla Voices made using https://online-voice-recorder.com/

import os
import concurrent.futures

from pydub import AudioSegment


INPUT = "assets/vanilla"
OUTPUT = "assets/pitched"

SPEED = 2.0


def process_file(file: str):
    audio = AudioSegment.from_mp3(os.path.join(INPUT, file))
    pitched_audio = audio._spawn(audio.raw_data, overrides={'frame_rate': int(audio.frame_rate * SPEED)})
    pitched_audio = pitched_audio._spawn(pitched_audio.raw_data, overrides={'sample_width': audio.sample_width, 'frame_rate': pitched_audio.frame_rate, 'channels': audio.channels})
    pitched_audio.export(os.path.join(OUTPUT, file), format='mp3')
    return file


if not os.path.exists(OUTPUT):
    os.makedirs(OUTPUT)

files = [file for file in os.listdir(INPUT) if file.endswith(".mp3")]

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = {executor.submit(process_file, file): file for file in files}
    for future in concurrent.futures.as_completed(futures):
        file = futures[future]
        try:
            future.result()
        except Exception as exc:
            print(f"Error processing file {file}: {exc}")
        else:
            print(f"Processed file {file}")
