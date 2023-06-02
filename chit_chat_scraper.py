import json
import pandas as pd
f = open('data.json')
data = json.load(f)
f.close()

df = pd.DataFrame.from_dict(data, orient="index")
del df["ratings"]
del df["start"]

# data
list_of_messages = []
questions = []
answers = []
data_final = data.values()
# print(data_final)
for conversation in data_final:
    conversation = conversation['messages']
    for data_a in conversation:
        if(type(data_a)==list):
            list_of_messages.extend(data_a)
print(len(list_of_messages))
for i in range(0, len(list_of_messages)):
    if i%2==0:
        questions.append(list_of_messages[i]["text"])
    else:
        answers.append(list_of_messages[i]["text"])
# print(questions)
# print("-----")
# print(answers)

df_questions1 = pd.DataFrame(questions)
df_answers1 =pd.DataFrame(answers)
df_conversations1 = pd.concat([df_questions1,df_answers1],axis =1)
df_conversations1.columns =["questions","answers"]
df_conversations1=df_conversations1.dropna()

xyz = json.loads(df_conversations1.to_json(orient = "records"))
#del xyz['data']['index']

json_object= json.dumps(xyz)
#parsed = json.loads(xyz)
#json_object = json.dumps(parsed, indent=4)

with open("sample2.json", "w") as outfile:
    outfile.write(json_object)