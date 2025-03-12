import streamlit as st 
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from io import BytesIO

def convert_mp4_to_mp3(uploaded_file):
    temp_video_path = "temp_video.mp4"

    # Save the uploaded file to a temporary path
    with open(temp_video_path, "wb") as f:
        f.write(uploaded_file.read())

    # Process the video file
    video_clip = VideoFileClip(temp_video_path)
    audio_clip = video_clip.audio

    # Store audio in memory
    mp3_buffer = BytesIO()
    audio_clip.write_audiofile("temp_audio.mp3", codec="mp3")
    audio_clip.close()
    video_clip.close()

    # Read the MP3 file into BytesIO
    with open("temp_audio.mp3", "rb") as f:
        mp3_buffer.write(f.read())

    mp3_buffer.seek(0)

    # Cleanup temporary files
    os.remove(temp_video_path)
    os.remove("temp_audio.mp3")

    return mp3_buffer

def generate_download_button(mp3_buffer):
    """Ensure the MP3 file is downloadable, including on iOS."""
    st.download_button(
        label="Download MP3",
        data=mp3_buffer.getvalue(),  # Ensure proper byte format
        file_name="converted_audio.mp3",
        mime="audio/mpeg"
    )

def main():
    st.title("MP4 to MP3 Converter")
    st.write("Upload an MP4 video file to extract its audio as an MP3 file.")
    
    uploaded_file = st.file_uploader("Choose an MP4 file", type=["mp4"])
    
    if uploaded_file is not None:
        st.video(uploaded_file)
        
        if st.button("Convert to MP3"):
            with st.spinner("Extracting audio..."):
                mp3_buffer = convert_mp4_to_mp3(uploaded_file)
                
                st.success("Conversion Successful!")
                st.audio(mp3_buffer, format="audio/mpeg")
                
                st.write("Download your MP3 file below:")
                generate_download_button(mp3_buffer)

                # Provide a shareable suggestion
                st.write("To share this MP3, upload it to Google Drive, Dropbox, or another file-sharing service and share the link.")
                
if __name__ == "__main__":
    main()
