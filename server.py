from flask import Flask
from pathlib import Path
from flask import send_file, render_template_string, make_response, request
import random

PICTURE_DIR = '.'  # 设定图片目录

app = Flask(__name__)


templ = '''
<html>
<head>
<meta name="viewport" content="width=device-width, minimum-scale=0.1">
<title>Home</title>

<style>
img{
	width: auto;
	height: auto;
	max-width: 100%;
	max-height: 100%;	
}
</style>
</head>
<body style="margin: 0px; background: #0e0e0e;">
<div id="container" style="width: 500px; margin:auto">
</div>
<script>
let div = document.getElementById('container');
var img = new Image();
img.onload = function() {
    console.log(this.width, this.height, this.width > this.height, window.innerWidth);
  if (this.width > this.height){  // 横向图设宽度
      if(this.width >  window.innerWidth){
          div.style.width =  window.innerWidth + "px"  // 宽度超过窗口宽度
      }else{
          div.style.width = this.width + "px"
      }
  }
  div.append(img);
}
img.src = '/img/{{imgindex}}';
</script>

<script>

currentIndex = {{ imgindex }}

function nextImg(){
    let url = window.origin + '?index=' + (currentIndex + 1);
    location.replace(url)
}

function lastImg(){
    let url = window.origin + '?index=' + (currentIndex - 1);
    location.replace(url)
}

function nextRandomImg(){
    let url = window.origin;
    location.replace(url)
}

function keyHandle(event){
    console.log(event.code)
    if(event.code === "Space"){
        nextRandomImg()
    }else if (event.code === "ArrowLeft"){
        lastImg()
    }else if (event.code === "ArrowRight"){
        nextImg()
    }
}

document.addEventListener('keydown', keyHandle);
</script>
</body>

</html>
'''

def collect_pics():
    img_exts = ['jpg', 'png', 'gif']
    data = []
    for ext in img_exts:
        imgs = list(Path(PICTURE_DIR).glob(f'**/*.{ext}'))
        print(f'Found {len(imgs)} {ext} img ')
        data.extend(imgs)
    return data   # 图片过多会占用较长时间启动，内存也会很大

data = collect_pics()
total = len(data)
print(f'Total image: {total}')

@app.route('/')
def home():
    index = request.args.get('index', random.randint(0, total))
    response = make_response(render_template_string(templ, imgindex=int(index)))
    response.cache_control.no_cache = True
    return response, 200


@app.route('/img/<int:index>')
def img(index):
    # filename = random.choice(data)
    filename = data[index]
    return send_file(filename, mimetype='image/gif')

if __name__ == "__main__":
    app.run(debug=True)
