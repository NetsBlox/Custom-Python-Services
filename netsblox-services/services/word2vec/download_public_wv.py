import gensim.downloader as api
from os import path

def save_wv(name):
    model_name = name.replace('word2vec-', '')
    model_path = path.join('models', model_name)
    if not path.isfile(model_path):
        print(f'Fetching {name}')
        wv = api.load(name);
        wv.save(model_path)
    else:
        print('model already exists. Skipping download')

    public_wv_file = path.join('models', 'public-wv.txt')
    if path.isfile(public_wv_file):
        with open(public_wv_file, 'r') as f:
            public_wvs = [ line.strip() for line in f.readlines() ]
    else:
        public_wvs = []
    if model_name not in public_wvs:
        with open(public_wv_file, 'a') as f:
            f.write(model_name + '\n')
    print(f'Saved new public word vectors {name} as {model_name}')


save_wv('word2vec-google-news-300')
