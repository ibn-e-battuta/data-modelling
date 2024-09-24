DROP DATABASE  movie_booking_system;
CREATE DATABASE IF NOT EXISTS movie_booking_system;
USE movie_booking_system;

## USER Table
CREATE TABLE IF NOT EXISTS User (
    user_id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Unique identifier for each user',
    user_name VARCHAR(100) NOT NULL COMMENT 'Name of the user',
    email VARCHAR(100) UNIQUE NOT NULL COMMENT 'User\'s email address, must be unique',
    phone_number VARCHAR(20) COMMENT 'User\'s contact phone number',
    password_hash VARCHAR(255) NOT NULL COMMENT 'Hashed password using bcrypt for security',
    role ENUM('customer', 'admin') DEFAULT 'customer' COMMENT 'Role of the user for authorization purposes',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when the user was created',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp when the user information was last updated',
    CHECK (email LIKE '%_@__%.__%') -- Simple email format validation
) COMMENT 'Stores user information for authentication and authorization';

## THEATRE Table
CREATE TABLE IF NOT EXISTS Theatre (
    theatre_id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Unique identifier for each theatre',
    theatre_name VARCHAR(100) NOT NULL COMMENT 'Name of the theatre',
    location VARCHAR(100) NOT NULL COMMENT 'Geographical location/address of the theatre',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when the theatre was added to the system',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp when the theatre information was last updated'
) COMMENT 'Stores theatre information including name and location';

## MOVIE Table
CREATE TABLE IF NOT EXISTS Movie (
    movie_id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Unique identifier for each movie',
    movie_name VARCHAR(100) NOT NULL COMMENT 'Title of the movie',
    language VARCHAR(50) NOT NULL COMMENT 'Language in which the movie is made',
    duration INT NOT NULL COMMENT 'Duration of the movie in minutes',
    genre VARCHAR(50) COMMENT 'Genre category of the movie (e.g., Action, Comedy)',
    release_date DATE COMMENT 'Official release date of the movie',
    rating VARCHAR(10) COMMENT 'Movie rating (e.g., PG-13, R)',
    director VARCHAR(100) COMMENT 'Name of the movie\'s director',
    cast TEXT COMMENT 'List of main actors/actresses in the movie',
    synopsis TEXT COMMENT 'Brief summary or plot description of the movie',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when the movie was added to the system',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp when the movie information was last updated'
) COMMENT 'Stores movie details including ratings and synopsis';

## FORMAT Table
CREATE TABLE IF NOT EXISTS Format (
    format_id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Unique identifier for each movie format',
    format_name VARCHAR(20) NOT NULL COMMENT 'Name of the movie format (e.g., 2D, 3D, IMAX)'
) COMMENT 'Stores available movie formats like 2D, 3D, IMAX';

## SCREEN Table
CREATE TABLE IF NOT EXISTS Screen (
    screen_id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Unique identifier for each screen within a theatre',
    theatre_id INT NOT NULL COMMENT 'Identifier of the theatre where the screen is located',
    screen_name VARCHAR(50) NOT NULL COMMENT 'Name or number of the screen',
    total_seats INT NOT NULL COMMENT 'Total number of seats available in the screen',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when the screen was added to the theatre',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp when the screen information was last updated',
    FOREIGN KEY (theatre_id) REFERENCES Theatre(theatre_id) ON DELETE CASCADE,
    UNIQUE (theatre_id, screen_name) COMMENT 'Ensures screen names are unique within each theatre'
) COMMENT 'Stores screen details for each theatre';

## SEAT CATEGORY Table
CREATE TABLE IF NOT EXISTS SeatCategory (
    category_id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Unique identifier for each seat category',
    category_name VARCHAR(50) NOT NULL COMMENT 'Name of the seat category (e.g., Regular, Premium)'
) COMMENT 'Defines different seat categories like Regular, Premium';

## SEAT Table
CREATE TABLE IF NOT EXISTS Seat (
    seat_id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Unique identifier for each seat',
    screen_id INT NOT NULL COMMENT 'Identifier of the screen where the seat is located',
    seat_number VARCHAR(10) NOT NULL COMMENT 'Alphanumeric designation of the seat (e.g., A1, B5)',
    category_id INT NOT NULL COMMENT 'Identifier of the seat category (e.g., Regular, Premium)',
    seat_row INT NOT NULL COMMENT 'Row number for seat map visualization',
    seat_column INT NOT NULL COMMENT 'Column number for seat map visualization',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when the seat was added to the screen',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp when the seat information was last updated',
    FOREIGN KEY (screen_id) REFERENCES Screen(screen_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES SeatCategory(category_id),
    UNIQUE (screen_id, seat_number) COMMENT 'Ensures each seat number is unique within a screen',
    CHECK (seat_row > 0),
    CHECK (seat_column > 0)
) COMMENT 'Stores seat details including position for visualization';

## ShowTime Table
CREATE TABLE IF NOT EXISTS ShowTime (
    show_id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Unique identifier for each show',
    theatre_id INT NOT NULL COMMENT 'Identifier of the theatre hosting the show',
    screen_id INT NOT NULL COMMENT 'Identifier of the screen where the show is scheduled',
    movie_id INT NOT NULL COMMENT 'Identifier of the movie being shown',
    format_id INT NOT NULL COMMENT 'Identifier of the movie format (e.g., 2D, 3D)',
    show_date DATE NOT NULL COMMENT 'Date when the show is scheduled',
    start_time TIME NOT NULL COMMENT 'Start time of the show',
    status ENUM('active', 'cancelled', 'completed') DEFAULT 'active' COMMENT 'Current status of the show',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when the show was created',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp when the show information was last updated',
    FOREIGN KEY (theatre_id) REFERENCES Theatre(theatre_id) ON DELETE CASCADE,
    FOREIGN KEY (screen_id) REFERENCES Screen(screen_id),
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id),
    FOREIGN KEY (format_id) REFERENCES Format(format_id),
    CHECK (status IN ('active', 'cancelled', 'completed')),
    UNIQUE INDEX idx_unique_show (theatre_id, screen_id, show_date, start_time)
) COMMENT 'Schedules shows with date, time, and status';

## Price Table
CREATE TABLE IF NOT EXISTS Price (
    price_id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Unique identifier for each pricing entry',
    theatre_id INT NOT NULL COMMENT 'Identifier of the theatre for which the price is set',
    screen_id INT NOT NULL COMMENT 'Identifier of the screen within the theatre',
    movie_id INT NOT NULL COMMENT 'Identifier of the movie for which the price is set',
    format_id INT NOT NULL COMMENT 'Identifier of the movie format (e.g., 2D, 3D)',
    category_id INT NOT NULL COMMENT 'Identifier of the seat category',
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0) COMMENT 'Price amount for the specified criteria',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when the price was set',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp when the price was last updated',
    FOREIGN KEY (theatre_id) REFERENCES Theatre(theatre_id) ON DELETE CASCADE,
    FOREIGN KEY (screen_id) REFERENCES Screen(screen_id),
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id),
    FOREIGN KEY (format_id) REFERENCES Format(format_id),
    FOREIGN KEY (category_id) REFERENCES SeatCategory(category_id),
    UNIQUE (theatre_id, screen_id, movie_id, format_id, category_id) COMMENT 'Ensures unique pricing for each combination of theatre, screen, movie, format, and seat category'
) COMMENT 'Defines pricing for each seat category per show';

## Show seat Table
CREATE TABLE IF NOT EXISTS ShowSeat (
    show_seat_id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Unique identifier for each seat in a specific show',
    show_id INT NOT NULL COMMENT 'Identifier of the show to which the seat belongs',
    seat_id INT NOT NULL COMMENT 'Identifier of the seat',
    is_booked BOOLEAN DEFAULT FALSE COMMENT 'Indicates whether the seat is booked (TRUE) or available (FALSE)',
    version INT NOT NULL DEFAULT 1 COMMENT 'Version number for optimistic locking to handle concurrent updates',
    FOREIGN KEY (show_id) REFERENCES ShowTime(show_id) ON DELETE CASCADE,
    FOREIGN KEY (seat_id) REFERENCES Seat(seat_id) ON DELETE CASCADE,
    UNIQUE (show_id, seat_id) COMMENT 'Ensures each seat is uniquely associated with a show'
) COMMENT 'Tracks seat availability for each show';

## Booking Table
CREATE TABLE IF NOT EXISTS Booking (
    booking_id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Unique identifier for each booking transaction',
    show_id INT NOT NULL COMMENT 'Identifier of the show being booked',
    user_id INT NOT NULL COMMENT 'Identifier of the user making the booking',
    booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when the booking was made',
    total_amount DECIMAL(10, 2) NOT NULL CHECK (total_amount >= 0) COMMENT 'Total amount for the booking',
    status ENUM('confirmed', 'cancelled') DEFAULT 'confirmed' COMMENT 'Current status of the booking',
    version INT NOT NULL DEFAULT 1 COMMENT 'Version number for optimistic locking to handle concurrent updates',
    FOREIGN KEY (show_id) REFERENCES ShowTime(show_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    CHECK (status IN ('confirmed', 'cancelled'))
) COMMENT 'Stores booking transactions made by users';

## BookedSeat Table
CREATE TABLE IF NOT EXISTS BookedSeat (
    booked_seat_id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Unique identifier for each booked seat entry',
    booking_id INT NOT NULL COMMENT 'Identifier of the booking associated with the seat',
    show_seat_id INT NOT NULL COMMENT 'Identifier of the show seat that has been booked',
    FOREIGN KEY (booking_id) REFERENCES Booking(booking_id) ON DELETE CASCADE,
    FOREIGN KEY (show_seat_id) REFERENCES ShowSeat(show_seat_id) ON DELETE CASCADE,
    UNIQUE (booking_id, show_seat_id) COMMENT 'Ensures that each booked seat is uniquely associated with a booking'
) COMMENT 'Associates booked seats with bookings';

DROP PROCEDURE IF EXISTS GetShowsForTheatreAndDate;
DELIMITER //
CREATE PROCEDURE GetShowsForTheatreAndDate(
    IN p_theatre_name VARCHAR(100),
    IN p_show_date DATE
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'An error occurred while fetching shows.' AS ErrorMessage;
    END;

    START TRANSACTION;

    SELECT
        m.movie_name,
        m.language,
        m.rating,
        DATE_FORMAT(s.start_time, '%h:%i %p') AS start_time,
        f.format_name,
        IF(
            EXISTS (
                SELECT 1 FROM ShowSeat ss WHERE ss.show_id = s.show_id AND ss.is_booked = FALSE
            ),
            'Available',
            'Houseful'
        ) AS availability
    FROM
        ShowTime s
        JOIN Movie m ON s.movie_id = m.movie_id
        JOIN Format f ON s.format_id = f.format_id
        JOIN Theatre t ON s.theatre_id = t.theatre_id
    WHERE
        t.theatre_name = p_theatre_name
        AND s.show_date = p_show_date
        AND s.status = 'active'
    ORDER BY
        m.movie_name,
        s.start_time;

    COMMIT;
END;
//
DELIMITER ;

CREATE INDEX idx_show_is_booked ON ShowSeat(show_id, is_booked);