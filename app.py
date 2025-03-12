import streamlit as st 
import os
import base64
from moviepy.video.io.VideoFileClip import VideoFileClip

from io import BytesIO

def convert_mp4_to_mp3(video_file):
    video_clip = VideoFileClip(video_file)
    audio_clip = video_clip.audio
    mp3_path = "output.mp3"
    audio_clip.write_audiofile(mp3_path, codec='mp3')
    audio_clip.close()
    video_clip.close()
    return mp3_path

def generate_shareable_link(mp3_path):
    with open(mp3_path, "rb") as f:
        mp3_bytes = f.read()
    b64 = base64.b64encode(mp3_bytes).decode()
    href = f'<a href="data:audio/mp3;base64,{b64}" download="output.mp3">Click here to download and share</a>'
    return href

def main():
    st.set_page_config(page_title="Audio Extract")
    st.title("MP4 to MP3 Converter")
    st.write("Upload an MP4 video file to extract its audio as an MP3 file.")
    
    uploaded_file = st.file_uploader("Choose an MP4 file", type=["mp4"])
    
    if uploaded_file is not None:
        st.video(uploaded_file)
        
        temp_video_path = "temp_video.mp4"
        with open(temp_video_path, "wb") as f:
            f.write(uploaded_file.read())
        
        if st.button("Convert to MP3"):
            with st.spinner("Extracting audio..."):
                mp3_path = convert_mp4_to_mp3(temp_video_path)
                
                with open(mp3_path, "rb") as f:
                    mp3_bytes = f.read()
                
                st.success("Conversion Successful!")
                st.audio(mp3_bytes, format="audio/mp3")
                
               
                st.write("Share the MP3 file using the link below:")
                st.markdown(generate_shareable_link(mp3_path), unsafe_allow_html=True)
                
                os.remove(mp3_path)
                os.remove(temp_video_path)
                
if __name__ == "__main__":
    main()
