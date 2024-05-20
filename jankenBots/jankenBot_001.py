import pandas as pd
import csv
from sklearn.tree import DecisionTreeClassifier

pastHands = [0]*4

handsCsvLink = 'Data/hand_Data.csv'
resultCsvLink = 'Data/result_Data.csv'

def inputHand(Question):
    """ユーザーが出す手を取得する関数

    引数:
        Question (str): 何を出すか尋ねる質問文

    戻り値:
        int: ユーザーが出した手
    """
    yourHand = int(input(Question))
    if yourHand == 1 or yourHand == 2 or yourHand == 3:
        return yourHand
    else:
        print("1, 2, 3のいずれかを入力してください")
        return inputHand(Question)
def doJanken(yourHand):
    """じゃんけんを行う関数

    引数:
        yourHand (int): ユーザーが出した手

    戻り値:
        result(str): 勝敗結果
    """
    # リストにユーザーが出した手を追加
    pastHands[0] = pastHands[1]
    pastHands[1] = pastHands[2]
    pastHands[2] = pastHands[3]
    pastHands[3] = yourHand
    # データを読み込む
    df = pd.read_csv(handsCsvLink)
    X = df[['b3h', 'b2h', 'b1h']]
    Y = df['hand']
    # モデル作成
    clf = DecisionTreeClassifier(random_state=0)
    clf.fit(X, Y)
    # 予測
    pred = clf.predict(pd.DataFrame(
        {"b3h": [pastHands[0]],
         "b2h": [pastHands[1]],
         "b1h": [pastHands[2]]}))
    # 記録
    writeCsv([pastHands[0], pastHands[1], pastHands[2], yourHand], handsCsvLink)
    # 勝敗判定
    if yourHand == pred:
        result = "w"
    else:
        result = "l"
    return result
def writeCsv(data, csvLink):
    """CSVファイルにデータを書き込む関数

    引数:
        data (str): 書き込むデータ
        csvLink (str): 書き込むCSVファイルのリンク
    """
    with open(csvLink, 'a', newline='\n') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(data)
    csvFile.close()
def resetResultCsv():
    with open(resultCsvLink, 'a', newline='')as csvFile:
        csvFile.truncate(0) #現在のファイルサイズを０にする
    csvFile.close()

resetResultCsv()
for i in range(100):
    writeCsv(doJanken(inputHand("あなたの手")), resultCsvLink)