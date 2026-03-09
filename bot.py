import requests
import os
import json
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters


import os
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")


TEXTS = {
    "az": {
        "welcome": "Salam! PulseBot-a xos geldin. Menyu:",
        "fetching": "Axtarilir...",
        "no_news": "Xeber tapilmadi.",
        "lang_menu": "Dil sec:",
        "lang_set": "Azerbaycanca secildi!",
        "weather_ask": "Seherin adini yaz:",
        "crypto_title": "Kripto Qiymetleri",
        "currency_title": "Valyuta Meznesi (1 USD)",
        "digest_title": "Gunun Xulasesi",
        "trending_title": "Trend Xeberler",
        "history_title": "Bu gun tarixde",
        "quiz_title": "Gunun Viktorinasi",
        "saved_title": "Saxlanmis Xeberler",
        "no_saved": "Hec bir xeber saxlanmayib.",
        "saved_ok": "Xeber saxlanildi!",
        "sentiment_pos": "Musbet xeber",
        "sentiment_neg": "Menfi xeber",
        "sentiment_neu": "Neytral xeber",
        "ask_ai": "Bu xeber haqqinda sual ver:",
        "keyword_ask": "Izlemek istediyiniz acarsoz yazin:",
        "keyword_set": "Acarsoz qeydiyye alindi!",
        "keywords_title": "Izlenen Acarsozler",
        "no_keywords": "Hec bir acarsoz yoxdur.",
        "reaction_done": "Reaksiya qeyd edildi!",
        "vacation_on": "Bildirislər söndürüldü (məzuniyyət rejimi).",
        "vacation_off": "Bildirişlər yenidən aktivdir!",
        "profile_title": "Istifadeci Profili",
        "leaderboard_title": "Liderlik Cedveli",
        "topics": {
            "tech": "Tech/AI",
            "business": "Biznes",
            "sports": "Idman",
            "world": "Dunya",
            "health": "Sagliq",
            "science": "Elm",
            "crypto": "Kripto"
        },
        "menu": {
            "news": "Xeberler",
            "digest": "Gunun Xulasesi",
            "trending": "Trend",
            "weather": "Hava",
            "crypto": "Kripto",
            "currency": "Valyuta",
            "saved": "Saxlanmis",
            "history": "Tarixde Bu Gun",
            "quiz": "Vikatorina",
            "language": "Dil",
            "keywords": "Acarsoz Izle",
            "markets": "Bazar Qiymetleri",
            "profile": "Profil",
            "leaderboard": "Liderler",
            "vacation": "Mezuniyyet Rejimi"
        }
    },
    "en": {
        "welcome": "Hello! Welcome to PulseBot. Menu:",
        "fetching": "Fetching...",
        "no_news": "No news found.",
        "lang_menu": "Choose language:",
        "lang_set": "English selected!",
        "weather_ask": "Type city name:",
        "crypto_title": "Crypto Prices",
        "currency_title": "Exchange Rates (1 USD)",
        "digest_title": "Daily Digest",
        "trending_title": "Trending News",
        "history_title": "Today in History",
        "quiz_title": "Daily Quiz",
        "saved_title": "Saved News",
        "no_saved": "No saved news.",
        "saved_ok": "News saved!",
        "sentiment_pos": "Positive news",
        "sentiment_neg": "Negative news",
        "sentiment_neu": "Neutral news",
        "ask_ai": "Ask a question about this news:",
        "keyword_ask": "Type a keyword to track:",
        "keyword_set": "Keyword saved!",
        "keywords_title": "Tracked Keywords",
        "no_keywords": "No keywords yet.",
        "reaction_done": "Reaction recorded!",
        "vacation_on": "Notifications paused (vacation mode).",
        "vacation_off": "Notifications are active again!",
        "profile_title": "User Profile",
        "leaderboard_title": "Leaderboard",
        "topics": {
            "tech": "Tech/AI",
            "business": "Business",
            "sports": "Sports",
            "world": "World",
            "health": "Health",
            "science": "Science",
            "crypto": "Crypto"
        },
        "menu": {
            "news": "News",
            "digest": "Daily Digest",
            "trending": "Trending",
            "weather": "Weather",
            "crypto": "Crypto",
            "currency": "Currency",
            "saved": "Saved",
            "history": "Today in History",
            "quiz": "Quiz",
            "language": "Language",
            "keywords": "Track Keywords",
            "markets": "Markets",
            "profile": "Profile",
            "leaderboard": "Leaderboard",
            "vacation": "Vacation Mode"
        }
    },
    "ru": {
        "welcome": "Privet! Dobro pozhalovat v PulseBot. Menyu:",
        "fetching": "Ishu...",
        "no_news": "Novosti ne naydeni.",
        "lang_menu": "Viberite yazik:",
        "lang_set": "Russkiy vibran!",
        "weather_ask": "Vvedite nazvanie goroda:",
        "crypto_title": "Tseni na kripto",
        "currency_title": "Kursi valyut (1 USD)",
        "digest_title": "Daydzhest dnya",
        "trending_title": "Trendovie novosti",
        "history_title": "V etot den v istorii",
        "quiz_title": "Viktorina dnya",
        "saved_title": "Sohranenie novosti",
        "no_saved": "Net sohranennih novostey.",
        "saved_ok": "Novost sohranena!",
        "sentiment_pos": "Pozitivnaya novost",
        "sentiment_neg": "Negativnaya novost",
        "sentiment_neu": "Neytralnaya novost",
        "ask_ai": "Zadayte vopros ob etoy novosti:",
        "keyword_ask": "Vvedite klyuchevoe slovo:",
        "keyword_set": "Klyuchevoe slovo sohraneno!",
        "keywords_title": "Otslezhivaemie slova",
        "no_keywords": "Net klyuchevikh slov.",
        "reaction_done": "Reaktsiya zapisana!",
        "vacation_on": "Uvedomleniya otklyucheni.",
        "vacation_off": "Uvedomleniya snova aktivni!",
        "profile_title": "Profil polzovatelya",
        "leaderboard_title": "Tablitsa liderov",
        "topics": {
            "tech": "Tex/II",
            "business": "Biznes",
            "sports": "Sport",
            "world": "Mir",
            "health": "Zdorovie",
            "science": "Nauka",
            "crypto": "Kripto"
        },
        "menu": {
            "news": "Novosti",
            "digest": "Daydzhest",
            "trending": "Trendi",
            "weather": "Pogoda",
            "crypto": "Kripto",
            "currency": "Valyuta",
            "saved": "Sohranenie",
            "history": "V etot den",
            "quiz": "Viktorina",
            "language": "Yazik",
            "keywords": "Klyuch slova",
            "markets": "Rinki",
            "profile": "Profil",
            "leaderboard": "Lideri",
            "vacation": "Otpusk"
        }
    },
    "tr": {
        "welcome": "Merhaba! PulseBot'a hosgeldin. Menu:",
        "fetching": "Aranıyor...",
        "no_news": "Haber bulunamadi.",
        "lang_menu": "Dil sec:",
        "lang_set": "Turkce secildi!",
        "weather_ask": "Sehir adini yaz:",
        "crypto_title": "Kripto Fiyatlari",
        "currency_title": "Doviz Kurlari (1 USD)",
        "digest_title": "Gunun Ozeti",
        "trending_title": "Trend Haberler",
        "history_title": "Tarihte Bugun",
        "quiz_title": "Gunun Bilgi Yarismasi",
        "saved_title": "Kaydedilen Haberler",
        "no_saved": "Kaydedilmis haber yok.",
        "saved_ok": "Haber kaydedildi!",
        "sentiment_pos": "Olumlu haber",
        "sentiment_neg": "Olumsuz haber",
        "sentiment_neu": "Tarafsiz haber",
        "ask_ai": "Bu haber hakkinda soru sor:",
        "keyword_ask": "Takip etmek istedigin kelimeyi yaz:",
        "keyword_set": "Anahtar kelime kaydedildi!",
        "keywords_title": "Takip Edilen Kelimeler",
        "no_keywords": "Anahtar kelime yok.",
        "reaction_done": "Reaksiyon kaydedildi!",
        "vacation_on": "Bildirimler durduruldu.",
        "vacation_off": "Bildirimler tekrar aktif!",
        "profile_title": "Kullanici Profili",
        "leaderboard_title": "Liderlik Tablosu",
        "topics": {
            "tech": "Teknoloji/AI",
            "business": "Is",
            "sports": "Spor",
            "world": "Dunya",
            "health": "Saglik",
            "science": "Bilim",
            "crypto": "Kripto"
        },
        "menu": {
            "news": "Haberler",
            "digest": "Gunun Ozeti",
            "trending": "Trend",
            "weather": "Hava",
            "crypto": "Kripto",
            "currency": "Doviz",
            "saved": "Kaydedilenler",
            "history": "Tarihte Bugun",
            "quiz": "Bilgi Yarismasi",
            "language": "Dil",
            "keywords": "Kelime Takip",
            "markets": "Piyasalar",
            "profile": "Profil",
            "leaderboard": "Liderler",
            "vacation": "Tatil Modu"
        }
    },
    "de": {
        "welcome": "Hallo! Willkommen bei PulseBot. Menue:",
        "fetching": "Suche...",
        "no_news": "Keine Nachrichten.",
        "lang_menu": "Sprache waehlen:",
        "lang_set": "Deutsch ausgewaehlt!",
        "weather_ask": "Stadtname eingeben:",
        "crypto_title": "Krypto Preise",
        "currency_title": "Wechselkurse (1 USD)",
        "digest_title": "Tagesrueckblick",
        "trending_title": "Trending News",
        "history_title": "Heute in Geschichte",
        "quiz_title": "Tagesquiz",
        "saved_title": "Gespeicherte Nachrichten",
        "no_saved": "Keine gespeicherten.",
        "saved_ok": "Gespeichert!",
        "sentiment_pos": "Positiv",
        "sentiment_neg": "Negativ",
        "sentiment_neu": "Neutral",
        "ask_ai": "Frage stellen:",
        "keyword_ask": "Stichwort eingeben:",
        "keyword_set": "Stichwort gespeichert!",
        "keywords_title": "Verfolgte Stichwoerter",
        "no_keywords": "Keine Stichwoerter.",
        "reaction_done": "Reaktion gespeichert!",
        "vacation_on": "Benachrichtigungen pausiert.",
        "vacation_off": "Benachrichtigungen aktiv!",
        "profile_title": "Benutzerprofil",
        "leaderboard_title": "Bestenliste",
        "topics": {
            "tech": "Tech/KI",
            "business": "Wirtschaft",
            "sports": "Sport",
            "world": "Welt",
            "health": "Gesundheit",
            "science": "Wissenschaft",
            "crypto": "Krypto"
        },
        "menu": {
            "news": "Nachrichten",
            "digest": "Tagesrueckblick",
            "trending": "Trends",
            "weather": "Wetter",
            "crypto": "Krypto",
            "currency": "Waehrung",
            "saved": "Gespeichert",
            "history": "Heute in Geschichte",
            "quiz": "Quiz",
            "language": "Sprache",
            "keywords": "Stichwoerter",
            "markets": "Maerkte",
            "profile": "Profil",
            "leaderboard": "Bestenliste",
            "vacation": "Urlaubsmodus"
        }
    }
}

KEYWORDS = {
    "tech": "artificial intelligence technology",
    "business": "business finance economy",
    "sports": "sports football",
    "world": "world news politics",
    "health": "health medicine",
    "science": "science research",
    "crypto": "cryptocurrency bitcoin"
}

user_langs = {}
user_saved = {}
user_states = {}
last_articles = {}
user_keywords = {}
user_vacation = {}
user_quiz_scores = {}
user_reactions = {}
user_joined = {}

def get_lang(uid, tg_lang=None):
    if uid in user_langs:
        return user_langs[uid]
    if tg_lang and tg_lang[:2] in TEXTS:
        return tg_lang[:2]
    return "en"

def get_main_kb(lang):
    m = TEXTS[lang]["menu"]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📰 " + m["news"], callback_data="menu_news"),
         InlineKeyboardButton("📋 " + m["digest"], callback_data="menu_digest")],
        [InlineKeyboardButton("🔥 " + m["trending"], callback_data="menu_trending"),
         InlineKeyboardButton("🌤️ " + m["weather"], callback_data="menu_weather")],
        [InlineKeyboardButton("₿ " + m["crypto"], callback_data="menu_crypto"),
         InlineKeyboardButton("💵 " + m["currency"], callback_data="menu_currency")],
        [InlineKeyboardButton("🔖 " + m["saved"], callback_data="menu_saved"),
         InlineKeyboardButton("📅 " + m["history"], callback_data="menu_history")],
        [InlineKeyboardButton("🎮 " + m["quiz"], callback_data="menu_quiz"),
         InlineKeyboardButton("📈 " + m["markets"], callback_data="menu_markets")],
        [InlineKeyboardButton("🔍 " + m["keywords"], callback_data="menu_keywords"),
         InlineKeyboardButton("👤 " + m["profile"], callback_data="menu_profile")],
        [InlineKeyboardButton("🏆 " + m["leaderboard"], callback_data="menu_leaderboard"),
         InlineKeyboardButton("😴 " + m["vacation"], callback_data="menu_vacation")],
        [InlineKeyboardButton("🌍 " + m["language"], callback_data="lang_menu")]
    ])

def get_topics_kb(lang):
    t = TEXTS[lang]["topics"]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🤖 " + t["tech"], callback_data="topic_tech"),
         InlineKeyboardButton("💰 " + t["business"], callback_data="topic_business")],
        [InlineKeyboardButton("⚽ " + t["sports"], callback_data="topic_sports"),
         InlineKeyboardButton("🌍 " + t["world"], callback_data="topic_world")],
        [InlineKeyboardButton("❤️ " + t["health"], callback_data="topic_health"),
         InlineKeyboardButton("🔬 " + t["science"], callback_data="topic_science")],
        [InlineKeyboardButton("₿ " + t["crypto"], callback_data="topic_crypto")],
        [InlineKeyboardButton("🔙 Geri", callback_data="menu_back")]
    ])

def get_news_kb(lang):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔖 Saxla", callback_data="save_news"),
         InlineKeyboardButton("🤖 AI Sual", callback_data="ask_ai")],
        [InlineKeyboardButton("👍", callback_data="react_like"),
         InlineKeyboardButton("👎", callback_data="react_dislike"),
         InlineKeyboardButton("🔥", callback_data="react_fire")],
        [InlineKeyboardButton("🔙 Geri", callback_data="menu_news")]
    ])

def fetch_news(topic, count=3):
    try:
        r = requests.get("https://newsapi.org/v2/everything",
                         params={"q": KEYWORDS[topic], "pageSize": count, "sortBy": "publishedAt", "apiKey": NEWS_API_KEY},
                         timeout=10)
        return r.json().get("articles", [])
    except Exception:
        return []

def fetch_news_keyword(keyword, count=3):
    try:
        r = requests.get("https://newsapi.org/v2/everything",
                         params={"q": keyword, "pageSize": count, "sortBy": "publishedAt", "apiKey": NEWS_API_KEY},
                         timeout=10)
        return r.json().get("articles", [])
    except Exception:
        return []

def fetch_trending():
    try:
        r = requests.get("https://newsapi.org/v2/top-headlines",
                         params={"language": "en", "pageSize": 5, "apiKey": NEWS_API_KEY},
                         timeout=10)
        return r.json().get("articles", [])
    except Exception:
        return []

def fetch_weather(city):
    try:
        r = requests.get("https://api.openweathermap.org/data/2.5/weather",
                         params={"q": city, "appid": WEATHER_API_KEY, "units": "metric"},
                         timeout=10)
        d = r.json()
        if d.get("cod") != 200:
            return None
        return {
            "city": d["name"],
            "temp": round(d["main"]["temp"]),
            "feels": round(d["main"]["feels_like"]),
            "desc": d["weather"][0]["description"],
            "humidity": d["main"]["humidity"],
            "wind": d["wind"]["speed"]
        }
    except Exception:
        return None

def fetch_crypto():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price",
                         params={"ids": "bitcoin,ethereum,solana,binancecoin",
                                 "vs_currencies": "usd",
                                 "include_24hr_change": "true"},
                         timeout=10)
        return r.json()
    except Exception:
        return {}

def fetch_currency():
    try:
        r = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10)
        rates = r.json().get("rates", {})
        return {
            "EUR": round(rates.get("EUR", 0), 4),
            "GBP": round(rates.get("GBP", 0), 4),
            "AZN": round(rates.get("AZN", 0), 4),
            "TRY": round(rates.get("TRY", 0), 4),
            "RUB": round(rates.get("RUB", 0), 4)
        }
    except Exception:
        return {}

def fetch_markets():
    try:
        gold = requests.get("https://api.metals.live/v1/spot/gold", timeout=10).json()
        gold_price = gold[0].get("price", "N/A") if isinstance(gold, list) else "N/A"
    except Exception:
        gold_price = "N/A"
    try:
        oil = requests.get("https://api.api-ninjas.com/v1/commodityprice?name=crude_oil", timeout=10)
        oil_price = "N/A"
    except Exception:
        oil_price = "N/A"
    return {"gold": gold_price, "oil": oil_price}

def groq_ask(prompt, lang):
    lang_names = {"az": "Azerbaijani", "en": "English", "ru": "Russian", "tr": "Turkish", "de": "German"}
    try:
        headers = {"Authorization": "Bearer " + GROQ_API_KEY, "Content-Type": "application/json"}
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": "Respond ONLY in " + lang_names[lang] + ". " + prompt}]
        }
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                          headers=headers, json=data, timeout=15)
        return r.json()["choices"][0]["message"]["content"]
    except Exception:
        return "..."

def summarize(text, lang):
    return groq_ask("Summarize this news in exactly 2 sentences:\n\n" + text, lang)

def analyze_sentiment(text, lang):
    result = groq_ask("Analyze sentiment. Reply with only one word POSITIVE NEGATIVE or NEUTRAL:\n\n" + text, lang)
    if "POSITIVE" in result.upper():
        return TEXTS[lang]["sentiment_pos"]
    elif "NEGATIVE" in result.upper():
        return TEXTS[lang]["sentiment_neg"]
    return TEXTS[lang]["sentiment_neu"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = get_lang(user.id, user.language_code)
    if user.id not in user_joined:
        user_joined[user.id] = datetime.now().strftime("%Y-%m-%d")
    await update.message.reply_text(TEXTS[lang]["welcome"], reply_markup=get_main_kb(lang))

async def btn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    uid = q.from_user.id
    lang = get_lang(uid)
    t = TEXTS[lang]
    try:
        await q.answer()
    except Exception:
        pass
    data = q.data

    if data == "menu_back":
        try:
            await q.edit_message_text(t["welcome"], reply_markup=get_main_kb(lang))
        except Exception:
            pass

    elif data == "lang_menu":
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🇦🇿 Azerbaycanca", callback_data="sl_az"),
             InlineKeyboardButton("🇬🇧 English", callback_data="sl_en")],
            [InlineKeyboardButton("🇷🇺 Russki", callback_data="sl_ru"),
             InlineKeyboardButton("🇹🇷 Turkce", callback_data="sl_tr")],
            [InlineKeyboardButton("🇩🇪 Deutsch", callback_data="sl_de")],
            [InlineKeyboardButton("🔙 Geri", callback_data="menu_back")]
        ])
        try:
            await q.edit_message_text(t["lang_menu"], reply_markup=kb)
        except Exception:
            pass

    elif data.startswith("sl_"):
        nl = data[3:]
        user_langs[uid] = nl
        nt = TEXTS[nl]
        try:
            await q.edit_message_text(nt["lang_set"] + "\n\n" + nt["welcome"], reply_markup=get_main_kb(nl))
        except Exception:
            pass

    elif data == "menu_news":
        try:
            await q.edit_message_text(t["welcome"], reply_markup=get_topics_kb(lang))
        except Exception:
            pass

    elif data.startswith("topic_"):
        topic = data[6:]
        try:
            await q.edit_message_text(t["fetching"])
        except Exception:
            pass
        articles = fetch_news(topic)
        if not articles:
            try:
                await q.edit_message_text(t["no_news"], reply_markup=get_main_kb(lang))
            except Exception:
                pass
            return
        last_articles[uid] = articles
        result = ""
        for i, a in enumerate(articles, 1):
            title = a.get("title", "")
            desc = a.get("description", "") or title
            url = a.get("url", "")
            summary = summarize(desc, lang)
            sentiment = analyze_sentiment(desc, lang)
            result += str(i) + ". " + title + "\n" + sentiment + "\n" + summary + "\n" + url + "\n\n"
        try:
            await q.edit_message_text(result, reply_markup=get_news_kb(lang), disable_web_page_preview=True)
        except Exception:
            pass

    elif data == "save_news":
        if uid in last_articles:
            if uid not in user_saved:
                user_saved[uid] = []
            user_saved[uid].extend(last_articles[uid])
        try:
            await q.answer(t["saved_ok"], show_alert=True)
        except Exception:
            pass

    elif data.startswith("react_"):
        reaction = data[6:]
        if uid not in user_reactions:
            user_reactions[uid] = []
        user_reactions[uid].append(reaction)
        if uid not in user_quiz_scores:
            user_quiz_scores[uid] = 0
        user_quiz_scores[uid] += 1
        try:
            await q.answer(t["reaction_done"], show_alert=False)
        except Exception:
            pass

    elif data == "ask_ai":
        user_states[uid] = "waiting_ai_question"
        try:
            await q.edit_message_text(t["ask_ai"])
        except Exception:
            pass

    elif data == "menu_saved":
        saved = user_saved.get(uid, [])
        if not saved:
            try:
                await q.edit_message_text(t["no_saved"], reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Geri", callback_data="menu_back")]]))
            except Exception:
                pass
            return
        result = t["saved_title"] + "\n\n"
        for i, a in enumerate(saved[-5:], 1):
            result += str(i) + ". " + a.get("title", "") + "\n" + a.get("url", "") + "\n\n"
        try:
            await q.edit_message_text(result, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Geri", callback_data="menu_back")]]), disable_web_page_preview=True)
        except Exception:
            pass

    elif data == "menu_digest":
        try:
            await q.edit_message_text(t["fetching"])
        except Exception:
            pass
        articles = fetch_news("world", 5)
        if not articles:
            try:
                await q.edit_message_text(t["no_news"], reply_markup=get_main_kb(lang))
            except Exception:
                pass
            return
        result = t["digest_title"] + "\n\n"
        for i, a in enumerate(articles, 1):
            title = a.get("title", "")
            desc = a.get("description", "") or title
            result += str(i) + ". " + title + "\n" + summarize(desc, lang) + "\n\n"
        try:
            await q.edit_message_text(result, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Geri", callback_data="menu_back")]]))
        except Exception:
            pass

    elif data == "menu_trending":
        try:
            await q.edit_message_text(t["fetching"])
        except Exception:
            pass
        articles = fetch_trending()
        if not articles:
            try:
                await q.edit_message_text(t["no_news"], reply_markup=get_main_kb(lang))
            except Exception:
                pass
            return
        result = t["trending_title"] + "\n\n"
        for i, a in enumerate(articles, 1):
            title = a.get("title", "")
            desc = a.get("description", "") or title
            result += str(i) + ". " + title + "\n" + summarize(desc, lang) + "\n\n"
        try:
            await q.edit_message_text(result, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Geri", callback_data="menu_back")]]))
        except Exception:
            pass

    elif data == "menu_weather":
        user_states[uid] = "waiting_city"
        try:
            await q.edit_message_text(t["weather_ask"])
        except Exception:
            pass

    elif data == "menu_crypto":
        try:
            await q.edit_message_text(t["fetching"])
        except Exception:
            pass
        crypto = fetch_crypto()
        if not crypto:
            try:
                await q.edit_message_text("Xeta", reply_markup=get_main_kb(lang))
            except Exception:
                pass
            return
        result = t["crypto_title"] + "\n\n"
        names = {"bitcoin": "Bitcoin", "ethereum": "Ethereum", "solana": "Solana", "binancecoin": "BNB"}
        for coin, info in crypto.items():
            price = info.get("usd", 0)
            change = info.get("usd_24h_change", 0)
            arrow = "up" if change > 0 else "down"
            result += names.get(coin, coin) + ": $" + str(round(price, 2)) + " " + arrow + " " + str(round(change, 2)) + "%\n"
        try:
            await q.edit_message_text(result, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Geri", callback_data="menu_back")]]))
        except Exception:
            pass

    elif data == "menu_currency":
        try:
            await q.edit_message_text(t["fetching"])
        except Exception:
            pass
        rates = fetch_currency()
        if not rates:
            try:
                await q.edit_message_text("Xeta", reply_markup=get_main_kb(lang))
            except Exception:
                pass
            return
        result = t["currency_title"] + "\n\n"
        result += "AZN: " + str(rates.get("AZN", "")) + "\n"
        result += "EUR: " + str(rates.get("EUR", "")) + "\n"
        result += "GBP: " + str(rates.get("GBP", "")) + "\n"
        result += "TRY: " + str(rates.get("TRY", "")) + "\n"
        result += "RUB: " + str(rates.get("RUB", "")) + "\n"
        try:
            await q.edit_message_text(result, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Geri", callback_data="menu_back")]]))
        except Exception:
            pass

    elif data == "menu_markets":
        try:
            await q.edit_message_text(t["fetching"])
        except Exception:
            pass
        crypto = fetch_crypto()
        result = "📈 " + t["menu"]["markets"] + "\n\n"
        result += "KRIPTO:\n"
        names = {"bitcoin": "Bitcoin", "ethereum": "Ethereum", "solana": "Solana", "binancecoin": "BNB"}
        for coin, info in crypto.items():
            price = info.get("usd", 0)
            change = info.get("usd_24h_change", 0)
            arrow = "up" if change > 0 else "down"
            result += names.get(coin, coin) + ": $" + str(round(price, 2)) + " " + arrow + "\n"
        rates = fetch_currency()
        result += "\nVALYUTA (1 USD):\n"
        result += "AZN: " + str(rates.get("AZN", "")) + "\n"
        result += "EUR: " + str(rates.get("EUR", "")) + "\n"
        result += "TRY: " + str(rates.get("TRY", "")) + "\n"
        try:
            await q.edit_message_text(result, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Geri", callback_data="menu_back")]]))
        except Exception:
            pass

    elif data == "menu_history":
        try:
            await q.edit_message_text(t["fetching"])
        except Exception:
            pass
        today = datetime.now()
        prompt = "Tell me 3 interesting historical events that happened on " + today.strftime("%B %d") + " in history. One sentence each."
        result = t["history_title"] + "\n\n" + groq_ask(prompt, lang)
        try:
            await q.edit_message_text(result, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Geri", callback_data="menu_back")]]))
        except Exception:
            pass

    elif data == "menu_quiz":
        try:
            await q.edit_message_text(t["fetching"])
        except Exception:
            pass
        prompt = "Create 1 multiple choice quiz question about world news or general knowledge. Format: Question, then A) B) C) D), then ANSWER: X"
        result = t["quiz_title"] + "\n\n" + groq_ask(prompt, lang)
        if uid not in user_quiz_scores:
            user_quiz_scores[uid] = 0
        user_quiz_scores[uid] += 1
        try:
            await q.edit_message_text(result, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Geri", callback_data="menu_back")]]))
        except Exception:
            pass

    elif data == "menu_keywords":
        kws = user_keywords.get(uid, [])
        result = t["keywords_title"] + "\n\n"
        if kws:
            for i, kw in enumerate(kws, 1):
                result += str(i) + ". " + kw + "\n"
        else:
            result += t["no_keywords"] + "\n"
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("+ Acarsoz Elave Et", callback_data="add_keyword")],
            [InlineKeyboardButton("Acarsoz Xeberler", callback_data="keyword_news")],
            [InlineKeyboardButton("🔙 Geri", callback_data="menu_back")]
        ])
        try:
            await q.edit_message_text(result, reply_markup=kb)
        except Exception:
            pass

    elif data == "add_keyword":
        user_states[uid] = "waiting_keyword"
        try:
            await q.edit_message_text(t["keyword_ask"])
        except Exception:
            pass

    elif data == "keyword_news":
        kws = user_keywords.get(uid, [])
        if not kws:
            try:
                await q.edit_message_text(t["no_keywords"], reply_markup=get_main_kb(lang))
            except Exception:
                pass
            return
        try:
            await q.edit_message_text(t["fetching"])
        except Exception:
            pass
        result = ""
        for kw in kws[:2]:
            articles = fetch_news_keyword(kw, 2)
            if articles:
                result += "🔍 " + kw + ":\n"
                for a in articles:
                    result += "- " + a.get("title", "") + "\n" + a.get("url", "") + "\n"
                result += "\n"
        if not result:
            result = t["no_news"]
        try:
            await q.edit_message_text(result, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Geri", callback_data="menu_back")]]), disable_web_page_preview=True)
        except Exception:
            pass

    elif data == "menu_profile":
        score = user_quiz_scores.get(uid, 0)
        joined = user_joined.get(uid, "N/A")
        saved_count = len(user_saved.get(uid, []))
        kw_count = len(user_keywords.get(uid, []))
        lang_name = {"az": "Azerbaycanca", "en": "English", "ru": "Russki", "tr": "Turkce", "de": "Deutsch"}.get(lang, lang)
        result = t["profile_title"] + "\n\n"
        result += "ID: " + str(uid) + "\n"
        result += "Dil: " + lang_name + "\n"
        result += "Qosulma: " + joined + "\n"
        result += "Saxlanmis xeberler: " + str(saved_count) + "\n"
        result += "Acarsozler: " + str(kw_count) + "\n"
        result += "Aktivlik xali: " + str(score) + "\n"
        try:
            await q.edit_message_text(result, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Geri", callback_data="menu_back")]]))
        except Exception:
            pass

    elif data == "menu_leaderboard":
        scores = sorted(user_quiz_scores.items(), key=lambda x: x[1], reverse=True)[:10]
        result = t["leaderboard_title"] + "\n\n"
        medals = ["🥇", "🥈", "🥉"]
        for i, (user_id, score) in enumerate(scores, 1):
            medal = medals[i-1] if i <= 3 else str(i) + "."
            result += medal + " User" + str(user_id)[-4:] + ": " + str(score) + " xal\n"
        if not scores:
            result += "Hec kim yoxdur."
        try:
            await q.edit_message_text(result, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Geri", callback_data="menu_back")]]))
        except Exception:
            pass

    elif data == "menu_vacation":
        if user_vacation.get(uid, False):
            user_vacation[uid] = False
            msg = t["vacation_off"]
        else:
            user_vacation[uid] = True
            msg = t["vacation_on"]
        try:
            await q.edit_message_text(msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Geri", callback_data="menu_back")]]))
        except Exception:
            pass

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    lang = get_lang(uid)
    text = update.message.text
    state = user_states.get(uid, "")

    if state == "waiting_city":
        user_states.pop(uid, None)
        weather = fetch_weather(text)
        if not weather:
            await update.message.reply_text("Sehir tapilmadi.", reply_markup=get_main_kb(lang))
            return
        result = "🌤️ " + weather["city"] + "\n\n"
        result += "🌡️ " + str(weather["temp"]) + "C (Hiss: " + str(weather["feels"]) + "C)\n"
        result += "☁️ " + weather["desc"] + "\n"
        result += "💧 " + str(weather["humidity"]) + "%\n"
        result += "💨 " + str(weather["wind"]) + " m/s"
        await update.message.reply_text(result, reply_markup=get_main_kb(lang))

    elif state == "waiting_ai_question":
        user_states.pop(uid, None)
        articles = last_articles.get(uid, [])
        ctx = ""
        if articles:
            ctx = "Context: " + articles[0].get("title", "") + ". " + (articles[0].get("description", "") or "")
        answer = groq_ask(ctx + "\n\nUser question: " + text, lang)
        await update.message.reply_text("🤖 " + answer, reply_markup=get_main_kb(lang))

    elif state == "waiting_keyword":
        user_states.pop(uid, None)
        if uid not in user_keywords:
            user_keywords[uid] = []
        if text not in user_keywords[uid]:
            user_keywords[uid].append(text)
        await update.message.reply_text(TEXTS[lang]["keyword_set"], reply_markup=get_main_kb(lang))

    else:
        await update.message.reply_text(TEXTS[lang]["welcome"], reply_markup=get_main_kb(lang))

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(btn))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("PulseBot isleyir!")
    app.run_polling()

if __name__ == "__main__":
    main()
