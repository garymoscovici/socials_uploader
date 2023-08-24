from flask import Flask, render_template, request
from main import run_app
import pathlib
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/page', methods=("GET", "POST"))
def my_link():
  data = request.form
  input_file = str(pathlib.Path().resolve() / "input_files" / data.get("videofile"))
  caption = data.get("caption")
  start_time = 60 * int(data.get("start_minutes", 0)) + int(data.get("start_seconds", 0))
  end_time = 60 * int(data.get("end_minutes", 0)) + int(data.get("end_seconds", 0))
  thumbnail_path = str(pathlib.Path().resolve() / "input_files" / data.get("thumbnail"))
  instagram = data.get("instagram")
  tiktok = data.get("tiktok")
  run_app(input_file, thumbnail_path, caption, start_time, end_time, instagram, tiktok)
  return data
    # from selenium import webdriver
    # from selenium .webdriver.common.by import By
    # from selenium.webdriver.support.ui import WebDriverWait
    # from selenium.webdriver.support import expected_conditions as EC
    # from selenium.webdriver.common.keys import Keys
    # import time
    # driver = webdriver.Chrome()
    # driver.get("https://instagram.com")

if __name__ == '__main__':
  app.run(debug=True)