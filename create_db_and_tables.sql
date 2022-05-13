CREATE DATABASE generated_db;
USE generated_db;

CREATE TABLE `Books` (
`isbn` varchar(100) NOT NULL,
`title` varchar(100) NOT NULL,
`year_of_publishing` int(11) NOT NULL,
UNIQUE KEY `books_un_1` (`title`, `year_of_publishing`),
PRIMARY KEY (`isbn`)
);

CREATE TABLE `Authors` (
`author_id` int(11) NOT NULL,
`first_name` varchar(100) NOT NULL,
`last_name` varchar(100) NOT NULL,
PRIMARY KEY (`author_id`)
);

CREATE TABLE `Books_Authors` (
`id` int(11) NOT NULL,
`isbn` int(11) NOT NULL,
`author_id` int(11) NOT NULL,
PRIMARY KEY (`id`)
);


ALTER TABLE `Books_Authors` ADD CONSTRAINT FOREIGN KEY (`isbn`) REFERENCES `Books` (`isbn`);
ALTER TABLE `Books_Authors` ADD CONSTRAINT FOREIGN KEY (`author_id`) REFERENCES `Authors` (`author_id`);
