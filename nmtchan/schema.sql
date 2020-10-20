CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username   VARCHAR,
	password   VARCHAR,
	level      INT
);

CREATE TABLE IF NOT EXISTS post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent  INT,
	board   VARCHAR,
	subject VARCHAR,
	body    VARCHAR,
    thumb   VARCHAR,
	media   VARCHAR,
    last_updated TEXT,
    created TEXT
);

CREATE TABLE IF NOT EXISTS reply (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    opID INTEGER NOT NULL,
    replyID INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS code (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    accessCode VARCHAR
);

DROP TABLE IF EXISTS board;
CREATE TABLE board (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR,
    category VARCHAR,
    link VARCHAR
);
INSERT INTO board ("name", "category", "link")
VALUES 
    ("technology", "interests", "/tech/"),
    ("auto", "interests", "/auto/"),
    ("celebrities", "interests", "/celeb/"),

    ("drawing", "creative", "/draw/"),
    ("photography", "creative", "/photo/"),
    ("music", "creative", "/mu/"),
    ("worksafe gif", "creative", "/wsg/"),

    ("computer science", "classes", "/cs/"),
    ("math", "classes", "/math/"),
    ("chem", "classes", "/chem/"),

    ("random", "nsfw", "/b/"),
    ("adult gif", "nsfw", "/gif/"),
    ("women", "nsfw", "/w/"),
    ("men", "nsfw", "/m/");