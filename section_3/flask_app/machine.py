from .database_main import get_data_to_anal
import seaborn as sns
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
import pandas as pd
import os

df = get_data_to_anal()
class learn():
    def __init__(self):
        self.df = pd.DataFrame()
        self.target = ''
        self.graph_x_aixs = ''
        self.graph_y_axis = ''
    @property
    def make_graph(self):
        len(self.df)*0.75
        train = self.df.sample(frac=0.75,random_state=1)
        test = self.df.drop(train.index)

        target = self.target
        y_train = train[target]
        y_test = test[target]

        predict = y_train.mean()


        # 기준모델로 훈련 에러(MAE) 계산

        y_pred = [predict] * len(y_train)
        mae = mean_absolute_error(y_train, y_pred)

        print(f'훈련 에러: {mae:.2f}')

        # 테스트 에러(MAE)
        y_pred = [predict] * len(y_test)
        mae = mean_absolute_error(y_test, y_pred)
        print(f'테스트 에러: {mae:.2f}')

        try :
            sns.regplot(x=train['origin_performance'], y=train['rating']).set_title('linear regression')
            return plt.savefig('flask_app\\static\\image\\filename.jpg')
        except :
            os.remove('flask_app\\templates\\filename.png')
            sns.regplot(x=train[f'{self.graph_x_aixs}'], y=train[f'{self.graph_y_aixs}']).set_title('linear regression')
            return plt.savefig('flask_app\\static\\image\\filename.jpg')


if __name__=='__main__':
    a=learn()
    a.df=df
    a.make_graph
    