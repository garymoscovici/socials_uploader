import click
from moviepy.editor import *
from moviepy.video.fx.all import crop

@click.command()
@click.argument('input')
@click.argument('start_time')
@click.argument('end_time')
@click.option('-v', 'second_input', default='random')
def uploadvid(input, start_time, end_time, second_input):

    clip1 = VideoFileClip(input)
    
    if second_input=='random':
        clip2 = VideoFileClip('soap_cutting.mp4')
    else:
        clip2 = VideoFileClip(second_input)

    clip1 = clip1.subclip(start_time, end_time)
    print(int(end_time)-int(start_time))
    clip2 = clip2.subclip(100, 100+ (int(end_time)-int(start_time)))
    (w,h) = clip2.size

    cropped_clip2 = crop(clip2,width=w/2, x_center=(h/2) + (w/4))
    (w,h) = cropped_clip2.size
    clip1 = clip1.resize(width=w)
    final = clips_array([[clip1], [cropped_clip2]])
    # final.ipython_display(width=480)
    final.write_videofile("combined.mp4")

def upload_to_insta():
    from selenium import webdriver
    driver = webdriver.Chrome('./chromedriver')
    
# if __name__ == '__main__':
#     uploadvid()
