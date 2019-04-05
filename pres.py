import os
import fire
import random
from flask import Flask, render_template, render_template_string, request, jsonify

GEORGE = [f'static/George/{f}' for f in os.listdir('static/George')]
# SLIDES = [f'static/slides/{f}' for f in os.listdir('static/slides')]
IMAGES = {f:f'static/images/{f}' for f in os.listdir('static/images')}
ORDER = ['title', 'dog','buddha', 'Koch_curve', 'sierpinski', 'brocolli', 'koch_zoom', 'paradox', 'measurement', 'line', 'square', 'cube', 'fracdim', 'complex', 'julia_def', 
 'fractal_julia', 'mandelbrot_def', 'fractal_mandel', 'union', "def_b_brot", 'Buddhabrot2', 'end_page']
app = Flask(__name__)

app.config['idx'] = 0
app.config['current_page'] = ORDER[0]
app.config['george_idx'] = 0

def images_html(i):
    print(app.config['george_idx'])
    print(app.config['idx'])
    print(app.config['current_page'])
    try:
        next_slide = ORDER[app.config['idx'] + 1]
        prev_slide = ORDER[app.config['idx'] - 1]
        
    except:
        next_slide = 'end_page'
        prev_slide = ORDER[app.config['idx'] - 1]

    if app.config['current_page'] == 'end_page':
        next_slide = "george"

    # if app.config['george_idx'] < len(GEORGE):
    #     img = GEORGE[app.config['george_idx']]
    #     app.config['george_idx'] += 1

    img = random.sample(GEORGE, 1)[0]
    # else:
    #     img = ""
    #     return image_page('real_end')
    if '.mp4' in img:
        style = ""
        vidstyle = f""" style='transform:rotate(270deg)'"""
        vid = f"""
        <video loop muted autoplay class="fsvid"{vidstyle}>
        <source src="{img}" type="video/mp4">
        </video>
        """
    else:
        style = "" #f""" style="background-image: url('{img}')" """
        vid = f"""
        <img src="{img}">
        """
        # vid = ""
    out = f"""
    <!doctype html>
<html>
    <head>
        <meta charset="utf-8"/>
        <title></title>
        <link rel="stylesheet" href="static/style.css">
        <link rel="icon" href="data:;base64,=">

    </head>
    <body onkeydown="rotator(event)">
    <script src='static/page_request.js'></script>
    <script> 
        const _next = '{next_slide}'
        const _prev = '{prev_slide}'
    </script>
    <div id='george' {style}>{vid}</div>

    </body>
</html>
    """
    return out

@app.route('/<image>')
def image_page(image):
    print(app.config['george_idx'])
    print(app.config['idx'])
    print(app.config['current_page'])
    print("image:  ", image)
    if "fractal_" in image:
        return fractal(image)

    if "george" in image:
        return render_template_string(images_html(1))

    if image != 'real_end':
        # try:
        app.config['idx'] = ORDER.index([o for o in ORDER if image in o][0])
        app.config['current_page'] = ORDER[app.config['idx']]
        next_slide = ""
        prev_slide = ""

        SLIDE_INDEX = app.config['idx']
        if SLIDE_INDEX > 0:
            prev_slide = ORDER[SLIDE_INDEX - 1]
        if SLIDE_INDEX < len(ORDER) - 1:
            next_slide = ORDER[SLIDE_INDEX + 1]
        else:
            next_slide = "george"
        # except IndexError:
        #     return images_html(1)
    else:
        next_slide = "real_end"
        prev_slide = "real_end"

    key = [k for k in IMAGES if image in k][0]
    image = IMAGES[key]
    vid = f"""
        <img src="{image}">
        """

    out = f"""
    <!doctype html>
<html>
    <head>
        <meta charset="utf-8"/>
        <title></title>
        <link rel="stylesheet" href="static/style.css">
        <link rel="icon" href="data:;base64,=">

    </head>
    <body onkeydown="rotator(event)">
    <script src='static/page_request.js'></script>
    <script> 
        const _next = '{next_slide}'
        const _prev = '{prev_slide}'
    </script>
    <div id='george'>{vid}</div>

    </body>
</html>
    """
    return render_template_string(out)


@app.route('/<int:arg>')
def page(arg):
    t = images_html(arg)
    return render_template_string(t)

@app.route('/ping')
def ping():
    return jsonify(pong=time.time())

@app.route('/real_end')
def fin():
    out=f"""
    <!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>title</title>
    <link rel="stylesheet" href="static/fractal.css">
    <link rel="icon" href="data:;base64,=">
  </head>
  <body onkeydown="rotator(event)">
    <iframe width="1206" height="678" src="https://www.youtube.com/embed/apP1Q7v6M7Y" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
  </body>
</html>"""
    return render_template_string(out)

        

@app.route('/fractals')
def fractal(frac = "fractal_julia"):
    if "julia" in frac:
        prev_slide = "julia_def"
        next_slide = "mandelbrot_def"
    else:
        prev_slide = "mandelbrot_def"
        next_slide = "union"

    out = f"""
    <!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>title</title>
    <link rel="stylesheet" href="static/fractal.css">
    <link rel="icon" href="data:;base64,=">
  </head>
  <body onkeydown="rotator(event)">
     <script> 
        const _next = '{next_slide}'
        const _prev = '{prev_slide}'
    </script>
        <script src='static/page_request.js'></script>
    <iframe src="http://0.0.0.0:8000" height="100%"></iframe>
  </body>
</html>
    """
    return render_template_string(out)

@app.route('/')
def idx():
    return image_page('title')


def main():
    app.run(host='0.0.0.0', port=8080, processes=1)

if __name__ == "__main__":
    # def main(i):
    #     with open('test.html', 'w') as f:
    #         t = images_html(i)
    #         f.write(t)
    fire.Fire(main)


    