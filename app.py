from flask import Flask, render_template, request, session
import random


app = Flask(__name__)

app.secret_key = "guess_game"


# 產生答案
def create_answer():
    return random.sample(range(10), 4)



# 判斷幾A幾B
def check_answer(answer, guess):

    A = 0
    B = 0

    for i in range(4):

        # 位置跟數字都正確
        if answer[i] == guess[i]:
            A += 1

        # 數字正確但位置錯
        elif guess[i] in answer:
            B += 1

    return A, B



# 首頁
@app.route("/")
def index():

    if "answer" not in session:

        session["answer"] = create_answer()
        session["history"] = []
        session["win"] = False


    return render_template(
        "index.html",
        history=session["history"],
        answer=None,
        win=session["win"]
    )



# 猜數字
@app.route("/guess", methods=["POST"])
def guess():


    number = request.form["number"]


    # 檢查格式
    if len(number) != 4 or not number.isdigit():

        return render_template(
            "index.html",
            history=session["history"],
            answer=None,
            win=False,
            error="請輸入4位數字!"
        )


    # 檢查重複
    if len(set(number)) != 4:

        return render_template(
            "index.html",
            history=session["history"],
            answer=None,
            win=False,
            error="不能輸入重複數字!"
        )



    guess_number = list(map(int, number))


    A, B = check_answer(
        session["answer"],
        guess_number
    )


    result = f"{number} → {A}A{B}B"


    history = session["history"]

    history.append(result)

    session["history"] = history



    if A == 4:

        session["win"] = True



    return render_template(
        "index.html",
        history=history,
        answer=None,
        win=session["win"]
    )





# 顯示答案
@app.route("/answer")
def show_answer():


    answer = "".join(
        map(str, session["answer"])
    )


    return render_template(
        "index.html",
        history=session["history"],
        answer=answer,
        win=session["win"]
    )





# 重新開始
@app.route("/restart")
def restart():


    session["answer"] = create_answer()

    session["history"] = []

    session["win"] = False


    return render_template(
        "index.html",
        history=[],
        answer=None,
        win=False
    )




if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )