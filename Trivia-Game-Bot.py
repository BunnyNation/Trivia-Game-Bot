import random
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os
from dotenv import load_dotenv

# Set the port to an environment variable or default to 8080
port = os.getenv("PORT", "8080")
print(f"Listening on port {port}...")

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("No API token found. Make sure BOT_TOKEN is set.")



QUESTIONS = [
    ("Who won the FIFA World Cup in 2018?", ["Croatia", "France", "Germany", "Brazil"], "France"),
    ("Which player has won the most Ballon d'Or awards?", ["C.Ronaldo", "Neymar", "Ronaldinho", "Messi"], "Messi"),
    ("Which country has won the most FIFA World Cups?", ["Italy", "Germany", "Brazil", "Argentina"], "Brazil"),
    ("Who scored the winning goal in the 2014 World Cup final?", ["Lionel Messi", "Mario Götze", "Thomas Müller", "André Schürrle"], "Mario Götze"),
    ("Which English club has won the most Premier League titles?", ["Chelsea", "Manchester United", "Liverpool", "Arsenal"], "Manchester United"),
    ("Who is known as the 'King of Football'?", ["Pele", "Maradona", "Messi", "Ronaldo"], "Pele"),
    ("In which year was the UEFA Champions League established?", ["1984", "1992", "1975", "1965"], "1992"),
    ("Who holds the record for the most goals in a single World Cup?", ["Ronaldo", "Just Fontaine", "Miroslav Klose", "Pelé"], "Just Fontaine"),
    ("Which country hosted the 2010 FIFA World Cup?", ["South Africa", "Brazil", "Germany", "Russia"], "South Africa"),
    ("Which player is known as 'The Pharaoh'?", ["RAshy MIke", "Mahrez", "Salah", "Hakimi"], "Salah"),
    ("Who is the top scorer in the history of the Premier League?", ["Alan Shearer", "Wayne Rooney", "Sergio Agüero", "Thierry Henry"], "Alan Shearer"),
    ("Which country won the 2006 FIFA World Cup?", ["England", "France", "Italy", "Argentina"], "Italy"),
    ("Who is known as 'CR7'?", ["Cristiano Ronaldo", "Lionel Messi", "David Beckham", "Neymar"], "Cristiano Ronaldo"),
    ("Which country did Zinedine Zidane represent in international football?", ["Egypt", "France", "Brazil", "Portugal"], "France"),
    ("Which player holds the record for the most goals in the UEFA Champions League?", ["Cristiano Ronaldo", "Lionel Messi", "Raúl", "Robert Lewandowski"], "Cristiano Ronaldo"),
    ("What year did Barcelona win their first Champions League title?", ["1992", "2006", "2011", "2015"], "1992"),
    ("Which player has the most appearances in the Premier League?", ["Ryan Giggs", "Gareth Barry", "Steven Gerrard", "Frank Lampard"], "Ryan Giggs"),
    ("Who won the Golden Boot at the 2018 FIFA World Cup?", ["Harry Kane", "Luka Modrić", "Kylian Mbappé", "Antoine Griezmann"], "Harry Kane"),
    ("What is the nickname of the Brazilian national football team?", ["Seleção", "Canarinha", "La Albiceleste", "Les Bleus"], "Seleção"),
    ("Which stadium is known as the 'Theatre of Dreams'?", ["Old Trafford", "Anfield", "Emirates Stadium", "Stamford Bridge"], "Old Trafford"),
    ("Who won the 2020 UEFA Champions League?", ["Bayern Munich", "PSG", "Liverpool", "Manchester City"], "Bayern Munich"),
    ("Which player is famous for his 'Hand of God' goal?", ["Diego Maradona", "Lionel Messi", "Zinedine Zidane", "Pelé"], "Diego Maradona"),
    ("Who is the manager of Manchester City as of 2024?", ["Pep Guardiola", "Jurgen Klopp", "Carlo Ancelotti", "Mauricio Pochettino"], "Pep Guardiola"),
    ("Which footballer is known as the 'Egyptian King'?", ["Mohamed Salah", "Ahmed Hegazi", "Mahmoud Trezeguet", "Ali Gabr"], "Mohamed Salah"),
    ("Which country hosted the 2014 FIFA World Cup?", ["Brazil", "Argentina", "Chile", "Uruguay"], "Brazil"),
    ("Which country won the Euro 2020 tournament?", ["Italy", "England", "France", "Portugal"], "Italy"),
    ("What is the nickname of the Spanish national football team?", ["La Roja", "La Furia", "La Celeste", "La Tri"], "La Roja"),
    ("Who is the all-time top scorer for the Spanish national team?", ["David Villa", "Raúl", "Fernando Torres", "Andres Iniesta"], "David Villa"),
    ("Which club won the 2021 UEFA Champions League?", ["Chelsea", "Manchester City", "Bayern Munich", "Real Madrid"], "Chelsea"),
    ("Who is the top scorer of the Argentina national football team?", ["Lionel Messi", "Gabriel Batistuta", "Diego Maradona", "Sergio Agüero"], "Lionel Messi"),
    ("What is the capital city of Japan?", ["Tokyo", "Kyoto", "Osaka", "Nagasaki"], "Tokyo"),
    ("Who painted the Mona Lisa?", ["Vincent van Gogh", "Leonardo da Vinci", "Pablo Picasso", "Claude Monet"], "Leonardo da Vinci"),
    ("What is the smallest country in the world?", ["Monaco", "Vatican City", "Nauru", "Malta"], "Vatican City"),
    ("Who wrote the play 'Romeo and Juliet'?", ["William Shakespeare", "J.K. Rowling", "Charles Dickens", "Ernest Hemingway"], "William Shakespeare"),
    ("What is the tallest mountain in the world?", ["K2", "Kangchenjunga", "Mount Everest", "Makalu"], "Mount Everest"),
    ("What is the capital city of Australia?", ["Sydney", "Melbourne", "Brisbane", "canberra"], "Canberra"),
    ("Which planet is known as the Red Planet?", ["Venus", "Jupiter", "Mars", "Saturn"], "Mars"),
    ("What is the largest ocean in the world?", ["Pacific Ocean", "Atlantic Ocean", "Indian Ocean", "Arctic Ocean"], "Pacific Ocean"),
    ("What is the main ingredient in guacamole?", ["Tomato", "Lime", "Avocado", "Onion"], "Avocado"),
    ("What is the name of the longest river in the world?", ["Nile River", "Amazon River", "Yangtze River", "Mississippi River"], "Nile River"),
    ("What is the national animal of Canada?", ["Beaver", "Moose", "Bear", "Wolf"], "Beaver"),
    ("Who invented the telephone?", ["Thomas Edison", "Alexander Graham Bell", "Nikola Tesla", "Albert Einstein"], "Alexander Graham Bell"),
    ("In which country was the game of chess invented?", ["India", "China", "Egypt", "Greece"], "India"),
    ("Which planet is closest to the sun?", ["Venus", "Mercury", "Earth", "Mars"], "Mercury"),
    ("What is the smallest bone in the human body?", ["Ulna", "Fibula", "Tibia", "Stapes"], "Stapes"),
    ("Which country is famous for its pyramids?", ["Egypt", "Mexico", "India", "China"], "Egypt"),
    ("Who was the first man to step on the moon?", ["Neil Armstrong", "Buzz Aldrin", "Michael Collins", "Yuri Gagarin"], "Neil Armstrong"),
    ("Which animal is known as the 'King of the Jungle'?", ["Lion", "Tiger", "Elephant", "Leopard"], "Lion"),
    ("What is the currency of the United Kingdom?", ["Pound Sterling", "Euro", "Dollar", "Franc"], "Pound Sterling"),
    ("Which is the longest river in South America?", ["Amazon River", "Paraná River", "Orinoco River", "São Francisco River"], "Amazon River"),
    ("In which city would you find the Colosseum?", ["Rome", "Athens", "Paris", "Istanbul"], "Rome"),
    ("What is the highest-grossing film of all time?", ["Avatar", "Titanic", "Avengers: Endgame", "Jurassic Park"], "Avatar"),
    ("Who is known as the 'Father of Computers'?", ["Alan Turing", "John von Neumann", "George Boole", "Charles Babbage",], "Charles Babbage"),
    ("What is the currency of Japan?", ["Won", "Dollar", "Yen", "Peso"], "Yen"),
    ("Which animal is the fastest on land?", ["Lion", "Horse", "Cheetah", "Ostrich"], "Cheetah"),
    ("Which country is known as the 'Land of the Rising Sun'?", ["Japan", "China", "South Korea", "India"], "Japan"),
    ("Which Manchester United Player has the  best bicycle kick in the Red Devils History?", ["Nani", "Wayne Rooney", "Alejandro Garnacho", "Marcus Rashford"], "Alejandro Garnacho"),
    ("Which team won the 2024 England FA Cup?", ["Chelsea", "Man City", "Man United", "Liverpool"], "Man United"),
    ("Which Team has the Highest Premiere League Trophy?", ["Liverpool", "Arsenal", "Man United", "Man City"], "Man United"),
    ("Who won the FIFA World Cup in 2018?", ["Croatia", "France", "Germany", "Brazil"], "France"),
    ("Which country has won the most FIFA World Cups?", ["Germany", "Italy", "Brazil", "Argentina"], "Brazil"),
    ("Who scored the winning goal in the 2014 World Cup final?",
     ["Lionel Messi", "Mario Götze", "Thomas Müller", "André Schürrle"], "Mario Götze"),
    ("Which English club has won the most Premier League titles?",
     ["Chelsea", "Manchester United", "Liverpool", "Arsenal"], "Manchester United"),
    ("Who is known as the 'King of Football'?", ["Maradona", "Messi", "Pele", "Ronaldo"], "Pele"),
    ("In which year was the UEFA Champions League established?", ["1984", "1992", "1975", "1965"], "1992"),
    ("Who holds the record for the most goals in a single World Cup?",
     ["Ronaldo", "Just Fontaine", "Miroslav Klose", "Pelé"], "Just Fontaine"),
    ("Which country hosted the 2010 FIFA World Cup?", ["Brazil", "South Africa", "Germany", "Russia"], "South Africa"),
    ("Which player is known as 'The Pharaoh'?", ["RAshy MIke", "Mahrez", "Salah", "Hakimi"], "Salah"),
    ("Who is the top scorer in the history of the Premier League?",
     ["Wayne Rooney", "Sergio Agüero", "Alan Shearer", "Thierry Henry"], "Alan Shearer"),
    ("Which country won the 2006 FIFA World Cup?", ["England", "France", "Italy", "Argentina"], "Italy"),
    ("Who is known as 'CR7'?", ["C.Ronaldo", "Messi", "D.Beckham", "Neymar"], "C.Ronaldo"),
    ("Which country did Zinedine Zidane represent in international football?", ["Egypt", "France", "Brazil", "Portugal"],
    "France"),
    ("Which player holds the record for the most goals in the UEFA Champions League?",
     ["Messi", "Raúl", "C.Ronaldo", "R.Lewandowski"], "C.Ronaldo"),
    ("What year did Barcelona win their first Champions League title?", ["1992", "2006", "2011", "2015"], "1992"),
    ("Which player has the most appearances in the Premier League?",
     ["Ryan Giggs", "Steven Gerrard", "Frank Lampard"], "Ryan Giggs"),
    ("Who won the Golden Boot at the 2018 FIFA World Cup?", ["Harry Kane", "Kylian Mbappé", "A.Griezmann"], "Harry Kane"),
    ("What is the nickname of the Brazilian national football team?", ["Canarinha", "Seleção", "La Albiceleste", "Les Bleus"], "Seleção"),
    ("Which stadium is known as the 'Theatre of Dreams'?", ["Old Trafford", "Anfield", "Emirates Stadium", "Stamford Bridge"], "Old Trafford"),
    ("Who won the 2020 UEFA Champions League?", ["Bayern Munich", "PSG", "Liverpool", "Manchester City"], "Bayern Munich"),
    ("Which player is famous for his 'Hand of God' goal?", ["Diego Maradona", "Lionel Messi", "Zinedine Zidane", "Pelé"], "Diego Maradona"),
    ("Who is the manager of Manchester City as of 2024?", ["Pep Guardiola", "Jurgen Klopp", "Carlo Ancelotti", "Mauricio Pochettino"], "Pep Guardiola"),
    ("Which footballer is known as the 'Egyptian King'?", ["Mohamed Salah", "Ahmed Hegazi", "Mahmoud Trezeguet", "Ali Gabr"], "Mohamed Salah"),
    ("Which country hosted the 2014 FIFA World Cup?", ["Brazil", "Argentina", "Chile", "Uruguay"], "Brazil"),
    ("Which country won the Euro 2020 tournament?", ["Italy", "England", "France", "Portugal"], "Italy"),
    ("What is the nickname of the Spanish national football team?", ["La Roja", "La Furia", "La Celeste", "La Tri"], "La Roja"),
    ("Who is the all-time top scorer for the Spanish national team?",
     ["David Villa", "Raúl", "Fernando Torres", "Andres Iniesta"], "David Villa"),
    ("Which club won the 2021 UEFA Champions League?", ["Chelsea", "Manchester City", "Bayern Munich", "Real Madrid"],
     "Chelsea"),
    ("Who is the top scorer of the Argentina national football team?",
     ["Lionel Messi", "Gabriel Batistuta", "Diego Maradona", "Sergio Agüero"], "Lionel Messi"),
    ("What is the capital city of Japan?", ["Tokyo", "Kyoto", "Osaka", "Nagasaki"], "Tokyo"),
    ("Who painted the Mona Lisa?", ["Vincent van Gogh", "Leonardo da Vinci", "Pablo Picasso", "Claude Monet"],"Leonardo da Vinci"),
    ("What is the smallest country in the world?", ["Monaco", "Vatican City", "Nauru", "Malta"], "Vatican City"),
    ("Who wrote the play 'Romeo and Juliet'?", ["J.K. Rowling", "William Shakespeare", "Charles Dickens", "Ernest Hemingway"], "William Shakespeare"),
    ("What is the tallest mountain in the world?", ["Mount Everest", "K2", "Kangchenjunga", "Makalu"], "Mount Everest"),
    ("What is the capital city of Australia?", ["Canberra", "Sydney", "Melbourne", "Brisbane"], "Canberra"),
    ("Which planet is known as the Red Planet?", ["Mars", "Venus", "Jupiter", "Saturn"], "Mars"),
    ("What is the largest ocean in the world?", ["Pacific Ocean", "Atlantic Ocean", "Indian Ocean", "Arctic Ocean"], "Pacific Ocean"),
    ("What is the main ingredient in guacamole?", ["Avocado", "Tomato", "Lime", "Onion"], "Avocado"),
    ("What is the name of the longest river in the world?", ["Nile River", "Amazon River", "Yangtze River", "Mississippi River"], "Nile River"),
    ("What is the national animal of Canada?", ["Beaver", "Moose", "Bear", "Wolf"], "Beaver"),
    ("Who invented the telephone?", ["Alexander Graham Bell", "Thomas Edison", "Nikola Tesla", "Albert Einstein"], "Alexander Graham Bell"),
    ("In which country was the game of chess invented?", ["India", "China", "Egypt", "Greece"], "India"),
    ("Which planet is closest to the sun?", ["Mercury", "Venus", "Earth", "Mars"], "Mercury"),
    ("What is the smallest bone in the human body?", ["Stapes", "Ulna", "Fibula", "Tibia"], "Stapes"),
    ("Which country is famous for its pyramids?", ["Egypt", "Mexico", "India", "China"], "Egypt"),
    ("Who was the first man to step on the moon?", ["Neil Armstrong", "Buzz Aldrin", "Michael Collins", "Yuri Gagarin"], "Neil Armstrong"),
    ("Which animal is known as the 'King of the Jungle'?", ["Lion", "Tiger", "Elephant", "Leopard"], "Lion"),
    ("What is the currency of the United Kingdom?", ["Pound Sterling", "Euro", "Dollar", "Franc"], "Pound Sterling"),
    ("Which is the longest river in South America?", ["Amazon River", "Paraná River", "Orinoco River", "São Francisco River"], "Amazon River"),
    ("In which city would you find the Colosseum?", ["Rome", "Athens", "Paris", "Istanbul"], "Rome"),
    ("What is the highest-grossing film of all time?", ["Avatar", "Titanic", "Avengers: Endgame", "Jurassic Park"], "Avatar"),
    ("Who is known as the 'Father of Computers'?", ["Charles Babbage", "Alan Turing", "John von Neumann", "George Boole"], "Charles Babbage"),
    ("What is the currency of Japan?", ["Yen", "Won", "Dollar", "Peso"], "Yen"),
    ("Which animal is the fastest on land?", ["Cheetah", "Lion", "Horse", "Ostrich"], "Cheetah"),
    ("Which country is known as the 'Land of the Rising Sun'?", ["Japan", "China", "South Korea", "India"], "Japan"),
    ("Which Manchester United Player has the best bicycle kick in the Red Devils History?", ["Wayne Rooney", "Nani", "Alejandro Garnacho", "Marcus Rashford"], "Alejandro Garnacho"),
]

user_scores = {}

def get_username(update: Update) -> str:
    return update.message.from_user.username or update.message.from_user.first_name

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = get_username(update)
    await update.message.reply_text(
        f"***HELLO, {username}!!**🎉🎉🎉Welcome to the Trivia Game Bot 👏👏👏, 🏠Home of FOOTBALL⚽ at its best,  ❣️💟😍🥰🤩feel free to invite ur friends👫 to test their football knowledge and know if they are real FANS❤️ 💕 💞 💓 💗 💖 💝.\n"
        "👏To start playing and Enjoying Trivia Game, simply type👏  /play          and👏  /score to check ur score."
    )

async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question, options, answer = random.choice(QUESTIONS)
    context.user_data['current_question'] = question
    context.user_data['current_answer'] = answer

    buttons = [
        [InlineKeyboardButton(opt, callback_data=opt) for opt in options]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        f"Question: {question}\n\nChoose an answer:",
        reply_markup=reply_markup
    )

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_answer = query.data
    correct_answer = context.user_data.get('current_answer')
    username = query.from_user.username or query.from_user.first_name

    await query.answer()

    if user_answer == correct_answer:
        user_scores[username] = user_scores.get(username, 0) + 1
        response = f"🎉👏Correct! ✅ Your score is now {user_scores[username]}."
    else:
        response = f"😢Incorrect ❌. The correct✔️ answer was: {correct_answer}."

    await query.edit_message_text(response)
    await ask_question(query, context)

async def score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = get_username(update)
    score = user_scores.get(username, 0)
    await update.message.reply_text(f"{username}, your current score is🎉: {score}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", ask_question))
    app.add_handler(CommandHandler("score", score))
    app.add_handler(CallbackQueryHandler(handle_answer))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
