import json
from pytube import YouTube
import os
import whisper

whisper_model = whisper.load_model("small")


class Transcriber:
    def __init__(self, video_id, video_title, video_description):
        self.video_id = video_id
        self.video_title = video_title
        self.video_description = video_description
        self.audio_file = ''
        self.destination = './data/AndrewHuberMan/audios/'

    def download_mp3(self):
        video_id = self.video_id
        title = self.video_title
        file_path = os.path.join(self.destination, f"{title}.mp3")
        if os.path.exists(file_path):
            print(f"{title}.mp3 already exists. Skipping download.")
            return
        try:
            yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
            video = yt.streams.filter(only_audio=True).first()
            print(f"Downloading audio for {title}...")
            out_file = video.download(output_path=self.destination)
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            self.audio_file = new_file
            os.rename(out_file, new_file)
            print(f"{title}.mp3 has been successfully downloaded.")
        except Exception as e:
            print(f"Error downloading audio for {title}: {e}")

    def transcribe_audio(self):
        result = whisper_model.transcribe(self.audio_file)
        self.transcription = result["text"]
        print(f"{self.video_title} has been successfully transcribed.")

    def save_transcription(self):
        transcriptions_path = "./data/AndrewHuberMan/transcriptions/"
        if not os.path.exists(transcriptions_path):
            os.makedirs(transcriptions_path)
        with open(f"{transcriptions_path}{self.video_title}.txt", "w") as f:
            f.write(f"Video Title: {self.video_title}\n")
            f.write(f"Video Description: {self.video_description}\n")
            f.write("Transcription:\n")
            f.write(self.transcription)
        print(f"{self.video_title} transcription has been successfully saved.")


# Load videos list from file
with open("./data/AndrewHuberMan/videos.txt", "r") as f:
    videos_list = json.load(f)

# Process each video
for video in videos_list:
    transcriber = Transcriber(
        video["id"], video["title"], video["description"])
    transcriber.download_mp3()
    transcriber.transcribe_audio()
    transcriber.save_transcription()
