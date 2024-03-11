from flask import Flask, render_template, jsonify, request
import glob
import os
from filetree import *

import argparse

argparser = argparse.ArgumentParser(description='Generate a list of audio files in a directory')
argparser.add_argument('--dir', help='Directory to search for audio files', type=str, required=True)
argparser.add_argument('--port', help='Port to run the server on', type=int, default=5000)
argparser.add_argument('--multitrack', help='Use multitrack mode', action='store_true')

root_path = argparser.parse_args().dir
port = argparser.parse_args().port
multi_track = argparser.parse_args().multitrack
print(argparser.parse_args())
app = Flask(__name__, static_folder=root_path, static_url_path='')

@app.route('/')
def index():
    print(multi_track)
    if not multi_track:
        print('non-stems')
        return render_template('index-non-stems.html')
    else:
        print('stems')
        return render_template('index-stems.html')  # 确保您的模板文件名正确

@app.route('/files')
def list_files():
    # 列出第一层目录
    init_file_tree(root_path)
    # print(id2node)
    return jsonify(id2node)

@app.route('/expand')
def expand_dir():
    # 递归列出所有子目录和文件
    expand_file_node(int(request.args.get('id')))
    return jsonify(id2node)

@app.route('/collapse')
def collapse_dir():
    # 递归列出所有子目录和文件
    collapse_file_node(int(request.args.get('id')))
    return jsonify(id2node)

@app.route('/audio-files')
def audio_files():
    directory_id = request.args.get('dir')  # 获取传递的目录参数, 为id的值
    directory = id2node[int(directory_id)]['dir']
    res = {}
    if request.args.get('parseall') is None:
        audio_files = [glob.glob(directory + '/*.' + ext) for ext in ['mp3', 'wav', 'flac']]
    else:
        audio_files = [glob.glob(directory + '/**/*.' + ext, recursive=True) for ext in ['mp3', 'wav', 'flac']]
    audio_files = [item for sublist in audio_files for item in sublist]
    audio_files = [os.path.relpath(f, root_path) for f in audio_files]
    res['directory'] = directory
    res['audio_files'] = audio_files
    res['multitrack'] = multi_track
    return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True, port=port)  # 确保您的静态文件夹名正确