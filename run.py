from app import create_app
import json
app=create_app()
dataset_path = ""
with open('./dataset_conf.json', 'r') as conf:
    dataset_path = json.load(conf)['dataset_path']
app.config['dataset_path'] = dataset_path
if __name__ == "__main__":
    app.run(debug=True, port=5000)