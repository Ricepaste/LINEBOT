import os
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# LINE BOT info
line_bot_api = LineBotApi(
    '0VH971y+3x7IbFvRMKzY+0w/pFaOOvJa6M+IEpADMVmNWZLtmLLNB7wek1PBcOnKVAWRYh3eqtD2JjNXpReRpxg42KQTEFQqMLk9wr9uZR3TrSOAhlRnT1URcX3zDiNFiIKYue4AQXT3T0pySXGEVQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ef511c10f38305d34d906fe9421acd39')

# NPC interaction story
story = {
    "start": {
        "message": ("早期自大陸渡海來台的漢人移民，多來自閩粵兩地，閩籍居民泰半為漳、泉二府人氏，"
                    "粵籍則為嘉應州及潮州、惠州的客家人，在清朝時，漳、泉、客三族人群涇渭分明，但今天，"
                    "除了桃竹苗和美濃等地客家文化還非常突顯，其他地區的客族已與閩南族群融合，成為「福佬客」。"
                    "有許多年輕一代的客籍青年都只說閩南語和國語，更甚至不知道自己是客籍的人。住在員林的江河鄰（小江）"
                    "是還在就讀小學六年級的學生，就在一次跟著爺爺去祭祖時偶然發現爺爺跟祖先說話時用的不是國語，"
                    "也不是在國小裡學到的閩南語，因此感到很好奇。後來一問之下他才知道原來那是客家話，而他們家其實是客籍家族，"
                    "所以他身上也流淌著客家的血脈。然而他們家族已經深受周圍環境引響而導致福佬化，平時都說國語和閩南語，"
                    "已經漸漸忘記身為客家人的事情。因此小江決定來到客家人聚集的大市「桃園」，來尋找自己的客家認同感，"
                    "並且更加了解有關客家人的文化和歷史。就在這時他遇到了鍾肇政，並決定從這裡開始追尋客家的記憶。"
                    "就讓我們一起跟隨小江一起開始這趟旅程吧！"),
        "question": "Q1:請問鍾肇政筆下的家鄉是哪裡呢？",
        "options": ["A:龍潭", "B:台北", "C:高雄"],
        "answer": "A",
        "next": "q2"
    },
    "q2": {
        "message": ("進入鍾肇政文學生活園區。沿著斑駁的紅磚牆走著，小江突然看到牆邊似乎有著什麼......"
                    "走近一看發現是一口只有半邊的古井"),
        "question": "Q2:原來這是當年的「共用古井」，過去從早到晚都有住在宿舍的______來洗衣、洗菜，孩子們也會在井邊嬉戲",
        "options": ["A:先生娘", "B:小朋友", "C:阿婆"],
        "answer": "A",
        "next": "q3"
    },
    "q3": {
        "message": "小江看到牆邊有一段話...請依序排出下文",
        "question": "Q3:請依序排出下文...",
        "options": ["A:龍潭係吾故鄉", "B:不時都來掛心腸", "C:分𠊎來日夜想", "D:故鄉係吾母", "E:發夢都會來想"],
        "answer": "DCAEAB",
        "next": "q4"
    },
    "q4": {
        "message": ("小江走進鐘老的舊居，發現桌上擺放著的是鍾肇政老師的手稿..."
                    "Q4:請問是鍾肇政的哪一個作品呢？"),
        "question": "Q4:請問是鍾肇政的哪一個作品呢？",
        "options": ["A:歸來記", "B:魯冰花", "C:濁流三部曲"],
        "answer": "A",
        "next": "q5"
    },
    "q5": {
        "message": ("鍾肇政居住於此時曾主動發起《文友通訊》，他文友通訊的摯友們包括台北施翠峰和陳火泉、新竹許炳成、"
                    "頭城李榮春、汐止廖清秀，以及同為客家人的_________"),
        "question": "Q5:鍾肇政居住於此時曾主動發起《文友通訊》，他文友通訊的摯友們包括台北施翠峰和陳火泉、新竹許炳成、"
        "頭城李榮春、汐止廖清秀，以及同為客家人的_________",
        "options": ["A:美濃鍾理和", "B:新竹林海音", "C:台南葉石濤"],
        "answer": "A",
        "next": "q6"
    },
    "q6": {
        "message": ("小江：「房間的最尾端看起來像是另外加蓋出去的廚房和餐廳，走過去看一看吧！」"
                    "Q6:小江：「哇桌上擺著都是家裡常見的客家菜欸！有滷豬腳、酸菜炒肉絲.......還有鍾老最愛的鹹菜湯跟_____」"),
        "question": "Q6:小江：「哇桌上擺著都是家裡常見的客家菜欸！有滷豬腳、酸菜炒肉絲.......還有鍾老最愛的鹹菜湯跟_____」",
        "options": ["A:九層糕", "B:客家米粉", "C:牛肉麵"],
        "answer": "A",
        "next": "end"
    },
    "end": {
        "message": ("小江：哇，在遊覽完整個園區後，感覺對日治時期的台灣文學作家以及客語作品都有了更多的了解。"
                    "鐘老不僅被譽為台灣文學之母，在臺灣客家運動的推展上更有著不容小覷的貢獻。1970年代，鍾老積極為眾多文學紀念館的成立四處奔走，"
                    "甚至包括還我客家母語運動、臺灣客家公共事務協會、寶島客家電臺的設立皆與其大力推動有關。等回去以後我一定要讀他最著名的作品，"
                    "長篇小說《魯冰花》、大河小說《濁流三部曲》以及《臺灣人三部曲》!"
                    "小江：現在讓我們一起問鐘老「下一個要探訪的地點在哪呢？」吧！"),
        "question": "下一個要探訪的地點在哪呢？",
        "options": ["A:菱潭街興創基地", "B:大河壩小書店", "C:胡嘉猶乙未抗日碑"],
        "answer": "A",
        "next": "finish"
    },
    "finish": None
}

user_data = {}


@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_type = event.message.type
    user_id = event.source.user_id
    reply_token = event.reply_token
    message = event.message.text.strip()

    # Check user progress or start the story
    if message == "開始":
        start_story(user_id, reply_token)
    else:
        user_progress = get_user_progress(user_id)
        if user_progress:
            current_question = story.get(user_progress)
            if message == current_question['answer']:
                next_question = story.get(current_question['next'])

                # line_bot_api.reply_message(
                #     reply_token, TextSendMessage(text=current_question['message']))
                # line_bot_api.reply_message(
                #     reply_token, TextSendMessage(text=current_question['next']))

                send_question(reply_token, next_question)
                set_user_progress(user_id, current_question['next'])
            else:
                send_message(reply_token, "回答錯誤，請再試一次。")
        else:
            send_message(reply_token, "請輸入 '開始' 開始遊戲。")


def start_story(user_id, reply_token):
    initial_question = story['start']
    set_user_progress(user_id, 'start')
    send_question(reply_token, initial_question)


def send_question(reply_token, question):
    if question is not None:
        options_text = "\n".join(
            question['options']) if question['options'] else ""
        full_message = f"{question['message']}\n\n{question['question']}\n{options_text}"
        line_bot_api.reply_message(
            reply_token, TextSendMessage(text=full_message))
    else:
        line_bot_api.reply_message(
            reply_token, TextSendMessage(text="恭喜你完成了所有關卡！\n請輸入 '開始' 重新開始遊戲。"))


def send_message(reply_token, message):
    line_bot_api.reply_message(reply_token, TextSendMessage(text=message))


def get_user_progress(user_id):
    # This function should retrieve the user's progress from a database or memory
    # For simplicity, using a dictionary as a placeholder
    if user_id not in user_data:
        return None
    return user_data[user_id]


def set_user_progress(user_id, question_key):
    # This function should update the user's progress in a database or memory
    global user_data
    user_data[user_id] = question_key


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)
