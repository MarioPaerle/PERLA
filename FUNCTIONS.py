import streamlit as st
from io import BytesIO

def midi_to_bytes(midi_obj):
    midi_bytes_io = BytesIO()
    midi_obj.write(midi_bytes_io)
    midi_bytes_io.seek(0)  # Reset pointer to start of buffer
    return midi_bytes_io

def get_midi_bytes_from_roll(roll):
    midi = roll.midi_human()
    st.download_button("Download Midi file",
                       data=midi_to_bytes(midi),
                       file_name="generated_music.mid",
                       mime="audio/midi"
                       )
    return 0