CREATE TABLE manga (
    manga_id VARCHAR(36) NOT NULL PRIMARY KEY,
    manga_name VARCHAR(50) NOT NULL,
    manga_link VARCHAR(200) NOT NULL,
    UNIQUE(manga_id, manga_name, manga_link)
);

CREATE TABLE episode (
    episode_id VARCHAR(36) NOT NULL PRIMARY KEY,
    manga_id VARCHAR(36) NOT NULL,
    episode_name VARCHAR(50) NOT NULL,
    episode_link VARCHAR(200) NOT NULL,
    episode_tag VARCHAR(10),
    UNIQUE(episode_id, episode_name, episode_link),
    CONSTRAINT fk_episode_manga_id
        FOREIGN KEY (manga_id)
            REFERENCES manga(manga_id)
);