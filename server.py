from flask import Flask
from pathlib import Path
from flask import send_file, render_template_string, make_response, request
import random
import logging

logger = logging.getLogger(__name__)

PICTURE_DIR = 'J:/'  # 设定图片目录

PICTURE_DIR = Path(PICTURE_DIR).resolve()

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
<div id="container" style="width: 500px; height: 700px; margin:auto; margin-top: 10px; margin-bottom: 10px;">
</div>
<script>
let div = document.getElementById('container');
var img = new Image();
const maxWidth = window.innerWidth * 0.8
const maxHeight = window.innerHeight - 20
img.onload = function() {
    let height = Math.min(maxHeight, this.height);
    let width = this.width / (this.height / height);
    if (width > maxWidth){
        width = maxWidth
        height = this.height / (this.width / width)
    } 
    div.style.width = width + "px";
    div.style.height = height + "px";
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

data = []
total = 0
def collect_pics():
    logger.info(f'Searching {PICTURE_DIR}...')
    img_exts = ['jpg', 'png', 'gif']
    for ext in img_exts:
        imgs = list(Path(PICTURE_DIR).glob(f'**/*.{ext}'))
        logger.info(f'Found {len(imgs)} {ext} img ')
        data.extend(imgs)
    logger.info(f'Total image: {total}')
    return data   # 图片过多会占用较长时间启动，内存也会很大


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
    logging.basicConfig(level='INFO', format="%(asctime)s %(message)s")
    data = collect_pics()
    total = len(data)
    app.run(debug=True)
