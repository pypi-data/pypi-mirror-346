from ep_sdk_4pd.ep_data import EpData


def test_predict_data():
    print('-------------test_predict_data-------------')

    data = EpData.get_predict_data(scope="plant",is_test=True,test_time='2023-04-02')
    print(data)
    print('-------------------------------------')


if __name__ == '__main__':
    test_predict_data()
