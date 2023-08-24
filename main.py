"""
FILE STRUCTURE
TIKTOK.PY
  handles upload to tiktok
INSTAGRAM.PY
  handles upload to instagram
EDITOR.PY
  handles 
CONFIG.YML
  contents:
      name of uploading thing for logging
      key values for stitch videos and start times



Welcome message etc

Select input video and stitch video
inputs:
Video file
Select input (default randomish)
Write caption
Upload mode true/false (false = write logs to file)


Stitch video and output
  Create sensible output video name, (original plus date)

run tiktok upload
run instagram upload



"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from tiktok import post_to_tiktok
from instagram import post_to_instagram
from video_generation import generate_clip

def run_app(input_file, thumbnail_filepath, 
            caption, start_time, end_time, instagram, tiktok):
  filename = generate_clip(input_file, caption, start_time, end_time)

  test_mode = True
  chrome_options = Options()
  chrome_options.add_argument('--log-level=3')

  if tiktok:
    driver = webdriver.Chrome(chrome_options=chrome_options)
    post_to_tiktok(driver, test_mode, filename)
  if instagram:
    driver = webdriver.Chrome(chrome_options=chrome_options)
    post_to_instagram(driver, test_mode, filename, thumbnail_filepath)
