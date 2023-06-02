import os
import pysolr
import requests
import pandas as pd
import joblib

CORE_NAME = "Reddit_data"
GCS_IP = "34.85.230.198"

def delete_core(core=CORE_NAME):
    print(os.system('sudo su - solr -c "/opt/solr/bin/solr delete -c {core}"'.format(core=core)))

def create_core(core=CORE_NAME):
    print(os.system(
        'sudo su - solr -c "/opt/solr/bin/solr create -c {core} -n data_driven_schema_configs"'.format(
            core=core)))

class Indexer:
    def __init__(self):
        self.solr_url = f'http://{GCS_IP}:8983/solr/'
        self.connection = pysolr.Solr(self.solr_url + CORE_NAME, always_commit=True, timeout=5000000)

    def do_initial_setup(self):
        delete_core()
        create_core()

    def create_documents(self, docs):
        total_docs = len(docs)
        for i in range(0, total_docs, 5000):
            try:
                print(self.connection.add(docs[i:i+5000]))
            except Exception as e:
                print(e)

    def add_fields(self):
        data = {
            "add-field": [

                {
                    "name": "parent_selftext",
                    "type": "text_en",
                    "multiValued": False,
                    "indexed":True,
                    "stored":True
                },
                {
                    "name": "Topics",
                    "type": "string",
                    "multiValued": False,
                    "indexed":True,
                    "stored":True
                },
                {
                    "name": "body",
                    "type": "text_en",
                    "multiValued": False,
                    "indexed":True,
                    "stored":True
                },
                {
                    "name": "parent_id",
                    "type": "string",
                    "multiValued": False,
                    "indexed":True,
                    "stored":True
                },

                {
                    "name": "parent_body",
                    "type": "text_en",
                    "multiValued": False,
                    "indexed":True,
                    "stored":True
                }

            ]
        }

        print(requests.post(self.solr_url + CORE_NAME + "/schema", json=data).json())


if __name__ == "__main__":
    i = Indexer()
#     i.do_initial_setup()
#     i.add_fields()
#     i.create_documents(index_data.to_dict("records"))
#   #  i.create_documents(comment_dict)
