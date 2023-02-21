import os.path as osp
from joblib import load
import numpy as np
import pandas as pd

from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)


model_name = "pipeline_key_rep.pkl" #TODO: search from config 

models_path= "../"

model = load(osp.join(models_path,model_name))  

def extract_dataset():
    path_to_data = "../data/Anime_data.csv"
    df = pd.read_csv(path_to_data).dropna()
    df['Producer'] = df['Producer'].apply(lambda x: eval(x)[0] if not  pd.isna(x) else None)
    df['Studio'] = df['Studio'].apply(lambda x: eval(x)[0] if not  pd.isna(x) else None)
    df['Genre'] = df['Genre'].apply(eval)
    df["list_rep"]=df.apply(lambda x: " ".join([x['Title'],*x['Genre'],x['Type'],x['Producer'],x["Studio"]]),axis=1)
    rep_mat = model.transform(df['list_rep'])
    return df,rep_mat 

df,rep_mat = extract_dataset()
print(rep_mat.shape)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/result",methods=['POST'])
def classify():

    key = request.form['key']

    sims = (rep_mat @ model.transform([key]).T).toarray().squeeze()
    top_4_sims = np.argpartition(sims, -4)[-4:][::-1]
    df_top = df.iloc[list(top_4_sims)]
    results = [ {"name":df_top.iloc[i]['Title'],'rating':df_top.iloc[i]['Rating'],"studio":df_top.iloc[i]['Studio']} for i in range(4)]
    # results = [{"name":"key"},{"name":"oui"}]
    return render_template("result.html", results=results)
