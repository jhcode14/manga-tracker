## GET /manga-list Example Output

{
"data": [
{
"episode_currently_on": {
"link": "https://m.manhuagui.com/comic/7580/772434.html",
"name": "第 247 话重置版",
"chapter_number": 247,
},
"episode_latest": {
"link": "/comic/7580/793549.html",
"name": "第 256 话重制版",
"chapter_number": 256,
},
"last_updated": "2024-12-26",
"link": "https://m.manhuagui.com/comic/7580/",
"name": "一拳超人",
"pfp_loc": "7580.jpg"
},
{
"episode_currently_on": {
"link": "https://m.manhuagui.com/comic/50667/733786.html",
"name": "第 3 话",
"chapter_number": 3,
},
"episode_latest": {
"link": "/comic/50667/789207.html",
"name": "一卷附錄",
"chapter_number": 1,
},
"last_updated": "2024-12-04",
"link": "https://m.manhuagui.com/comic/50667/",
"name": "每遭放逐就能获得技能的我，在 100 个世界大开第二轮无双",
"pfp_loc": "50667.jpg"
},
{
"episode_currently_on": {
"link": "/comic/36859/792123.html",
"name": "第 119 话",
"chapter_number": 119,
},
"episode_latest": {
"link": "/comic/36859/792123.html",
"name": "第 119 话",
"chapter_number": 119,
},
"last_updated": "2024-12-20",
"link": "https://m.manhuagui.com/comic/36859/",
"name": "怪兽 8 号",
"pfp_loc": "36859.jpg"
}
],
"mimetype": "application/json",
"status": 200
}

## POST /add-manga Example Input

{
"manga_link": "https://m.manhuagui.com/comic/53973/",
"latest": true
}

## PUT /update-progress Example Input

{
"manga_link": "https://m.manhuagui.com/comic/36859/",
"action": "latest" // or "restart"
}

## DELETE /delete-manga Example Input

{
"manga_link": "https://m.manhuagui.com/comic/36859/"
}
