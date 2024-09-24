import mysql.connector
from mysql.connector import errorcode
from faker import Faker
import bcrypt
import random
import re
import datetime
import logging

# Initialize Faker
fake = Faker()

# Configure Logging
logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG for more detailed output
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
        # Uncomment the next line to enable logging to a file
        # logging.FileHandler("data_insertion.log"),
    ]
)

config = {
    'user': 'root',
    'password': 'root_password',
    'host': 'localhost',
    'database': 'movie_booking_system',
    'raise_on_warnings': True
}

# Define words associated with each genre
GENRE_WORDS = {
    "Action": {
        "nouns": ["Battle", "Warrior", "Mission", "Vengeance", "Revenge", "Strike", "Assault", "Operation"],
        "adjectives": ["Last", "Final", "Hidden", "Dark", "Red", "Black", "Secret", "Silent"]
    },
    "Comedy": {
        "nouns": ["Laugh", "Joke", "Fun", "Party", "Chaos", "Prank", "Giggle", "Fiasco"],
        "adjectives": ["Crazy", "Silly", "Wild", "Happy", "Funny", "Wacky", "Ridiculous", "Hilarious"]
    },
    "Drama": {
        "nouns": ["Heart", "Life", "Dream", "Destiny", "Journey", "Tears", "Love", "Hope"],
        "adjectives": ["Broken", "Silent", "Endless", "Deep", "Lost", "Forgotten", "True", "Hidden"]
    },
    "Horror": {
        "nouns": ["Nightmare", "Shadow", "Fear", "Terror", "Spirit", "Monster", "Darkness", "Curse"],
        "adjectives": ["Silent", "Deadly", "Haunted", "Eternal", "Blood", "Forgotten", "Cursed", "Shadowy"]
    },
    "Sci-Fi": {
        "nouns": ["Galaxy", "Star", "Universe", "Alien", "Planet", "Future", "Space", "Quantum"],
        "adjectives": ["Lost", "Infinite", "Dark", "New", "Cyber", "Virtual", "Galactic", "Interstellar"]
    },
    "Romance": {
        "nouns": ["Love", "Heart", "Dream", "Passion", "Destiny", "Journey", "Promise", "Forever"],
        "adjectives": ["Eternal", "True", "Hidden", "Secret", "Pure", "Lost", "Deep", "Silent"]
    },
    "Thriller": {
        "nouns": ["Shadow", "Game", "Secret", "Danger", "Mist", "Night", "Trap", "Mind"],
        "adjectives": ["Silent", "Dark", "Hidden", "Final", "Deadly", "Last", "Deep", "Lost"]
    }
}

# Define additional words or patterns for specific languages
LANGUAGE_ADDITIONAL_WORDS = {
    "Hindi": {
        "nouns": ["Dil", "Jaan", "Pyaar", "Sapna", "Zindagi", "Aashiqui", "Kismet", "Ishq"],
        "adjectives": ["Khoobsurat", "Anokhi", "Pyaari", "Dastaan", "Mohabbat", "Sajawat", "Rangin", "Dil Se"]
    },
    "Spanish": {
        "nouns": ["Amor", "Vida", "Sueño", "Corazón", "Destino", "Pasión", "Estrella", "Luna"],
        "adjectives": ["Eterno", "Secreto", "Perdido", "Feliz", "Brillante", "Oscuro", "Dulce", "Puro"]
    },
    "French": {
        "nouns": ["Amour", "Vie", "Rêve", "Cœur", "Destin", "Passion", "Étoile", "Lune"],
        "adjectives": ["Éternel", "Secret", "Perdu", "Heureux", "Brillant", "Sombre", "Doux", "Pur"]
    },
    "German": {
        "nouns": ["Liebe", "Leben", "Traum", "Herz", "Schicksal", "Leidenschaft", "Stern", "Mond"],
        "adjectives": ["Ewiger", "Geheimer", "Verlorener", "Glücklicher", "Strahlender", "Dunkler", "Süßer", "Reiner"]
    },
    "Italian": {
        "nouns": ["Amore", "Vita", "Sogno", "Cuore", "Destino", "Passione", "Stella", "Luna"],
        "adjectives": ["Eterno", "Segreto", "Perduto", "Felice", "Brillante", "Oscuro", "Dolce", "Puro"]
    },
    "Korean": {
        "nouns": ["사랑 (Sarang)", "삶 (Salm)", "꿈 (Kkum)", "심장 (Simjang)", "운명 (Unmyeong)", "열정 (Yeoljeong)", "별 (Byeol)", "달 (Dal)"],
        "adjectives": ["영원한 (Yeongwonhan)", "비밀의 (Bimilui)", "잃어버린 (Ireobeorin)", "행복한 (Haengbokhan)", "빛나는 (Bitnaneun)", "어두운 (Eoduun)", "달콤한 (Dalkomhan)", "순수한 (Sunsuhan)"]
    },
    "Portuguese": {
        "nouns": ["Amor", "Vida", "Sonho", "Coração", "Destino", "Paixão", "Estrela", "Lua"],
        "adjectives": ["Eterno", "Secreto", "Perdido", "Feliz", "Brilhante", "Escuro", "Doce", "Puro"]
    },
    "Russian": {
        "nouns": ["Любовь (Lyubov)", "Жизнь (Zhizn)", "Мечта (Mechta)", "Сердце (Serdtse)", "Судьба (Sudba)", "Страсть (Strast)", "Звезда (Zvezda)", "Луна (Luna)"],
        "adjectives": ["Вечный (Vechnyy)", "Секретный (Sekretnyy)", "Потерянный (Poteryannyy)", "Счастливый (Schastlivyy)", "Блестящий (Blestyashchiy)", "Темный (Temnyy)", "Сладкий (Sladkiy)", "Чистый (Chistyy)"]
    },
    # Add more languages as needed following the same structure
}

# Updated language_suffixes to include new languages
language_suffixes = {
    "Hindi": "Hindi",
    "Spanish": "Español",
    "French": "Français",
    "German": "Deutsch",
    "Mandarin": "中文",
    "Japanese": "日本語",
    "Italian": "Italiano",
    "Korean": "한국어",
    "Portuguese": "Português",
    "Russian": "Русский",
    # Add more languages as needed
}

# New lists for theatre name generation
THEATRE_PREFIXES = ["Grand", "Majestic", "Imperial", "Regal", "Royal", "Silver", "Golden", "Cineplex", "Galaxy", "City", "Metro"]
THEATRE_SUFFIXES = ["Cinema", "Theatre", "Multiplex", "Movie House", "Screen", "Picture House", "Cinemas", "Theatres"]

def generate_theatre_name(city):
    prefix = random.choice(THEATRE_PREFIXES)
    suffix = random.choice(THEATRE_SUFFIXES)
    return f"{prefix} {city} {suffix}"

def generate_movie_title(genre, language=None):
    """
    Generates a realistic movie title based on genre and language.
    
    Parameters:
        genre (str): The genre of the movie.
        language (str, optional): The language of the movie. Defaults to None.
    
    Returns:
        str: A generated movie title.
    """
    # Fetch words based on genre
    genre_words = GENRE_WORDS.get(genre, {})
    nouns = genre_words.get("nouns", [])
    adjectives = genre_words.get("adjectives", [])
    
    # Initialize lists for language-specific words
    language_nouns = []
    language_adjectives = []
    
    if language and language in LANGUAGE_ADDITIONAL_WORDS:
        language_words = LANGUAGE_ADDITIONAL_WORDS.get(language, {})
        language_nouns = language_words.get("nouns", [])
        language_adjectives = language_words.get("adjectives", [])
    
    # Decide on a title pattern
    patterns = [
        "{Adj} {Noun}",
        "{Noun} of the {Adj}",
        "{Adj} and the {Noun}",
        "{Noun} in the {Adj}",
        "The {Adj} {Noun}",
        "{Noun}: {Adj} Rising",
        "Return of the {Noun}",
        "Rise of the {Adj} {Noun}",
        "{Adj} {Noun} Saga",
        "{Noun} {Adj} Chronicles"
    ]
    
    # Combine genre and language words
    combined_nouns = nouns + language_nouns
    combined_adjectives = adjectives + language_adjectives
    
    if not combined_nouns:
        combined_nouns = nouns  # Fallback to genre nouns
    if not combined_adjectives:
        combined_adjectives = adjectives  # Fallback to genre adjectives
    
    # Select a random pattern
    pattern = random.choice(patterns)
    
    # Select random adjective and noun
    adj = random.choice(combined_adjectives) if combined_adjectives else ""
    noun = random.choice(combined_nouns) if combined_nouns else ""
    
    # Construct the title
    title = pattern.format(Adj=adj, Noun=noun)
    
    # Optionally, append language-specific phrases
    if language and language != "English":
        suffix = language_suffixes.get(language, "")
        if suffix:
            title = f"{title} ({suffix})"
    
    return title

def main():
    try:
        # Establish the database connection
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        logging.info("Successfully connected to the database.")

        # Insert data in the correct order
        user_ids = insert_users(cursor, n=100)
        theatre_ids = insert_theatres(cursor, n=10)
        format_ids = insert_formats(cursor)
        seat_category_ids = insert_seat_categories(cursor)
        movie_ids = insert_movies(cursor, n=50)
        screen_ids = insert_screens(cursor, theatre_ids, n_screens_range=(5,10))
        seat_ids = insert_seats(cursor, screen_ids, seat_category_ids)
        showtime_ids = insert_showtimes(cursor, theatre_ids, screen_ids, movie_ids, format_ids)
        insert_prices(cursor, theatre_ids, screen_ids, movie_ids, format_ids, seat_category_ids)
        insert_showseats(cursor, showtime_ids, screen_ids, seat_ids)
        booking_ids = insert_bookings(cursor, user_ids, showtime_ids, n=200)
        insert_bookedseats(cursor, booking_ids, showtime_ids)

        # Commit all the transactions
        cnx.commit()
        logging.info("Sample data insertion completed successfully.")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logging.error("Error: Something is wrong with your user name or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logging.error("Error: Database does not exist.")
        else:
            logging.error(f"MySQL Error: {err}")
    except Exception as ex:
        logging.error(f"General Error: {ex}")
    finally:
        cursor.close()
        cnx.close()
        logging.info("Database connection closed.")

def insert_users(cursor, n=100):
    add_user = (
        "INSERT INTO User "
        "(user_name, email, phone_number, password_hash, role) "
        "VALUES (%s, %s, %s, %s, %s)"
    )
    users = []
    logging.info("\nInserting Users:")
    for _ in range(n):
        user_name = fake.name()
        email = fake.unique.email()
        
        # Format Phone Number to remove non-digits and limit to 15 characters
        phone_number = format_phone_number(fake.phone_number())[:15]
        
        password_hash = bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        role = random.choices(['customer', 'admin'], weights=[90, 10], k=1)[0]
        user = (user_name, email, phone_number, password_hash, role)
        users.append(user)
        logging.debug(f"  - User: {user}")  # Use DEBUG level for detailed info
    
    try:
        cursor.executemany(add_user, users)
        logging.info(f"Inserted {n} users.")
        # Retrieve inserted user IDs
        cursor.execute("SELECT user_id FROM User ORDER BY user_id DESC LIMIT %s", (n,))
        user_ids = [row[0] for row in cursor.fetchall()][::-1]  # Reverse to maintain order
        return user_ids
    except mysql.connector.Error as err:
        logging.error(f"Error inserting users: {err}")
        return []

def format_phone_number(phone):
    """
    Formats the phone number by removing unwanted characters.
    """
    return re.sub(r'\D', '', phone)

def insert_theatres(cursor, n=10):
    add_theatre = (
        "INSERT INTO Theatre "
        "(theatre_name, location) "
        "VALUES (%s, %s)"
    )
    theatres = []
    logging.info("\nInserting Theatres:")
    cities = set()
    while len(cities) < n:
        city = fake.city()
        if city not in cities:
            cities.add(city)

    for city in cities:
        theatre_name = generate_theatre_name(city)
        location = fake.address().replace('\n', ', ')
        theatre = (theatre_name, location)
        theatres.append(theatre)
        logging.debug(f"  - Theatre: {theatre}")  # Use DEBUG level for detailed info
    
    try:
        cursor.executemany(add_theatre, theatres)
        logging.info(f"Inserted {len(theatres)} theatres.")
        # Retrieve inserted theatre IDs
        cursor.execute("SELECT theatre_id FROM Theatre ORDER BY theatre_id DESC LIMIT %s", (len(theatres),))
        theatre_ids = [row[0] for row in cursor.fetchall()][::-1]
        return theatre_ids
    except mysql.connector.Error as err:
        logging.error(f"Error inserting theatres: {err}")
        return []

def insert_formats(cursor):
    add_format = (
        "INSERT INTO Format "
        "(format_name) "
        "VALUES (%s)"
    )
    formats = [("2D",), ("3D",), ("IMAX",), ("4DX",)]
    logging.info("\nInserting Formats:")
    for fmt in formats:
        logging.debug(f"  - Format: {fmt}")  # Use DEBUG level for detailed info
    
    try:
        cursor.executemany(add_format, formats)
        logging.info(f"Inserted {len(formats)} formats.")
        # Retrieve inserted format IDs
        cursor.execute("SELECT format_id FROM Format ORDER BY format_id DESC LIMIT %s", (len(formats),))
        format_ids = [row[0] for row in cursor.fetchall()][::-1]
        return format_ids
    except mysql.connector.Error as err:
        logging.error(f"Error inserting formats: {err}")
        return []

def insert_seat_categories(cursor):
    add_category = (
        "INSERT INTO SeatCategory "
        "(category_name) "
        "VALUES (%s)"
    )
    categories = [("Regular",), ("Premium",), ("VIP",)]
    logging.info("\nInserting Seat Categories:")
    for category in categories:
        logging.debug(f"  - Seat Category: {category}")  # Use DEBUG level for detailed info
    
    try:
        cursor.executemany(add_category, categories)
        logging.info(f"Inserted {len(categories)} seat categories.")
        # Retrieve inserted category IDs
        cursor.execute("SELECT category_id FROM SeatCategory ORDER BY category_id DESC LIMIT %s", (len(categories),))
        category_ids = [row[0] for row in cursor.fetchall()][::-1]
        return category_ids
    except mysql.connector.Error as err:
        logging.error(f"Error inserting seat categories: {err}")
        return []

def insert_movies(cursor, n=50):
    add_movie = (
        "INSERT INTO Movie "
        "(movie_name, language, duration, genre, release_date, rating, director, cast, synopsis) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )
    genres = ["Action", "Comedy", "Drama", "Horror", "Sci-Fi", "Romance", "Thriller"]
    languages = ["English", "Hindi", "Spanish", "French", "German", "Mandarin", "Japanese", "Italian", "Korean", "Portuguese", "Russian"]
    ratings = ["G", "PG", "PG-13", "R", "NC-17"]
    movies = []
    logging.info("\nInserting Movies:")
    for _ in range(n):
        genre = random.choice(genres)
        language = random.choice(languages)
        movie_name = generate_movie_title(genre, language)
        duration = random.randint(90, 180)
        release_date = fake.date_between(start_date='-2y', end_date='today').strftime('%Y-%m-%d')
        rating = random.choice(ratings)
        director = fake.name()
        # Generate cast without uniqueness to prevent exhaustion
        cast = ', '.join([fake.name() for _ in range(random.randint(2,5))])
        synopsis = fake.paragraph(nb_sentences=3)
        movie = (movie_name, language, duration, genre, release_date, rating, director, cast, synopsis)
        movies.append(movie)
        logging.debug(f"  - Movie: {movie}")  # Use DEBUG level for detailed info
    
    try:
        cursor.executemany(add_movie, movies)
        logging.info(f"Inserted {n} movies.")
        # Retrieve inserted movie IDs
        cursor.execute("SELECT movie_id FROM Movie ORDER BY movie_id DESC LIMIT %s", (n,))
        movie_ids = [row[0] for row in cursor.fetchall()][::-1]
        return movie_ids
    except mysql.connector.Error as err:
        logging.error(f"Error inserting movies: {err}")
        return []

def insert_screens(cursor, theatre_ids, n_screens_range=(5,10)):
    add_screen = (
        "INSERT INTO Screen "
        "(theatre_id, screen_name, total_seats) "
        "VALUES (%s, %s, %s)"
    )
    screens = []
    logging.info("\nInserting Screens:")
    for theatre_id in theatre_ids:
        num_screens = random.randint(*n_screens_range)
        for i in range(1, num_screens + 1):
            screen_name = f"Screen {i}"
            total_seats = random.choice([50, 75, 100, 150])
            screen = (theatre_id, screen_name, total_seats)
            screens.append(screen)
            logging.debug(f"  - Screen: {screen}")  # Use DEBUG level for detailed info
    
    try:
        cursor.executemany(add_screen, screens)
        logging.info(f"Inserted {len(screens)} screens.")
        # Retrieve inserted screen IDs
        cursor.execute("SELECT screen_id FROM Screen ORDER BY screen_id DESC LIMIT %s", (len(screens),))
        screen_ids = [row[0] for row in cursor.fetchall()][::-1]
        return screen_ids
    except mysql.connector.Error as err:
        logging.error(f"Error inserting screens: {err}")
        return []

def insert_seats(cursor, screen_ids, seat_category_ids):
    add_seat = (
        "INSERT INTO Seat "
        "(screen_id, seat_number, category_id, seat_row, seat_column) "
        "VALUES (%s, %s, %s, %s, %s)"
    )
    seats = []
    logging.info("\nInserting Seats:")
    # Fetch SeatCategory mappings
    seat_category_map = {}
    try:
        cursor.execute("SELECT category_id, category_name FROM SeatCategory")
        for (category_id, category_name) in cursor:
            seat_category_map[category_name] = category_id
    except mysql.connector.Error as err:
        logging.error(f"Error fetching seat categories: {err}")
        return []
    
    for screen_id in screen_ids:
        # Fetch total seats for the screen
        cursor.execute("SELECT total_seats FROM Screen WHERE screen_id = %s", (screen_id,))
        result = cursor.fetchone()
        if not result:
            continue
        total_seats = result[0]
        
        # Determine rows and columns
        rows = random.randint(5, 15)
        cols = total_seats // rows if rows else 1
        if cols == 0:
            cols = 1  # Prevent division by zero
        
        for row in range(1, rows + 1):
            for col in range(1, cols + 1):
                seat_number = f"{chr(64 + row)}{col}"  # e.g., A1, B2
                # Assign category based on row number
                if row <= 2:
                    category = "VIP"
                elif row <=5:
                    category = "Premium"
                else:
                    category = "Regular"
                category_id = seat_category_map.get(category, seat_category_map.get("Regular"))
                seat = (screen_id, seat_number, category_id, row, col)
                seats.append(seat)
                logging.debug(f"  - Seat: {seat}")  # Use DEBUG level for detailed info
    
    try:
        cursor.executemany(add_seat, seats)
        logging.info(f"Inserted {len(seats)} seats.")
        # Optionally, retrieve seat IDs if needed
        # cursor.execute("SELECT seat_id FROM Seat ORDER BY seat_id DESC LIMIT %s", (len(seats),))
        # seat_ids = [row[0] for row in cursor.fetchall()][::-1]
        # return seat_ids
    except mysql.connector.Error as err:
        logging.error(f"Error inserting seats: {err}")

def insert_showtimes(cursor, theatre_ids, screen_ids, movie_ids, format_ids):
    add_showtime = (
        "INSERT INTO ShowTime "
        "(theatre_id, screen_id, movie_id, format_id, show_date, start_time, status) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)"
    )
    showtimes = []
    today = datetime.date.today()

    # Buffer time between shows in minutes
    BUFFER_TIME = 30  # 30 minutes buffer
    logging.info("\nInserting ShowTimes:")
    for theatre_id in theatre_ids:
        # Fetch screens for this theatre
        cursor.execute("SELECT screen_id FROM Screen WHERE theatre_id = %s", (theatre_id,))
        screens = [row[0] for row in cursor.fetchall()]
        for screen_id in screens:
            for day_offset in range(0, 7):  # Next 7 days
                show_date = today + datetime.timedelta(days=day_offset)
                # Define operating hours
                opening_time = datetime.datetime.combine(show_date, datetime.time(10, 0))  # 10:00 AM
                closing_time = datetime.datetime.combine(show_date, datetime.time(23, 0))  # 11:00 PM

                # Initialize current_time
                current_time = opening_time

                while current_time < closing_time:
                    # Select a movie that can fit into the remaining time
                    cursor.execute("SELECT movie_id, duration FROM Movie")
                    movies = cursor.fetchall()
                    if not movies:
                        break
                    # Filter movies that fit into the remaining time
                    possible_movies = [movie for movie in movies if (current_time + datetime.timedelta(minutes=movie[1] + BUFFER_TIME)) <= closing_time]
                    if not possible_movies:
                        break

                    movie = random.choice(possible_movies)
                    movie_id, duration = movie
                    format_id = random.choice(format_ids)
                    status = "active"

                    start_time = current_time.time().strftime('%H:%M:%S')
                    show_date_str = show_date.strftime('%Y-%m-%d')

                    showtime = (theatre_id, screen_id, movie_id, format_id, show_date_str, start_time, status)
                    showtimes.append(showtime)
                    logging.debug(f"  - ShowTime: {showtime}")  # Use DEBUG level for detailed info

                    # Update current_time
                    current_time += datetime.timedelta(minutes=duration + BUFFER_TIME)

                    # Round up to the nearest 5 minutes
                    minutes = current_time.minute
                    rounded_minutes = (minutes + 4) // 5 * 5  # Round up to next multiple of 5
                    if rounded_minutes == 60:
                        current_time = current_time.replace(hour=current_time.hour + 1, minute=0, second=0, microsecond=0)
                    else:
                        current_time = current_time.replace(minute=rounded_minutes, second=0, microsecond=0)
    
    try:
        cursor.executemany(add_showtime, showtimes)
        logging.info(f"Inserted {len(showtimes)} showtimes.")
        # Retrieve inserted showtime IDs
        cursor.execute("SELECT show_id FROM ShowTime ORDER BY show_id DESC LIMIT %s", (len(showtimes),))
        showtime_ids = [row[0] for row in cursor.fetchall()][::-1]
        return showtime_ids
    except mysql.connector.Error as err:
        logging.error(f"Error inserting showtimes: {err}")
        return []

def insert_prices(cursor, theatre_ids, screen_ids, movie_ids, format_ids, seat_category_ids):
    add_price = (
        "INSERT INTO Price "
        "(theatre_id, screen_id, movie_id, format_id, category_id, price) "
        "VALUES (%s, %s, %s, %s, %s, %s)"
    )
    prices = []
    logging.info("\nInserting Prices:")
    # Example pricing logic
    for theatre_id in theatre_ids:
        for screen_id in screen_ids:
            for movie_id in movie_ids:
                for format_id in format_ids:
                    for category_id in seat_category_ids:
                        base_price = random.choice([100, 150, 200])
                        if format_id == 2:  # Assuming 1:2D, 2:3D, etc.
                            base_price += 20
                        elif format_id == 3:
                            base_price += 50
                        if category_id == 3:  # VIP
                            base_price += 100
                        elif category_id == 2:  # Premium
                            base_price += 50
                        price = min(base_price, 1000)  # Ensure price is reasonable
                        price_entry = (theatre_id, screen_id, movie_id, format_id, category_id, price)
                        prices.append(price_entry)
                        logging.debug(f"  - Price: {price_entry}")  # Use DEBUG level for detailed info
    
    try:
        cursor.executemany(add_price, prices)
        logging.info(f"Inserted {len(prices)} price entries.")
    except mysql.connector.Error as err:
        logging.error(f"Error inserting prices: {err}")

def insert_showseats(cursor, showtime_ids, screen_ids, seat_ids):
    add_showseat = (
        "INSERT INTO ShowSeat "
        "(show_id, seat_id, is_booked, version) "
        "VALUES (%s, %s, %s, %s)"
    )
    showseats = []
    logging.info("\nInserting ShowSeats:")
    # Map show_id to screen_id
    show_screen_map = {}
    cursor.execute("SELECT show_id, screen_id FROM ShowTime")
    for (show_id, screen_id) in cursor:
        show_screen_map[show_id] = screen_id
    
    # Determine shows to fully book (~5% of total shows)
    num_shows_to_full_book = max(1, len(showtime_ids) // 20)
    shows_to_full_book = random.sample(showtime_ids, num_shows_to_full_book)
    
    # Fetch seats per screen
    screen_seats_map = {}
    cursor.execute("SELECT screen_id, seat_id FROM Seat")
    for (screen_id, seat_id) in cursor:
        if screen_id not in screen_seats_map:
            screen_seats_map[screen_id] = []
        screen_seats_map[screen_id].append(seat_id)
    
    for show_id in showtime_ids:
        screen_id = show_screen_map.get(show_id)
        if not screen_id:
            continue
        seats = screen_seats_map.get(screen_id, [])
        is_full_book = show_id in shows_to_full_book
        for seat_id in seats:
            is_booked = True if is_full_book else (random.random() < 0.2)  # 20% chance booked
            showseat = (show_id, seat_id, is_booked, 1)
            showseats.append(showseat)
            logging.debug(f"  - ShowSeat: {showseat}")  # Use DEBUG level for detailed info
    
    try:
        cursor.executemany(add_showseat, showseats)
        logging.info(f"Inserted {len(showseats)} show seats with {num_shows_to_full_book} shows fully booked.")
    except mysql.connector.Error as err:
        logging.error(f"Error inserting show seats: {err}")

def insert_bookings(cursor, user_ids, showtime_ids, n=200):
    add_booking = (
        "INSERT INTO Booking "
        "(show_id, user_id, total_amount, status, version) "
        "VALUES (%s, %s, %s, %s, %s)"
    )
    bookings = []
    logging.info("\nInserting Bookings:")
    for _ in range(n):
        show_id = random.choice(showtime_ids)
        user_id = random.choice(user_ids)
        
        # Fetch price for the show
        cursor.execute("""
            SELECT price 
            FROM Price 
            WHERE theatre_id = (SELECT theatre_id FROM ShowTime WHERE show_id = %s) 
              AND screen_id = (SELECT screen_id FROM ShowTime WHERE show_id = %s) 
              AND movie_id = (SELECT movie_id FROM ShowTime WHERE show_id = %s) 
              AND format_id = (SELECT format_id FROM ShowTime WHERE show_id = %s)
            LIMIT 1
        """, (show_id, show_id, show_id, show_id))
        result = cursor.fetchone()
        price = result[0] if result else 100  # Default price
        
        num_seats = random.randint(1,5)
        total_amount = price * num_seats
        status = "confirmed"
        version = 1
        booking = (show_id, user_id, total_amount, status, version)
        bookings.append(booking)
        logging.debug(f"  - Booking: {booking}")  # Use DEBUG level for detailed info
    
    try:
        cursor.executemany(add_booking, bookings)
        logging.info(f"Inserted {n} bookings.")
        # Retrieve inserted booking IDs
        cursor.execute("SELECT booking_id FROM Booking ORDER BY booking_id DESC LIMIT %s", (n,))
        booking_ids = [row[0] for row in cursor.fetchall()][::-1]
        return booking_ids
    except mysql.connector.Error as err:
        logging.error(f"Error inserting bookings: {err}")
        return []

def insert_bookedseats(cursor, booking_ids, showtime_ids):
    add_bookedseat = (
        "INSERT INTO BookedSeat "
        "(booking_id, show_seat_id) "
        "VALUES (%s, %s)"
    )
    bookedseats = []
    logging.info("\nInserting BookedSeats:")
    # Map show_id to show_seat_ids that are booked
    show_seat_map = {}
    cursor.execute("SELECT show_id, show_seat_id FROM ShowSeat WHERE is_booked = TRUE")
    for (show_id, show_seat_id) in cursor:
        if show_id not in show_seat_map:
            show_seat_map[show_id] = []
        show_seat_map[show_id].append(show_seat_id)
    
    for booking_id in booking_ids:
        # Fetch show_id for the booking
        cursor.execute("SELECT show_id FROM Booking WHERE booking_id = %s", (booking_id,))
        result = cursor.fetchone()
        if not result:
            continue
        show_id = result[0]
        
        # Fetch all booked seats for the show
        booked_seats = show_seat_map.get(show_id, [])
        if not booked_seats:
            continue
        
        # Assign 1 to 5 seats randomly
        num_seats = random.randint(1, min(5, len(booked_seats)))
        selected_seats = random.sample(booked_seats, num_seats)
        for show_seat_id in selected_seats:
            bookedseat = (booking_id, show_seat_id)
            bookedseats.append(bookedseat)
            logging.debug(f"  - BookedSeat: {bookedseat}")  # Use DEBUG level for detailed info
    
    try:
        cursor.executemany(add_bookedseat, bookedseats)
        logging.info(f"Inserted {len(bookedseats)} booked seats.")
    except mysql.connector.Error as err:
        logging.error(f"Error inserting booked seats: {err}")

if __name__ == "__main__":
    main()



