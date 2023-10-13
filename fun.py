from env import *
import random as rd
import time
import datetime
import pymysql

def wordLoad():
    words = []

    with open('./data/word.txt') as f:
        for word in f:
            words.append(word.strip())
    # print(words)
    return words

def gameRun(words):
    print("Type the words you see on the screen correctly.")
    print("You will receive 5 random words.")
    input("ARE U READY? press 'ENTER' to start")
    print()
    print("Here we go!")
    time.sleep(3)

    cor_cnt = 0
    start = time.time()

    for i in range(5):
        rd.shuffle(words)
        word = rd.choice(words)

        print()
        print("Word Number # {}".format(i+1))
        print(word)

        ans = input()
        print()

        if str(word).strip() == str(ans).strip():
            print("Excellent!")
            cor_cnt += 1
        else:
            print("Incorrect!")

    end = time.time()
    time_final = end - start
    time_final = format(time_final, ".3f")

    now_date = datetime.datetime.now()
    now_date = now_date.strftime("%Y-%m-%d %H:%M:%S")

    conn = pymysql.connect(host=host, user=user, password=password, charset=charset)
    cur = conn.cursor()

    sql = "CREATE DATABASE IF NOT EXISTS word_game"

    cur.execute(sql)

    sql = "USE word_game"

    cur.execute(sql)

    sql = """
    CREATE TABLE IF NOT EXISTS game_records (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    cor_cnt SMALLINT NOT NULL,
    record FLOAT NOT NULL,
    regdate varchar(20)
    )
    """
    cur.execute(sql)

    sql = "INSERT INTO game_records(cor_cnt, record, regdate) VALUES (%s, %s, %s)"
    cur.execute(sql, (cor_cnt, time_final, now_date))

    conn.commit

    sql = "SELECT * FROM game_records"
    cur.execute(sql)

    result_data = cur.fetchall()
    conn.close()

    print("-"*50)
    if cor_cnt == 5:
        print("PERFECT!")
        print("Wow, you're really good at typing!")
    elif cor_cnt <= 4 :
        print("Great!")
    elif cor_cnt == 1 :
        print("I think you need focus more...")
    else:
        print("It's okay. You just have to practice more.")

    print("Record:", time_final, "sec /", "correct:", cor_cnt )

    print('='*50)
    print("No.\tCounts\tTime\tdDate")
    print('='*50)
    for record in result_data:
        print('{}\t{}\t{}\t{}'.format(record[0], record[1], record[2], record[3]))
    print('-'*50)

if __name__ == '__main__':
    words = wordLoad()
    gameRun(words)