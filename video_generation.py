from __future__ import unicode_literals

import os
import pathlib

import pandas as pd
import whisper
from moviepy.editor import (CompositeVideoClip, ImageClip, TextClip,
                            VideoFileClip)
from moviepy.video.fx.margin import margin
from moviepy.video.tools.subtitles import SubtitlesClip


def crop_video(input_file, start_time, end_time):
    video = VideoFileClip(input_file)
    video = video.subclip(start_time,end_time)
    video = video.resize(width=1080)

    black_image = (ImageClip("./input_files/background.jpeg"))
    video = CompositeVideoClip([black_image, video.set_position("center")])
    duration =  end_time - start_time
    video.duration = duration
    
    return video, duration

def add_caption(video, caption):
    height = 540
    width = 1000
    top_margin = 200
    side_margin = 50
    txt_clip = TextClip(caption, color="white", method="caption", size = (width-side_margin, height-top_margin)) 
    txt_clip = margin(txt_clip, top=top_margin, left=side_margin, right=side_margin, bottom=1920-(height + top_margin), opacity=0)
        
    txt_clip = txt_clip.set_position("top")
    video = CompositeVideoClip([video, txt_clip]) 
    
    return video

def add_subtitles(video, caption: str, duration):
    caption = caption.replace(" ", "_")
    # Keep only alphanumeric characters
    caption = "".join(filter(str.isalnum, caption))
    # Use local clip if not downloading from youtube
    audio = video.audio
    audio.fps = 44100
    if not os.path.exists("tmp/"):
        os.mkdir(f"tmp/")
    audio.write_audiofile(f'tmp/{caption}.mp3', bitrate="50k")
    # Instantiate whisper model using model_type variable
    model = whisper.load_model('medium.en')
    
    # Get text from speech for subtitles from audio file
    result = model.transcribe(f'tmp/{caption}.mp3', task = 'translate')
    
    # create Subtitle dataframe, and save it
    dict1 = {'start':[], 'end':[], 'text':[]}
    for i in result['segments']:
        dict1['start'].append(int(i['start']))
        dict1['end'].append(int(i['end']))
        dict1['text'].append(i['text'])
    df = pd.DataFrame.from_dict(dict1)
    df.to_csv(f'tmp/{caption}.csv')

    height = 1920
    width = 1080

    # Instantiate MoviePy subtitle generator with TextClip, subtitles, and SubtitlesClip
    generator = lambda txt: TextClip(txt, font='P052-Bold', fontsize=width/20, stroke_width=.7, color='white', stroke_color = 'black', size = (width, height*.25), method='caption')
    # generator = lambda txt: TextClip(txt, color='white', fontsize=20, font='Georgia-Regular',stroke_width=3, method='caption', align='south', size=video.size)
    subs = tuple(zip(tuple(zip(df['start'].values, df['end'].values)), df['text'].values))
    subtitles = SubtitlesClip(subs, generator)
    subtitles = margin(subtitles, bottom=200)

    final = CompositeVideoClip([video, subtitles.set_pos(('center','bottom'))])
    final.duration = duration
    if not os.path.exists("clips/"):
        os.mkdir(f"clips/")
    output_filename = f'{str(pathlib.Path(__file__).parent.resolve())}\\output_files\\{caption}.mp4'
    final.write_videofile(output_filename, fps=video.fps, remove_temp=True, codec="libx264", audio_codec="aac")
    
    return output_filename

def generate_clip(input_file, caption, start_time, end_time):

    video, duration = crop_video(input_file, start_time, end_time)
    video = add_caption(video, caption)
    filename = add_subtitles(video, caption, duration)
    
    return filename