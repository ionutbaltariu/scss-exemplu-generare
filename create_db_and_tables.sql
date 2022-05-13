CREATE DATABASE generated_db;
USE generated_db;

CREATE TABLE `Books` (
`isbn` varchar(100) NOT NULL,
`title` varchar(100) NOT NULL,
`year_of_publishing` int(11) NOT NULL,
`authors_fk` int(11) NOT NULL,
UNIQUE KEY `books_un_1` (`title`, `year_of_publishing`),
PRIMARY KEY (`isbn`)
);

CREATE TABLE `authors` (
`author_id` int(11) NOT NULL,
`first_name` varchar(100) NOT NULL,
`last_name` varchar(100) NOT NULL,
UNIQUE KEY `one_to_one_constr` (`author_id`),
PRIMARY KEY (`author_id`)
);


ALTER TABLE `Books` ADD CONSTRAINT FOREIGN KEY (`authors_fk`) REFERENCES `authors` (`author_id`);
