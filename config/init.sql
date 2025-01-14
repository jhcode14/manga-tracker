-- Create the manga table
CREATE TABLE IF NOT EXISTS manga (
    manga_id UUID PRIMARY KEY,
    manga_name TEXT NOT NULL,
    manga_link TEXT NOT NULL,
    manga_pfp_loc TEXT,

    UNIQUE (manga_name, manga_link)
);

-- Create the episode table
-- A manga should always have 1 c and one l episode
CREATE TABLE IF NOT EXISTS episode (
    episode_id UUID PRIMARY KEY,
    manga_id UUID NOT NULL,
    episode_name TEXT NOT NULL,
    episode_link TEXT NOT NULL,
    episode_tag TEXT, -- l=latest, c=currently_on
    episode_date_added TEXT,

    FOREIGN KEY (manga_id) REFERENCES manga(manga_id)
);

-- Insert test data into the manga table
INSERT INTO manga (manga_id, manga_name, manga_link) VALUES
('A2E7AD9B-6CD2-4C0C-BD33-EF7E6FD35909', '一拳超人', 'https://m.manhuagui.com/comic/7580/'),
--('4611FF5E-B6E8-4645-8E44-60A59204939B', '每遭放逐就能获得技能的我，在100个世界大开第二轮无双', 'https://m.manhuagui.com/comic/50667/'),
--('A6F6C87B-64BD-4338-B451-2DB9CC0CBE91', '怪兽8号', 'https://m.manhuagui.com/comic/36859/');

-- Insert test data into the episodes table
INSERT INTO episode (episode_id, manga_id, episode_name, episode_link, episode_tag, episode_date_added) VALUES
('F6F781B9-CA35-441A-9016-DDC5547F4D60', 'A2E7AD9B-6CD2-4C0C-BD33-EF7E6FD35909', '第247话重置版', 'https://m.manhuagui.com/comic/7580/772434.html', 'c', ''),
--('66F67364-32AC-4E41-9033-FE4EB1F3AC65', '4611FF5E-B6E8-4645-8E44-60A59204939B', '第3话', 'https://m.manhuagui.com/comic/50667/733786.html', 'c', ''),
--('3ACA1D34-0FAA-4DE2-A432-A6F42FC78B30', 'A6F6C87B-64BD-4338-B451-2DB9CC0CBE91', '第112话', 'https://m.manhuagui.com/comic/36859/771479.html', 'c', ''),
('8C7A3A12-95D8-4626-BAF5-82540C45FC16', 'A2E7AD9B-6CD2-4C0C-BD33-EF7E6FD35909', '第248话重置版', 'https://m.manhuagui.com/comic/7580/774842.html', 'l', ''),
--('28438C33-270D-422E-9DFB-B7E3F574FF96', '4611FF5E-B6E8-4645-8E44-60A59204939B', '第4话', 'https://m.manhuagui.com/comic/50667/748155.html', 'l', ''),
--('6229D309-C892-4289-9B8E-32918A3A0316', 'A6F6C87B-64BD-4338-B451-2DB9CC0CBE91', '第113话', 'https://m.manhuagui.com/comic/36859/773740.html', 'l', '');