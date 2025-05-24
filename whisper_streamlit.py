import os
import time
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

import logging

logger = logging.getLogger("whisperStreamlit")
logging.getLogger("speechbrain").setLevel(logging.WARNING)

import streamlit as st
import torch
import whisper
from pyannote.audio import Pipeline  # noqa: E402
from pyannote.audio.pipelines.utils.hook import ProgressHook
from pydub import AudioSegment

from src.merge_whisper_pyannot import diarize_text, save_merge, save_undiarized

torch.classes.__path__ = [
    os.path.join(torch.__path__[0], torch.classes.__file__)
]  # https://discuss.streamlit.io/t/error-in-torch-with-streamlit/90908/4

WHISPER_TOKEN = "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"


def transcribe_audio(audio_path, model_size, language):
    """Transcribes the given audio file using the specified Whisper model and language.

    Args:
        audio_path (str): Path to the audio file.
        model_size (str): Whisper model size to use.
        language (str): Language for transcription.

    Returns:
        Dict: Full whisper output.
    """
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path, language=language, verbose=False)
    return result


def main():
    """Main function to run the Streamlit application for Whisper speech-to-text transcription."""
    st.title("Whisper Speech-to-Text")

    # File uploader
    uploaded_file = st.file_uploader(
        "Upload an audio file", type=["mp3", "wav", "m4a", "ogg"]
    )

    col1, col2 = st.columns(2)

    with col1:
        # Whisper model selection
        model_size = st.selectbox(
            "Choose Whisper model size",
            ["tiny", "base", "small", "medium", "turbo", "large"],
            index=4,
        )

        # Diarization options
        help_message = "Turn speaker segmentation on/off to save time"
        do_diarize = st.toggle(
            "Segment speakers",
            value=True,
            key=None,
            help=help_message,
            on_change=None,
            label_visibility="visible",
        )

    with col2:
        # Language selection
        language = st.selectbox(
            "Select language",
            [
                "english",
                "russian",
                "french",
                "spanish",
                "german",
                "japanese",
                "chinese",
            ],
            index=1,
        )
        num_speakers = st.number_input(
            "Select number of speakers",
            step=1,
            value=2,
            min_value=0,
            disabled=not do_diarize,
        )

    if st.button("Start Transcription"):
        if uploaded_file is not None:
            output_folder = os.path.join(os.getcwd(), "out")
            os.makedirs(output_folder, exist_ok=True)  # Ensure output folder exists

            file_extension = uploaded_file.name.split(".")[-1]
            file_name = os.path.splitext(uploaded_file.name)[0] + ".txt"
            output_path = os.path.join(output_folder, file_name)

            # TODO improve this, bad format handling
            if file_extension == "m4a":
                file_extension = "wav"
                temp_audio_path = os.path.join("temp_audio." + file_extension)
                audio = AudioSegment.from_file(uploaded_file)
                audio.export(temp_audio_path, format="wav")
            else:
                temp_audio_path = os.path.join("temp_audio." + file_extension)
                with open(temp_audio_path, "wb") as f:
                    f.write(uploaded_file.read())

            start_time = time.time()
            st.text("Transcribing...")
            whisper_output = transcribe_audio(temp_audio_path, model_size, language)
            save_undiarized(whisper_output, output_path[:-4] + "_whisper.txt")

            # TODO: diarization is not very well done
            if do_diarize:
                pass
                # Grabbing the pyannot pipeline
                diarization_pipe = Pipeline.from_pretrained(
                    "pyannote/speaker-diarization-3.1",
                    use_auth_token=WHISPER_TOKEN,
                )

                st.text("Segmenting...")
                with ProgressHook() as hook:
                    diarization_result = diarization_pipe(
                        temp_audio_path, hook=hook, num_speakers=num_speakers
                    )

                st.text("Merging and saving output...")
                if num_speakers == 0:
                    num_speakers = None
                final_result = diarize_text(whisper_output, diarization_result)
                save_merge(final_result, output_path)
            else:
                save_undiarized(whisper_output, output_path, do_format=True)

            logger.info(
                f"Finished file. Total processing time: {time.time() - start_time} seconds"
            )

            st.success("Transcription completed!")
            with open(output_path, "rb") as file:
                st.download_button(
                    "Download Transcription",
                    data=file,
                    file_name=file_name,
                    mime="text/plain",
                )
            os.remove(temp_audio_path)  # Cleanup temporary file
            uploaded_file = []
        else:
            st.error("Please upload a file")


if __name__ == "__main__":
    main()
