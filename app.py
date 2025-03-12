import streamlit as st 
import os
import base64
from moviepy.video.io.VideoFileClip import VideoFileClip
from io import BytesIO

def convert_mp4_to_mp3(video_file):
    video_clip = VideoFileClip(video_file)
    audio_clip = video_clip.audio
    mp3_buffer = BytesIO()
    audio_clip.write_audiofile(mp3_buffer, codec='mp3')
    audio_clip.close()
    video_clip.close()
    mp3_buffer.seek(0)
    return mp3_buffer

def generate_shareable_link(mp3_buffer):
    b64 = base64.b64encode(mp3_buffer.getvalue()).decode()
    href = f'<a href="data:audio/mp3;base64,{b64}" download="output.mp3">Click here to download and share</a>'
    return href

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
                st.audio(mp3_buffer, format="audio/mp3")
                
                st.download_button(
                    label="Download MP3",
                    data=mp3_buffer,
                    file_name="output.mp3",
                    mime="audio/mp3"
                )
                
                st.write("Share the MP3 file using the link below:")
                st.markdown(generate_shareable_link(mp3_buffer), unsafe_allow_html=True)
                
if __name__ == "__main__":
    main()
