from moviepy.editor import TextClip, CompositeVideoClip

# Create a text clip (by default the text will be white on black)
text_clip = TextClip("Hello world", fontsize=70, color='white')

# Set the duration of the text clip
text_clip = text_clip.set_duration(10)

# Create a composite video clip (here, on a black background)
video = CompositeVideoClip([text_clip], size=text_clip.size)

# Set the final duration of the video
video = video.set_duration(10)

# Write the video to a file
video.write_videofile("hello_world.mp4", fps=24)