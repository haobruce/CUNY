CREATE DATABASE IF NOT EXISTS movies;

DROP TABLE IF EXISTS movie_names;

CREATE TABLE movie_names
(
    movie_name varchar(100) NOT NULL
);

DROP TABLE IF EXISTS movie_ratings;
CREATE TABLE movie_ratings
(
	user_id int NOT NULL,
    movie_name varchar(100) NOT NULL,
    rating int NOT NULL
);

INSERT INTO movie_names (movie_name)
VALUES 
	('Star Wars: The Force Awakens'), 
	('Ride Along 2'),
    ('The Revenant'), 
    ('Kung Fu Panda 3'), 
    ('Deadpool'), 
    ('Zootopia');

SELECT * FROM movie_names;

INSERT INTO movie_ratings (user_id, movie_name, rating)
VALUES
	(1, 'Star Wars: The Force Awakens', 1), 
	(1, 'Ride Along 2', 2),
    (1, 'The Revenant', 5), 
    (1, 'Kung Fu Panda 3', 5), 
    (1, 'Deadpool', 5), 
    (1, 'Zootopia', 5),
	(2, 'Star Wars: The Force Awakens', 3), 
	(2, 'Ride Along 2', 1),
	(2, 'The Revenant', 3), 
	(2, 'Kung Fu Panda 3', 2), 
	(2, 'Deadpool', 4), 
	(2, 'Zootopia', 1),
	(3, 'Star Wars: The Force Awakens', 2), 
	(3, 'Ride Along 2', 1),
    (3, 'The Revenant', 4), 
    (3, 'Kung Fu Panda 3', 5), 
    (3, 'Deadpool', 2), 
    (3, 'Zootopia', 5),
	(4, 'Star Wars: The Force Awakens', 3), 
	(4, 'Ride Along 2', 3),
    (4, 'The Revenant', 1), 
    (4, 'Kung Fu Panda 3', 3), 
    (4, 'Deadpool', 2), 
    (4, 'Zootopia', 3),
	(5, 'Star Wars: The Force Awakens', 4), 
	(5, 'Ride Along 2', 4),
    (5, 'The Revenant', 2), 
    (5, 'Kung Fu Panda 3', 2), 
    (5, 'Deadpool', 3), 
    (5, 'Zootopia', 1);

SELECT * FROM movie_ratings;

-- TRUNCATE TABLE movie_names;
-- TRUNCATE TABLE movie_ratings;