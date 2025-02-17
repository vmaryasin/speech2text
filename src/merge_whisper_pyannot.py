# Credits to https://github.com/yinruiqing/pyannote-whisper
from pyannote.core import Segment

PUNC_SENT_END = [".", "?", "!"]


def get_text_with_timestamp(transcribe_res):
    timestamp_texts = []
    for item in transcribe_res["segments"]:
        start = item["start"]
        end = item["end"]
        text = item["text"]
        timestamp_texts.append((Segment(start, end), text))
    return timestamp_texts


def add_speaker_info_to_text(timestamp_texts, ann):
    spk_text = []
    for seg, text in timestamp_texts:
        spk = ann.crop(seg).argmax()
        spk_text.append((seg, spk, text))
    return spk_text


def merge_cache(text_cache):
    sentence = "".join([item[-1] for item in text_cache])
    spk = text_cache[0][1]
    start = text_cache[0][0].start
    end = text_cache[-1][0].end
    return Segment(start, end), spk, sentence


def merge_sentence(spk_text):
    merged_spk_text = []
    pre_spk = None
    text_cache = []
    for seg, spk, text in spk_text:
        if spk != pre_spk and pre_spk is not None and len(text_cache) > 0:
            merged_spk_text.append(merge_cache(text_cache))
            text_cache = [(seg, spk, text)]
            pre_spk = spk

        elif text and len(text) > 0 and text[-1] in PUNC_SENT_END:
            text_cache.append((seg, spk, text))
            merged_spk_text.append(merge_cache(text_cache))
            text_cache = []
            pre_spk = spk
        else:
            text_cache.append((seg, spk, text))
            pre_spk = spk
    if len(text_cache) > 0:
        merged_spk_text.append(merge_cache(text_cache))
    return merged_spk_text


def diarize_text(transcribe_res, diarization_result):
    timestamp_texts = get_text_with_timestamp(transcribe_res)
    spk_text = add_speaker_info_to_text(timestamp_texts, diarization_result)
    res_processed = merge_sentence(spk_text)
    return res_processed


def save_merge(final_result, output_filepath, display=False):
    """Save output to file"""
    with open(output_filepath, "w", encoding="utf-8") as f:
        prev_speaker = "SPEAKER_00"
        for _, spk, sent in final_result:
            # Add a blank line when the speaker changes
            if spk != prev_speaker:
                f.write("\n")
                prev_speaker = spk
            line = f"{spk} {sent}"
            f.write(line + "\n")
            if display:
                print(line)


def format_transcription(text):
    """Formats the transcribed text so that each sentence starts on a new line.

    Args:
        text (str): The transcribed text.

    Returns:
        str: Formatted text with sentences on separate lines.
    """
    sentences = text.replace(". ", "\n").replace("? ", "\n").replace("! ", "\n")
    return sentences


def save_undiarized(whisper_output, output_filepath, do_format=True):
    formatted_output = format_transcription(whisper_output["text"])
