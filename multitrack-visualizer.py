from flask import Flask, render_template, jsonify, request
import glob
import os

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
    # 递归列出所有子目录和文件
    file_tree = []
    file_tree.append(root_path)
    for root, dirs, files in os.walk(root_path):
        for dirname in dirs:
            file_tree.append(os.path.join(root, dirname))
        # for filename in files:
        #     file_tree.append(os.path.join(root, filename))
    return jsonify(file_tree)

@app.route('/audio-files')
def audio_files():
    directory = request.args.get('dir')  # 获取传递的目录参数
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