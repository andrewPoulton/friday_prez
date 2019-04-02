import os
import fire
from flask import Flask, render_template, render_template_string, request, jsonify

IMAGES = [f'static/George/{f}' for f in os.listdir('static/George')]
app = Flask(__name__)

def images_html(i):
    img = IMAGES[i]
    if '.mp4' in img:
        style = ""
        vidstyle = f""" style='transform:rotate(270deg)'"""
        vid = f"""
        <video loop muted autoplay class="fsvid"{vidstyle}>
        <source src="{img}" type="video/mp4">
        </video>
        """
    else:
        style = f""" style="background-image: url('{IMAGES[i]}');background-size:100%" """
        vid = ""
    out = f"""
    <!doctype html>
<html>
    <head>
        <meta charset="utf-8"/>
        <title></title>
        <link rel="stylesheet" href="static/style.css">

    </head>
    <body>
    <div{style}>{vid}</div>

    </body>
</html>
    """
    return out

# @app.route('/')
# def index():
#     context = generate(None, True)
#     print(context)
#     context = app.config['tokenizer'].decode(context)
#     context = context[len('<CONV>'):].strip()
#     return render_template('index.html', context=context, special_tokens=jsonify(app.config['tokenizer'].special_tokens))
@app.route('/<int:arg>')
def page(arg):
    # with open('templates/page.html', 'w') as f:
    #     t = images_html(arg)
    #     f.write(t)
    t = images_html(arg)
    return render_template_string(t)

@app.route('/ping')
def ping():
    return jsonify(pong=time.time())

@app.route('/fractals')
def fractal():
    return render_template('fractals.html')


def main():
    app.run(host='0.0.0.0', port=8080, processes=1)

if __name__ == "__main__":
    # def main(i):
    #     with open('test.html', 'w') as f:
    #         t = images_html(i)
    #         f.write(t)
    fire.Fire(main)