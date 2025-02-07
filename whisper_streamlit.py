import os

import streamlit as st
import whisper


def transcribe_audio(audio_path, model_size, language):
    """Transcribes the given audio file using the specified Whisper model and language.

    Args:
        audio_path (str): Path to the audio file.
        model_size (str): Whisper model size to use.
        language (str): Language for transcription.

    Returns:
        str: The transcribed text.
    """
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path, language=language, verbose=False)
    return result["text"]


def format_transcription(text):
    """Formats the transcribed text so that each sentence starts on a new line.

    Args:
        text (str): The transcribed text.

    Returns:
        str: Formatted text with sentences on separate lines.
    """
    sentences = text.replace(". ", "\n").replace("? ", "\n").replace("! ", "\n")
    return sentences


def main():
    """Main function to run the Streamlit application for Whisper speech-to-text transcription."""
    st.title("Whisper Speech-to-Text Transcription")

    # File uploader
    uploaded_file = st.file_uploader(
        "Upload an audio file", type=["mp3", "wav", "m4a", "ogg"]
    )

    # Output folder selection
    output_folder = st.text_input(
        "Select output folder", value=os.path.join(os.getcwd(), "out")
    )

    # Whisper model selection
    model_size = st.selectbox(
        "Choose Whisper model size",
        ["tiny", "base", "small", "medium", "turbo", "large"],
        index=4,
    )

    # Language selection
    language = st.selectbox(
        "Select language",
        ["english", "russian", "french", "spanish", "german", "japanese", "chinese"],
        index=1,
    )

    if st.button("Start Transcription"):
        if uploaded_file is not None and output_folder:
            os.makedirs(output_folder, exist_ok=True)  # Ensure output folder exists

            file_extension = uploaded_file.name.split(".")[-1]
            file_name = os.path.splitext(uploaded_file.name)[0] + ".txt"
            temp_audio_path = os.path.join("temp_audio." + file_extension)

            with open(temp_audio_path, "wb") as f:
                f.write(uploaded_file.read())

            st.text("Transcribing...")
            transcribed_text = transcribe_audio(temp_audio_path, model_size, language)
            formatted_text = format_transcription(transcribed_text)

            output_path = os.path.join(output_folder, file_name)
            with open(output_path, "w") as f:
                f.write(formatted_text)

            st.success("Transcription completed!")
            st.download_button(
                "Download Transcription", formatted_text, file_name=file_name
            )
            os.remove(temp_audio_path)  # Cleanup temporary file
        else:
            st.error("Please upload a file and select an output folder.")


if __name__ == "__main__":
    main()
