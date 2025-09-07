from os import path, environ, remove
from faster_whisper import WhisperModel
import torch
import ffmpegio
from tkinter import filedialog
from win11toast import notify
from time import sleep


def get_tempdir():
    for var in ("TMPDIR", "TEMP", "TMP"):
        attemptPath = environ.get(var)
        if attemptPath and path.isdir(attemptPath):
            return attemptPath

    return r"C:\\TEMP"


def extract_audio(input_path,output_path):
    notify("MP4 Transcriber","Beginning audio extraction...")
    
    try:
        ffmpegio.transcode(input_path, output_path, acodec='pcm_s16le', format='wav')
    except Exception as e:
        notify("MP4 Transcriber",f"Error during audio extraction: {e}",duration=3)
        remove(output_path)
        sleep(3)
        notify("MP4 Transcriber","Re-attempting audio extraction.",duration=1)
        sleep(1)
        try:
            ffmpegio.transcode(input_path, output_path, acodec='pcm_s16le', format='wav')
        except:
            notify("MP4 Transcriber",f"Error occured during audio extraction, terminating.",duration=2)
            remove(output_path)
            exit()

    notify("MP4 Transcriber","Finished audio extraction.")


class STTProcessor:
    def __init__(self, model_size="medium"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.compute_type = "float32" if self.device == "cuda" else "int8"
        try:
            self.model = WhisperModel(model_size, device=self.device, compute_type=self.compute_type)
        except Exception as e:
            notify("MP4 Transcriber",f"Error loading model: {e}")
            self.model = None

    def transcribe(self, audio_file_path, language="en", task="translate", beam_size=5):
        if not self.model:
            notify("MP4 Transcriber","Model is not loaded.")
            return None

        if not path.exists(audio_file_path):
            notify("MP4 Transcriber",f"Error: Audio file not found at {audio_file_path}")
            return None

        notify("MP4 Transcriber","Transcribing audio...")

        try:
            segments, info = self.model.transcribe(
                audio_file_path,
                language=language,
                task=task,
                beam_size=beam_size
            )
            transcribed_text = "".join(segment.text for segment in segments)
            notify("MP4 Transcriber","Transcription complete!")
            return transcribed_text
        except Exception as e:
            notify("MP4 Transcriber",f"Error during transcription: {e}",duration=4)
            sleep(4)
            notify("MP4 Transcriber","Re-attempting transcription.",duration=1)
            sleep(1)
            try:
                segments, info = self.model.transcribe(
                    audio_file_path,
                    language=language,
                    task=task,
                    beam_size=beam_size
                )
                transcribed_text = "".join(segment.text for segment in segments)
                notify("MP4 Transcriber","Transcription complete!")
            except:
                return None


    def transcribe_and_save(self, audio_path, output_txt_path, **kwargs):
        transcription = self.transcribe(audio_path, **kwargs)

        if transcription:
            with open(output_txt_path, "w", encoding="utf-8") as script:
                script.write(transcription)
            return
        else:
            notify("MP4 Transcriber",f"Error occured during transcription, terminating.",duration=2)
            exit()



if __name__ == '__main__':
    openPath = rf'{filedialog.askopenfilename(title="Choose a Mp4 file to transcribe",filetypes=[("MP4 files","*.mp4")])}'
    tmp = path.join(get_tempdir(),(path.basename(openPath)[:-4]+'.wav'))
    extract_audio(openPath,tmp)

    savePath = filedialog.asksaveasfilename(title="Choose a location to save the transcript",defaultextension=".txt",filetypes=[("Text files", "*.txt")])
    STTProcessor().transcribe_and_save(tmp,savePath)
    remove(tmp)

