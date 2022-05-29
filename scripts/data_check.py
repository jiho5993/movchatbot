import pickle

with open('./recommender/data/users.pickle', 'rb') as f:
    user = pickle.load(f)

with open('./recommender/data/datas.pickle', 'rb') as f:
    data = pickle.load(f)

with open('./recommender/data/model.pickle', 'rb') as f:
    model = pickle.load(f)

print('============================ user ============================')

print(user)

print('============================ data ============================')

print(data)

print('============================ model ============================')

print(model)