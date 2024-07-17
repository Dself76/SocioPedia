-- Create the database
CREATE DATABASE newsociopedia;

-- Use the newly created database
USE newsociopedia;

-- Create the users table
CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(50) NULL,
    last_name VARCHAR(50) NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    country VARCHAR(50) NULL,
    state VARCHAR(50) NULL,
    county VARCHAR(50) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sex VARCHAR(10) NULL,
    PRIMARY KEY (id)
);

-- Create the address table
CREATE TABLE address (
    address_id INT NOT NULL AUTO_INCREMENT,
    user_id INT,
    country VARCHAR(50),
    state VARCHAR(50),
    county VARCHAR(50),
    PRIMARY KEY (address_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (country) REFERENCES users(country),
    FOREIGN KEY (state) REFERENCES users(state),
    FOREIGN KEY (county) REFERENCES users(county)
);
-- Create the posts table
CREATE TABLE posts (
    post_id INT NOT NULL AUTO_INCREMENT,
    user_id INT,
    title VARCHAR(255),
    content TEXT,
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    post VARCHAR(255),
    PRIMARY KEY (post_id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create the general_posts table
CREATE TABLE general_posts (
    post_id INT NOT NULL AUTO_INCREMENT,  -- Unique identifier for each post, automatically incremented
    title VARCHAR(255),                  -- Title of the post, optional/ eventually I will keep this in to track everypost,
    content TEXT,                        -- Content of the post, text type to accommodate longer entries,
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Timestamp of when the post was made, defaults to the current time/ I think timezone shouldnt matter
    PRIMARY KEY (post_id),               -- Sets post_id as the primary key
    INDEX (posted_at)                    -- Index on the posted_at column for better performance on timestamp-based queries/should query faster
);


-- Create the group_vote table
CREATE TABLE group_vote (
    group_id INT NOT NULL AUTO_INCREMENT,
    group_name VARCHAR(255) NOT NULL,
    group_type ENUM('friends', 'family', 'business') NOT NULL,
    description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (group_id)
);
CREATE TABLE issues (
    issue_id INT NOT NULL AUTO_INCREMENT,
    group_id INT,
    issue_name VARCHAR(255) NOT NULL,
    issue_description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (issue_id),
    FOREIGN KEY (group_id) REFERENCES group_vote(group_id)
);
