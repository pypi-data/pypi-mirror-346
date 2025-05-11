import argparse
import librosa
import numpy as np
import os
from mlx_lm_omni import load, generate
import librosa
from io import BytesIO
from urllib.request import urlopen
from recorder import AudioRecorder

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, help='Path to the model')
parser.add_argument('--text-model-id', type=str, help='Override the text model id for ultravox model')
parser.add_argument('--single', type=str, help='Path to the input file, we will transcribe the input file')
parser.add_argument('--folder', type=str, help='Path to the input folder, we will transcribe all files in the folder')
parser.add_argument('--repl', type=str, help='Manual input mode, we will transcribe the input file in repl mode. Input as recording folder path')
parser.add_argument('--language', type=str, help='Language of the audio file', default="Vietnamese")

args = parser.parse_args()

if args.model is None:
    args.model = "Qwen/Qwen2.5-Omni-3B"

model, tokenizer = load(args.model, model_config={"text_model_id": args.text_model_id})

def inference(audio: np.ndarray):
    messages = [
        {"role": "system", "content": """You are a speech recognition model."""},
        {"role": "user", "content": f"Transcribe the {args.language} audio into text without including any punctuation marks.", "audio": audio},
    ]
    prompt = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True
    )
    text = generate(model, tokenizer, prompt=prompt, max_tokens=1000, verbose=True)
    print(text)
    
if args.single:
    # play audio
    if args.single.startswith("http"):
        audio = BytesIO(urlopen(args.single).read())
    else:
        audio = args.single
    audio, sr = librosa.load(audio, sr=16000)
    print(f"Transcribing audio from {args.single}")
    # play_audio(audio, sample_rate=sr)
    inference(audio)
    print("Done\n")
elif args.folder:
    for file in os.listdir(args.folder):
        print(f"Transcribing audio from {file}")
        audio, sr = librosa.load(os.path.join(args.folder, file), sr=16000)
        # play_audio(audio, sample_rate=sr)
        inference(audio)
        print("Done\n")
elif args.repl:
    while True:
        file_path = input("Enter the path to the audio file: ")
        full_path = os.path.join(args.repl, file_path)
        try:
            audio, sr = librosa.load(full_path, sr=16000)
            print(f"Transcribing audio from {full_path}")
            # play_audio(audio, sample_rate=sr)
            inference(audio)
        except Exception as e:
            print(f"Error loading audio file: {e}")
else:
    recorder = AudioRecorder()
    print("Press and hold SPACE to record audio. Release to stop recording.")
    try:
        while True:
            audio, file_path = recorder.get_last_recording()
            if audio is not None:
                inference(audio)
                
    except KeyboardInterrupt:
        print("\nExiting...") 
        
