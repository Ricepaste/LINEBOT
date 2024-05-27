import os
import time
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError,
    LineBotApiError
)
from linebot.models import *

app = Flask(__name__)

# LINE BOT info
line_bot_api = LineBotApi(
    '0VH971y+3x7IbFvRMKzY+0w/pFaOOvJa6M+IEpADMVmNWZLtmLLNB7wek1PBcOnKVAWRYh3eqtD2JjNXpReRpxg42KQTEFQqMLk9wr9uZR3TrSOAhlRnT1URcX3zDiNFiIKYue4AQXT3T0pySXGEVQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ef511c10f38305d34d906fe9421acd39')

DEBUG = True

# NPC interaction story

story = {
    "start": {
        "messages": [("鍾肇政文學園區 （起點）\n"
                     "1.菱潭街興創基地 \n2.大河壩小書店  \n3.胡嘉猶乙未抗日碑 \n4.龍元宮 \n5. 三坑老街\n\n"
                      "小江一開始先來到了鍾肇政文學園區，想要從這裡開始旅程。鐘老又被稱為「台灣文學之母」，"
                      "他把龍潭的周遭空間，一點一滴寫進他的文章裡，但是這附近還有好多跟客家相關的景點，"
                      "而小江今天要去「三個地方」，但是想知道下一個地點在哪，就必須先完成這個地點的任務，"
                      "才會得到關於下一個景點的提示喔！"
                      "那我們就趕快和小江一起，跟著鐘老的筆觸所至一起更加認識龍潭裡的客家。\n\n"),

                     ('天上的星星不說話 地上的娃娃想媽媽\n'
                      '天上的眼睛眨呀眨 媽媽的心呀魯冰花\n'
                      '家鄉的茶園開滿花 媽媽的心肝在天涯\n'
                      '夜夜想起媽媽的話 閃閃的淚光魯冰花'),

                     '《魯冰花》是許多台灣人共同的回憶，《魯冰花》是作者鍾肇政自1960年開始連載的長篇小說，故事中的場景多描述其家鄉的環境'],
        "question": "Q1:請問鍾肇政筆下的家鄉是哪裡呢？",
        "options": ["A:龍潭", "B:台北", "C:高雄"],
        "answer": "A",
        "next": "q2"
    },
    "q2": {
        "messages": [("鍾肇政出身於桃園龍潭的客家莊，《魯冰花》即是在這裡藴育而成的，龍潭過去是茶葉的重要產地，《魯冰花》亦是以茶農為故事背景開展。"
                      "小小的魯冰花在路邊默默綻放，凋謝後成為茶園的肥料，象徵著犧牲奉獻的精神，因此又被稱為客家人的母親花"),

                     "現在就讓我們跟著鐘老的腳步一起探索龍潭吧！\n進入鍾肇政文學生活園區。",

                     "沿著斑駁的紅磚牆走著，小江突然看到牆邊似乎有著什麼......"
                     "走近一看發現是一口只有半邊的古井"],
        "question": "Q2:原來這是當年的「共用古井」，過去從早到晚都有住在宿舍的______來洗衣、洗菜，孩子們也會在井邊嬉戲",
        "options": ["A:先生娘", "B:小朋友", "C:阿婆"],
        "answer": "A",
        "next": "q3"
    },
    "q3": {
        "messages": [
            "先生娘 xin24 sang24 ngiong11 (四縣)，用以稱呼醫生或老師的妻子，意指師母、醫生夫人。共用古井原先是完整的一口井，在學校擴建時曾被掩埋，重新出土後才變成現在只剩半邊井的樣貌。",

            "這時，小江看到旁邊好像有人影",

            "😮原來是鐘爺爺坐在旁邊的木椅慈祥地看著他。",

            "小江走向鐘爺爺所在的建築物想要一探究竟，看到門牌上寫著這裡是南龍路3號",

            "(小江來到了位在3號宿舍的園區資訊站)\n鍾肇政生活園區由龍潭國小宿舍群、武德殿組成。宿舍包含3號宿舍(園區資訊站)；5、7號宿舍(大河學堂)；9號宿舍(以文會友講堂)、11號宿舍(鍾肇政舊居)",

            "一面牆上有著用毛筆寫下的一段話：「麼儕無故鄉，麼儕毋想鄉......」"
        ],
        "question": "Q3:請依序排出下文...",
        "image_urls": ["https://i.imgur.com/j71sZHb.png", "https://pic.pimg.tw/siouteng0822/1694172035-1521326360-g_n.jpg"],
        "options": ["A:龍潭係吾故鄉", "B:不時都來掛心腸", "C:分亻厓來日夜想", "D:故鄉係吾母", "E:發夢都會來想"],
        "answer": "DCAEAB",
        "next": "q4"
    },
    "q4": {
        "messages": [
            "《龍潭故鄉》是鍾老於千禧年時，在離這裡不遠處的龍潭大池邊提筆以客語書寫的。",

            "小江沿著展區路線，觀賞了許多鍾肇政的作品，像是《魯冰花》、《濁流三部曲》、《臺灣人三部曲》等等，最後來到了園區最裡面的日式教師宿舍，也就是鍾肇政的舊居。",

            "在這裡彷彿能看到鍾老過去生活的痕跡，一張精美的檜木書桌佔去了房間大半的面積，鍾肇政許多作品是在這裡完成的，小江仔細一看發現桌上擺放著的是鍾肇政老師的手稿"
        ],
        "question": "Q4:請問是鍾肇政的哪一個作品呢？",
        "options": ["A:歸來記", "B:魯冰花", "C:濁流三部曲"],
        "answer": "A",
        "next": "q5"
    },
    "q5": {
        "messages": [
            "〈歸來記〉：「那還是個匱乏的年代，不過我特別記得剛剛有日光燈的時代。託它之賜，我能在過去所想像不到的光線下，開始寫我的第一部長篇小說，題曰：《魯冰花》。」"
        ],
        "question": "Q5:鍾肇政居住於此時曾主動發起《文友通訊》，他文友通訊的摯友們包括台北施翠峰和陳火泉、新竹許炳成、"
        "頭城李榮春、汐止廖清秀，以及同為客家人的_________",
        "image_urls": ["https://i.imgur.com/fmnJ3cW.png"],
        "options": ["A:美濃鍾理和", "B:新竹林海音", "C:台南葉石濤"],
        "answer": "A",
        "next": "q6"
    },
    "q6": {
        "messages": [
            "小江：「房間的最尾端看起來像是另外加蓋出去的廚房和餐廳，走過去看一看吧！」"
        ],
        "question": "Q6:小江：「哇桌上擺著都是家裡常見的客家菜欸！有滷豬腳、酸菜炒肉絲.......還有鍾老最愛的鹹菜湯跟_____」",
        "image_urls": ["https://i.imgur.com/n15yPIP.png"],
        "options": ["A:九層糕", "B:客家米粉", "C:牛肉麵"],
        "answer": "A",
        "next": "q7"
    },
    "q7": {
        "messages": [
            "「九層粄」是以一層加了紅糖水的米漿，和一層加了鹽的白色米漿，蒸製而成的，口感甜中帶鹹，外型類似東南亞的娘惹糕，層層分明、棕白相間。有象徵著步步高升、升官發財之意；於年節食用則有希望長輩能長命百歲，活得平安長久的意涵。\n\n此外，客家人時常在料理中加入酸菜，鍾肇政最喜歡妻子煮的「鹹菜湯」，就是將鹹菜片（酸菜片）加上三層肉切片慢慢燉煮成湯。",

            "小江：哇，在遊覽完整個園區後，感覺對日治時期的台灣文學作家以及客語作品都有了更多的了解。",

            ("鐘老不僅被譽為台灣文學之母，在臺灣客家運動的推展上更有著不容小覷的貢獻。1970年代，鍾老積極為眾多文學紀念館的成立四處奔走，"
             "甚至包括還我客家母語運動、臺灣客家公共事務協會、寶島客家電臺的設立皆與其大力推動有關。等回去以後我一定要讀他最著名的作品，"
             "長篇小說《魯冰花》、大河小說《濁流三部曲》以及《臺灣人三部曲》!"),

            "小江：現在讓我們一起問鐘老「下一個要探訪的地點在哪呢？」吧！",

            "(回答)鐘老：我有一個推薦的地方，那裡的發展說起來跟我也有點關係，給你們一點提示吧。",
            '''舊市場華麗變身，
文創一條街迎新生。
社區小教室裡，
手作體驗溫馨情。
小書店安靜角落，
藝文新據點，心靈的港灣。

混搭美味在舌尖，
傳統與創意齊舞，
新滋味在唇間。

街區微旅行，
步步走讀老城，
昔日風華，
依然動人心弦。
這樣就知道在哪裡了吧？'''
        ],
        "question": "下一個要探訪的地點在哪呢？",
        "options": ["# 菱潭街興創基地", "# 大河壩小書店", "# 胡嘉猶乙未抗日碑"],
        "answer": "菱潭街興創基地",
        "next": "q85"
    },
    "q85":
        {
            "messages": ["進入菱潭街興創基地。"],
            "question": "(請拍攝並上傳入口照片)",
            "options": [],
            "answer": "",
            "allow_image_upload": True,
            "next": "q9"
    },
    "q9": {
        "messages": [("鐘老：菱潭街興創基地真是一個充滿文藝氣息的街市，其實這裡的發展說起來也跟我有點關係，"
                      "菱潭街的創生發起人張智宇先生就是在閱讀了我著作《魯冰花》後，他們才發現：文章中的水城鄉就是龍潭鄉，"
                      "而水城國校即龍潭國小，透過小說可以連結到龍潭真實的地景意象，儘管當地有很多歷史地景已被拆除，"
                      "但仍被保存在我的筆下。"),

                     "於是他便開始發想文學是不是可以串聯藝術與文化？是否可以跟在地的商業和觀光去做結合？以及激勵更多年輕人返鄉去做更多的藝文創作。在2014年時這個小小的心願種子就在菱潭街種下，開始發芽成長。"
                     ],
        "question": "Q：小江：聽說這條街有一間店希望在街區提供一處如同自己家一般的餐飲處所，讓來往遊客停下歇腳、聊天。"
        "店內提供手沖咖啡、濃郁的主廚咖哩，適合在逛完商店街後，坐下細細品味美味輕食與飲品。而且他的店名是客語的「客廳」的意思，"
        "你們能告訴我那間店的名字嗎？",
        "image_urls": ["https://travel.tycg.gov.tw/content/images/attractions/47971/1024x768_attractions-image-gc1ct2gvwuqz0yo-vogqlw.jpg"],
        "options": ["# 廳下小餐館", "# 客家會館", "# 阿婆小吃"],
        "answer": "A",
        "next": "q10"
    },
    "q10": {
        "messages": [
            "「廳下」除了指客廳以外，在傳統客家家庭內，也是客家族群祭祀祖先牌位的神聖空間。2022年女性影展鐘導演鄭慧玲拍攝的紀錄片作品命名為「廳下火」，這邊的「火」有點燈的意思。「廳下火」，是說客家家庭在傍晚臨暗時節，伙房內成員除了點香敬拜祖先之外，點廳下火即是傍晚固定例行性的工作。不管廳下有無安奉祖先牌位，或是伙房已無人口居住，或是已當作是閒置空間，讓廳下火的光芒徹夜照亮伙房禾埕。",

            ("Q：小江：說到客家文化就不得不了解一下客家美食吧。客家族群早期先民們需要靠自己雙手勞動拓荒墾殖，"
             "因此客家的勞動強度是很高的，要以勞力換取生存，改善經濟，所以也就順應環境發展出什麼菜系風格？"
             "（答題格式）「 」、「 」、「 」")],
        "question": "Q：請選擇客家菜的風格",
        "options": ["# 鹹、香、肥", "# 甜、香、嫩", "# 酸、辣、甜"],
        "answer": "鹹、香、肥",
        "next": "q11"
    },
    "q11": {
        "messages": [("Q：這裡有一間叫艸木間的店也有許多客家特色的菜餚，其中刈包有一種口味是搭配了客家的特色醬汁，是用金桔所製成，你們知道那是什麼嗎？")],
        "question": "Q：請選擇客家的特色醬汁",
        "options": ["A:醬油膏", "B:桔醬", "C:豆瓣醬"],
        "answer": "B",
        "next": "q12"
    },
    "q12": {
        "messages": [
            "桔醬是客家庄特有的沾醬。每年的11月底至隔年過年前，是金桔盛產的季節。製作桔醬是將金桔蒸熟去子磨醬，再用鹽、辣椒調味。有著金桔濃郁的香味，客家人習慣吃白斬雞、白切五花肉時，將其作成沾料與沾醬，顏色偏黃帶甜稠，口感細膩帶酸甜。不但可去油膩，也可以開胃，促進食慾，令人回味。通常金桔醬會因金桔的種植生產，以北部新竹、北埔地區產量較多，南部地區則少產。",
            ("小江：原來那是桔醬gidˋ jiong阿，那酸甜濃郁的滋味真的會讓人胃口大開呢。誒那邊好像有一間跟客家茶業相關「製品」的店，"
             "我們一起過去看看吧！")],
        "question": "Q：請找到正確店家並回復「抵達（店名）」",
        "options": ["# 秘丞手作", "# 客家茶坊", "# 茶葉之家"],
        "answer": "抵達秘丞手作",
        "next": "q13"
    },
    "q13": {
        "messages": [("秘丞手作主打草本植物手工皂的秘丞手作，最大特色是手工皂選用與客家文化相關的植物製作，如龍潭客家庄的在地包種茶，"
                      "以及在地自家種植的紅茶，以茶葉入皂；或是選用在地產的薑黃、紅麴、備長炭、橫山鄉老薑爺爺種植的無毒老薑等製作客家元素香皂。"),

                     ("客家人素以熱情好客著稱，「以茶敬客、以茶會友；以茶爲禮、以茶敘情」早已成爲客家人生活的一部份，不僅是文化的傳承，"
                      "更在南遷落腳過程中發展了茶業。經由客家人研發成功或客家文化獨創的茶品，如膨風茶（又稱白毫烏龍、椪風茶、東方美人茶）、"
                      "酸柑茶、柚子茶、柚香茶等，源於客家人勤儉惜物的天性而創出，也最能反映客家精神與風貌。")],
        "question": "Q：請將以下茶葉與其特色作配對\n"
        "1膨風茶\n2柚子茶\n3酸柑茶\n\n"
        "Ａ代表客家人克勤克儉精神。是早年客家人在春節時以虎頭柑拜神，擺放過年後不捨丟棄，因此將柑桔挖洞後取出果肉，"
        "再將茶葉、紫蘇、薄荷、甘草等各家不同的配料攪拌混合後回填虎頭柑中，接著經過九蒸九曬才宣告完工。"
        "是可以紓緩扁桃腺發炎、降火氣、潤喉、爽聲、提神的天然果茶飲。\n"
        "Ｂ命名有客語「吹牛」之，原料多以選用心芽肥大、白毫多、葉質柔軟且遭小綠葉蟬刺吸過之「一心二葉」為主，"
        "而茶湯水色呈橙紅色，具天然的蜜香或熟果味，滋味圓柔醇厚。\n"
        "Ｃ把採收已2至3天後柚子果肉挖出，新鮮柚肉去籽加入檸檬皮、茶葉、佛手柑混合均勻，扎實塞回空柚子，再用繩索綁緊，"
        "一次製茶需經過「九蒸九曬」階段，工時花費3個月左右時間。相傳喝了能潤喉止咳。",
        "options": ["選項如下", "1A、2B、3C", "1B、2C、3A", "1C、2A、3B"],
        "answer": "1B、2C、3A",
        "next": "q14"
    },
    "q14": {
        "messages": [
            "沒錯，你們很了解客家的特色茶葉呢，其實酸柑茶和柚子茶的製程基本一樣，但製作『酸柑茶』的『酸柑』則需要到農曆年左右才可採收，一年只生產一次。",

            ("小江：在菱潭街興創基地可以看到好多古早客家生活文化與新事物的結合，讓我有好大的收穫，"
             "雖然不是在傳統客家莊長大，但好像發現家裡也有一些客家的影子在，像是我家阿婆也會點「廳下火」呢！"),

            ("好想繼續認識更多的客家文化。鐘老、鐘老！還有其他客家相關景點嗎？")],
        "question": "鐘老：信仰也是客家文化中很重要的一環，那龍潭區的信仰中心在哪呢？",
        "options": ["# 龍元宮", "# 大天后宮", "# 三山國王廟"],
        "answer": "龍元宮",
        "next": "q15"
    },
    "q15": {
        "messages": [
            "沒錯，就是龍元宮，到了之後就先找到主要祭祀的神明吧。",

            ("龍元宮每年四月的「五穀爺文化季｣，以賽神豬、傳統樂曲表演等活動慶賀五穀爺誕辰，場面萬人空巷。"
             "而一年一度的元宵節則有「迎古董｣踩街嘉年華、財神爺發財母金遶境，在中秋節時，龍元宮也會舉辦慶祝活動，"
             "包括舞獅、遊戲活動更是在每逢過年節慶的時候會有歌仔戲、擲杯比賽等，吸引了大批遊客前來參與。")],
        "question": "Q：台灣民間奉祀神農大帝的神像外型，因行業別而有所不同，那龍元宮的神農大帝臉是什麼顏色的？",
        "options": ["# 紅色", "# 黑色", "# 綠色"],
        "answer": "紅色",
        "next": "q16"
    },
    "q16": {
        "messages": [
            "面部呈現為紅色的神農大帝，是農民為求五穀豐收，希望能夠時時豐收得以溫飽，人人臉色都如同祂那樣紅潤。\n面部呈現為黑色的神農大帝，是醫藥界為了紀念神農大帝因誤食毒草身中劇毒，導致全身發黑。\n面部呈現為綠色的神農大帝，則是意味神農早年嘗百草，而面有菜色。",

            "而客家族群對神農信仰的重視，主要是因客家人渡臺較晚，大多僅能在山區或偏遠地區進行農業開墾，因環境條件甚為艱難，故更需神農大帝的庇祐，以祈求開墾順利、五穀豐收，由於大多數客家人是以農為業，對五穀爺崇祀便特別虔誠。",
            ("Q：五穀爺在台灣有許多外型，以下哪些是龍元宮五穀爺的形象？")],
        "question": "請選擇龍元宮五穀爺的形象\n（答題格式）「 」、「 」、「 」",
        "options": ["A:頭角崢嶸", "B:文官氣派", "C:袒胸露背", "D:腰圍樹葉", "E:衣冠束帶", "F:赤手跣足", "G:手持稻穗"],
        "answer": "B、E",
        "next": "q17"
    },
    "q17": {
        "messages": [
            "台灣地區的神農神像造型很多，有頭角崢嶸、袒胸露背、腰圍樹葉、赤手跣足、手持稻穗之原始造型，也有儀表如莊稼漢、質樸親切的神貌。龍元宮供奉的神農大帝， 又稱為五穀爺，衣冠束帶，文官氣派與一般原始時代農民的神農像完全不同，是北部少見的例子。據說這樣特殊的形象與當地文風興盛有關。",

            "小江：「這裡除了供奉五穀爺以外還有好多其他的神明跟廳室，讓我們一起過去看看吧！」",

            ("Q：上圖為龍元宮的格局圖，請將各個位置的名稱和其功能做配對。"),
            ("位置名稱\n"
             "1. 廟埕\n2. 拜殿（拜亭）\n3. 前殿\n4. 龍虎門\n5. 正殿\n6. 後殿\n7. 鐘鼓樓\n8.廂廊\n"
             "位置功能\n")
        ],
        "question":
        "B廟埕是香客要入廟參拜前集合的場所，空間最寬敞，也是藝陣或童乩大展神通的地方。\n"
        "E是供信眾祭拜的地方，通常會擺放一個大香爐。\n"
        "G又叫做「三川殿」或「三川門」，是寺廟的第一殿，也是信眾初拜的位置。外觀華麗，裝飾最為繁複，是寺廟藝術表現的重點所在。\n"
        "A位在三川門的兩側，左龍右虎，與三川門合稱為「五門」，是信眾出入的通道，習慣上由龍門進入，由虎門出。\n"
        "D寺廟的主祀空間，是祀神的聖域，內部光線明亮，搭配著暗紅大理石神龕，氣氛顯得莊嚴肅穆。\n"
        "F是中軸上最後一進的殿宇，因為祀奉的是陪祀的神明，所以在建築的高度和進深上都比正殿來得小。\n"
        "C位於龍虎門之後，兩廂之上，分別為左（龍）鐘、右（虎）鼓。遇有重大祀典或貴賓入廟，就會鐘鼓齊鳴，表示敬迎之意。\n"
        "H位於寺廟的左右兩側，通常作為管理委員會的辦公所在，有時也作為陪祀神明的偏殿",
        "image_urls": ["https://i.imgur.com/QMpsG9d.png"],
        "options": ["（答題格式範例）：1-A、2-B、3-C、4-D、5-E、6-F、7-G、8-H"],
        "answer": "1-B、2-E、3-G、4-A、5-D、6-F、7-C、8-H",
        "next": "q18"
    },
    "q18": {
        "messages": [
            "現在的龍元宮為兩殿式建築，由烏樹林仕紳翁新統、翁新造，黃泥塘仕紳李養、黃樹勳、古望林等人發起，增建了前殿和後殿。次年，翁新統、翁新造與黃樹勳、鍾會宏等人再次發起募捐，進行後殿增高及左右走廊的建設。在戰後的1966年成立修建委員會，推選翁瑞川為主任委員，募得32萬餘元進行修復。目前看到的廟貌主要是1994年改建完成的，增設了天井和鐘鼓樓。自2010年起，廟方陸續改建了兩側廂房，拓寬了廟埕廣場，並在廟後增建了活動中心，以擴展空間，方便舉辦每年豐富多樣的廟會活動。",
            "Q：廟內的建築風格為兩殿式，正殿主祀是神農大帝，偏殿主祀是斗母元君，請分別寫出祂們左、右陪祀的神明。",
            "正殿主祀—神農大帝\n正殿陪祀（左）— 【甲】\n正殿陪祀（右）— 【乙】\n偏殿主祀—斗母元君 \n偏殿配祀 ( 左 )— 【丙】\n偏殿陪祀 ( 右 )—【丁】"],
        "question": "Q：請依序寫出神明陪祀名，（答題格式提示）：甲、乙、丙、丁",
        "options": ["選項：", "#天上聖母", "#文昌帝君", "#財神爺", "#註生娘娘"],
        "answer": "文昌帝君、天上聖母、財神爺、註生娘娘",
        "next": "q19"
    },
    "q19": {
        "messages": [
            "Q：龍元宮內的藻井是中國建築裡特有的天花板結構及裝飾手法，通常選在天花板最顯眼的位置，由四周不斷向中心懸挑內縮的斗拱，交織成網狀的傘蓋形頂棚，由下往上看，深邃如井，所以稱為「藻井」。"
        ],
        "question": "請找出「藻井」並拍照。",
        "options": [],
        "answer": "",
        "allow_image_upload": True,
        "next": "q20"
    },
    "q20": {
        "messages": [
            ("藻井最中心的部分是一個八角形或近似圓形的結構，稱為「頂心明鏡」。由於「頂心明鏡」上常繪有龍形圖案，故又被稱為「龍井」。"
             "藻井最初的功能是支撐天窗，後來演變為匠師們競技的場所，其結構也變得越來越複雜和華麗。"
             "根據藻井的外形和網目結構的不同，有八卦形、圓形、橢圓形、方形、六角形或內圓外八卦、內八卦外圓等形式。"),
            ("據說藻井的由來是這樣的：明太祖朱元璋為了躲避陳友諒的追兵，走投無路之際躲進一個破舊的山神廟供桌底下，以破舊的桌巾遮蔽自己，並默默祈求神明保佑。"
             "此時，山神變出一張完整的蜘蛛網，將朱元璋藏身的破桌巾縫隙緊緊網住。追兵趕到後，見四周無人且蜘蛛網完整，認為朱元璋不可能藏在此處，便沒有細查離開了，"
             "朱元璋因此得以保命。當朱元璋成為皇帝後，為感謝神明的保佑，便命建築工匠依照蜘蛛網的形狀在大殿室內建造出「藻井」，既作為幸運符，又表達對神恩的永遠感念。"
             "這雖然是一則未經證實的說法，但確實是一有趣的故事。\n"
             "Q：廟前的大廣場有天公爐，而「拜天公」對客家人來說是信仰中很重要的一環。"
             "下面哪些關於客家天公信仰的描述是正確的？")],
        "question": "A農曆除夕夜的前一晚子時以後，客家人在小年夜的習俗，會在門口設香案拜天公，感謝上天一年來的庇佑。\n"
        "B 拜天公，有分上界下界，上界拜素，下界拜葷\n"
        "C客家人在農曆初九拜天公，年初一時則祭天迎新年。",
        "options": [],
        "image_urls": ["https://i.imgur.com/j8ofL0T.png"],
        "answer": "A、B",
        "next": 'q21'
    },
    "q21": {
        "messages": [
            "閩南人農曆初九拜天公，客家人則在年三十時，會祭天以辭年，年初一時則祭天迎新年。除了神祇信仰，客家人最重視祖先崇拜，「拜阿公婆」乃是客家人認為最為重要的大事。因此一般祭拜時順序都是先祭祖，然後才是祭拜神明。",

            "小江：「你看你看，剛剛我抬頭發現屋頂上有用雙龍搶珠（ 龍與寶珠）、雙鳳、福祿壽三仙、天官賜福、祈求吉慶（ 旗球戢磬）、双獅戲球、北極仙翁、麻姑獻壽、人物戰馬、寶珠、寶塔、麒麟、龍首、飛鳳、雲彩、仙人、仙女、神獸、魚化龍及其他代表吉祥的動物、人物山水、花草等等，用五顏六色的塑膠片或是彩色玻璃片所製作的交趾陶裝飾。」",

            ("Q：龍元宮屋頂特色最明顯的特徵就是屋頂正脊尾端突出且往上揚，垂脊頂住正脊，形狀有如燕子的尾巴一樣，一般常見於廟宇，"
             "但也有出現於宅第上，若身份為官宦、富貴人家、功名及第者，通常也會於宅第上裝飾燕尾，這是一種榮耀的象徵。"
             "請問這種建築特色稱為什麼？")],
        "question": "請選擇建築特色名稱",
        "options": ["A:燕尾", "B:馬背", "C:瓦鎮"],
        "image_urls": ["https://i.imgur.com/soyj9V7.png"],
        "answer": "A",
        "next": 'q22'
    },
    "q22": {
        "messages": [
            "在臺灣的民間傳說中，燕尾脊只能由官員或中舉人家族使用，閩南地區也有類似的說法。許多臺灣的合院民宅會在正身屋脊上設置燕尾脊，代表家族的祖祠，尤其在客家家族中更為常見。雖然燕尾脊象徵尊貴，但有時宗祠或廟宇擔心翹起的燕尾脊會沖犯民宅，會在外加一道馬背脊，形成特殊的屋頂造型。\n\n燕尾脊指的是屋頂正脊兩端向上翹起，如燕子的尾巴。這種設計常見於官宅或廟宇，正脊成曲線向上揚起，尾端分叉成兩支，垂脊則向上支撐正脊，給人良好的印象，是中國南方特有的建築形式，在臺灣尤為盛行。燕尾脊、馬背脊和瓦鎮是台灣漢人古厝屋頂的三大特徵。",

            "小江：「謝謝你們今天陪伴我一起尋找客家的記憶，台灣客家族群的自我隱形化行為是一個普遍為客家人所認知的公共問題，構成客家隱形的五大因素是：（一）弱勢族群說；（二）文化融合說；（三） 語言流失說；（四）歷史包袱說；（五）自利動機說，這些原因確實存在於現實的客家社群當中。就像我雖然是來自客家家庭，但卻因為長輩都沒有提及，甚至只跟我說「國語」、「台語」才讓我不知道自己的客家身份。現在政府也積極在推動傳統台文的復甦，希望能讓更多人認識客家語言及文化的美，和讓多元的文化面貌在台灣這個小島上兼容並蓄。希望有更多客家青年願意用自信的態度面對客家的身分，也期待能讓更多民眾看見客家不只有小氣的一面。」",

            "小江：「打幫你兜，亻厓正做得完成今晡日个旅行，有閒正來尞！」"
        ],
        "question": "恭喜你完成了所有關卡！\n請輸入 '開始' 重新開始遊戲。",
        "options": [],
        "answer": "",
        "next": "finish"
    },
    "finish": None
}

user_data = {}


@ app.route("/", methods=['POST'])
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


@ handler.add(MessageEvent, message=(TextMessage, ImageMessage))
def handle_message(event):
    message_type = event.message.type
    user_id = event.source.user_id
    reply_token = event.reply_token

    if message_type == 'text':
        message = event.message.text.strip()
        # Check user progress or start the story
        if message == "開始":
            start_story(user_id, reply_token)
        else:
            user_progress = get_user_progress(user_id)
            if (message == '關於客家'):
                send_message(
                    reply_token, "https://www.hakka.gov.tw/index.html")
            elif (message == '地點提示'):
                send_message(
                    reply_token, "https://www.google.com/maps/d/edit?mid=1EDXW7ousVBIDaB9DfDiA1q-A_slZiQ8&ll=24.90371743628607%2C121.2071314861216&z=12")
            elif (message == '心得回饋'):
                send_message(
                    reply_token, "https://docs.google.com/forms/d/e/1FAIpQLScmuH_Kdn4W8RhwFC3o5PWUSYBrkjbhEkhAjQ1XpCpKcob0uw/viewform?usp=sf_link")
            elif (message == 'Hello'):
                send_message(
                    reply_token, ("早期自大陸渡海來台的漢人移民，多來自閩粵兩地，閩籍居民泰半為漳、泉二府人氏，"
                                  "粵籍則為嘉應州及潮州、惠州的客家人，在清朝時，漳、泉、客三族人群涇渭分明，但今天，"
                                  "除了桃竹苗和美濃等地客家文化還非常突顯，其他地區的客族已與閩南族群融合，成為「福佬客」。"
                                  "有許多年輕一代的客籍青年都只說閩南語和國語，更甚至不知道自己是客籍的人。\n\n住在員林的江河鄰（小江）"
                                  "是還在就讀小學六年級的學生，就在一次跟著爺爺去祭祖時偶然發現爺爺跟祖先說話時用的不是國語，"
                                  "也不是在國小裡學到的閩南語，因此感到很好奇。後來一問之下他才知道原來那是客家話，而他們家其實是客籍家族，"
                                  "所以他身上也流淌著客家的血脈。然而他們家族已經深受周圍環境引響而導致福佬化，平時都說國語和閩南語，"
                                  "已經漸漸忘記身為客家人的事情。\n\n因此小江決定來到客家人聚集的大市「桃園」，來尋找自己的客家認同感，"
                                  "並且更加了解有關客家人的文化和歷史。就在這時他遇到了鍾肇政，並決定從這裡開始追尋客家的記憶。\n"
                                  "就讓我們一起跟隨小江一起開始這趟旅程吧！\n\n請輸入 '開始' 開始遊戲。"))

            if user_progress:
                current_question = story.get(user_progress)
                if message == current_question['answer'] or (message == 'P' and DEBUG):
                    next_question = story.get(current_question['next'])
                    send_question(user_id, reply_token, next_question)
                    set_user_progress(user_id, current_question['next'])
                else:
                    send_message(reply_token, "回答錯誤，請再試一次。")
            else:
                send_message(reply_token, ("早期自大陸渡海來台的漢人移民，多來自閩粵兩地，閩籍居民泰半為漳、泉二府人氏，"
                                           "粵籍則為嘉應州及潮州、惠州的客家人，在清朝時，漳、泉、客三族人群涇渭分明，但今天，"
                                           "除了桃竹苗和美濃等地客家文化還非常突顯，其他地區的客族已與閩南族群融合，成為「福佬客」。"
                                           "有許多年輕一代的客籍青年都只說閩南語和國語，更甚至不知道自己是客籍的人。\n\n住在員林的江河鄰（小江）"
                                           "是還在就讀小學六年級的學生，就在一次跟著爺爺去祭祖時偶然發現爺爺跟祖先說話時用的不是國語，"
                                           "也不是在國小裡學到的閩南語，因此感到很好奇。後來一問之下他才知道原來那是客家話，而他們家其實是客籍家族，"
                                           "所以他身上也流淌著客家的血脈。然而他們家族已經深受周圍環境引響而導致福佬化，平時都說國語和閩南語，"
                                           "已經漸漸忘記身為客家人的事情。\n\n因此小江決定來到客家人聚集的大市「桃園」，來尋找自己的客家認同感，"
                                           "並且更加了解有關客家人的文化和歷史。就在這時他遇到了鍾肇政，並決定從這裡開始追尋客家的記憶。\n"
                                           "就讓我們一起跟隨小江一起開始這趟旅程吧！\n\n請輸入 '開始' 開始遊戲。"))

    elif message_type == 'image':
        user_progress = get_user_progress(user_id)
        if user_progress:
            current_question = story.get(user_progress)
            if allow_image_upload(current_question):  # 檢查當前問題是否允許圖像上傳作為答案
                next_question = story.get(current_question['next'])
                send_question(user_id, reply_token, next_question)
                set_user_progress(user_id, current_question['next'])
            else:
                send_message(reply_token, "這不是一個上傳照片即可回答正確的問題。")


def allow_image_upload(question):
    # 添加邏輯來判斷哪些問題允許用戶上傳圖片作為正確答案
    return 'allow_image_upload' in question and question['allow_image_upload']


def start_story(user_id, reply_token):
    initial_question = story['start']
    set_user_progress(user_id, 'start')
    send_question(user_id, reply_token, initial_question)


def send_messages_in_batches(user_id, reply_token, messages, batch_size=5):
    # 计算消息分批次数
    batch_count = (len(messages) + batch_size - 1) // batch_size
    for i in range(batch_count):
        batch = messages[i * batch_size:(i + 1) * batch_size]
        try:
            if i == 0:
                # 使用LINE Bot API发送消息
                line_bot_api.reply_message(reply_token, batch)
            else:
                # 使用LINE Bot API发送消息
                line_bot_api.push_message(user_id, batch)
        except LineBotApiError as e:
            # 输出错误信息
            print(
                f"\n\n\nError sending batch {i + 1}/{batch_count}: {e.message}, request_id: {e.request_id}\n\n\n")


def send_question(user_id, reply_token, question):
    if question is not None:
        messages = []
        if 'messages' in question:
            for msg in question['messages']:
                messages.append(TextSendMessage(text=msg))
                if 'image_urls' in question and len(question['image_urls']) > 0:
                    image_url = question['image_urls'].pop(0)
                    messages.append(ImageSendMessage(
                        original_content_url=image_url,
                        preview_image_url=image_url
                    ))
        options_text = "\n".join(
            question['options']) if question['options'] else ""
        full_message = f"{question['question']}\n{options_text}"
        # 添加转义处理特殊字符
        messages.append(TextSendMessage(text=full_message))

        # 使用批量消息发送
        send_messages_in_batches(user_id, reply_token, messages, batch_size=5)
    else:
        # 处理完成所有关卡的情况
        line_bot_api.reply_message(
            reply_token, TextSendMessage(text="恭喜你完成了所有關卡！請輸入 '開始' 重新開始遊戲。")
        )

# 其他函数如前所述保留不变


def send_message(reply_token, message):
    line_bot_api.reply_message(reply_token, TextSendMessage(text=message))


def get_user_progress(user_id):
    if user_id not in user_data:
        return None
    return user_data[user_id]


def set_user_progress(user_id, question_key):
    global user_data
    user_data[user_id] = question_key


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)
