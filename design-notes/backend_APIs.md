## /manga-list

#### Schema
{
    mangas: [
        {
            name: "一拳超人",
            link: "https://m.manhuagui.com/comic/7580/",
            episode_latest: {
                name: "第5话",
                link: "https://m.manhuagui.com/comic/7580/772479.html",
            }
            episode_currently_on: {
                name: "第2话",
                link: "https://m.manhuagui.com/comic/7580/772479.html",
            }
        },
        {
            name: "怪兽8号",
            link: "https://m.manhuagui.com/comic/36859/",
            episode_latest: {
                name: "第247话重置版",
                link: "https://m.manhuagui.com/comic/36859/772479.html",
            }
            episode_currently_on: {
                name: "第222话",
                link: "https://m.manhuagui.com/comic/36859/771479.html",
            }
        },
        ...
    ]
}

#### Notes
- Each manga will have 2 episode children - latest and currently_on