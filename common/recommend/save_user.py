import pickle
import pandas as pd
import random

class DataSave:
    def __init__(self, req):
        self.User_req = req
        self.user_req_id = self.User_req['userRequest']['user']['id']
        self.user_input_data = self.User_req['userRequest']['utterance']

        path = './recommender/data'

        with open(f"{path}/datas.pickle","rb") as f:
            self.Review_Datas_df = pickle.load(f)

        with open(f"{path}/users.pickle","rb") as f:
            self.User_Datas_df = pickle.load(f)

        self.isUser = True
        self.user_data = self.User_Datas_df[self.User_Datas_df['UserRequestID'] == self.user_req_id]
        try:
            self.user_data.iloc[0]
        except:
            self.isUser = False

    def new_user(self, movie_id):
        new_user_id = self.Review_Datas_df['UserID'].max() + 1
        new_user_data = {'UserRequestID':self.user_req_id, 'UserID':new_user_id, 'MovieID':movie_id}
        self.User_Datas_df.loc[len(self.User_Datas_df.index)] = new_user_data

        self.review_data(movie_id, new_user_id)

    def old_user(self, movie_id):
        old_user_id = self.user_data.iloc[0]['UserID']
        old_user_movie = self.user_data.iloc[0]['MovieID']
        head = list(map(int, old_user_movie.split(',')))
        tail = int(movie_id)
        if tail not in head:
            head.append(tail)
            head.sort()

            movie = ','.join(list(map(str,head)))

            old_user_data = {'UserRequestID':self.user_req_id, 'UserID':old_user_id, 'MovieID':movie}
            self.User_Datas_df = self.User_Datas_df.drop(index=self.User_Datas_df.loc[self.User_Datas_df['UserRequestID'] == self.user_req_id].index)
            self.User_Datas_df.loc[len(self.User_Datas_df.index)] = old_user_data

            self.review_data(tail, old_user_id)

    def review_data(self, movie_id, user_id): # movieid userid int rating str
        columns = ['MovieName', 'MovieID', 'Genre', 'Rating', 'UserID', 'Review']
        review = '리뷰 없음'
        data = []
        try:
            movie = self.Review_Datas_df[self.Review_Datas_df['MovieID'] == movie_id].iloc[0]
            name = movie['MovieName']
            genre = movie['Genre']
        except:
            name = self.user_input_data
            genre = '장르없음'
        rating = random.randrange(7,11)
        data.append([name, movie_id, genre, rating, int(user_id), review])

        df = pd.DataFrame(data, columns=columns)

        self.Review_Datas_df = self.Review_Datas_df.append(df, ignore_index=True)

    def save_data(self):
        try:
            movie = self.Review_Datas_df[self.Review_Datas_df['MovieName'] == self.user_input_data].iloc[0]
            movie_id = str(movie['MovieID'])
        except:
            movie_id = str(self.Review_Datas_df['MovieID'].max()+1)
        
        if self.isUser:
            self.old_user(movie_id)
        else:
            self.new_user(movie_id)
        return self.User_Datas_df, self.Review_Datas_df