import React, { useEffect, useState } from "react";
import axios from "axios";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import CircularProgress from "@mui/material/CircularProgress";
import { Avatar, ListItemAvatar } from "@mui/material";
import FiberNewIcon from "@mui/icons-material/FiberNew";

export interface Root {
  data: Manga[];
  mimetype: string;
  status: number;
}

export interface Manga {
  episode_currently_on: Episode;
  episode_latest: Episode;
  last_updated: string;
  link: string;
  name: string;
  pfp_loc: string;
}

export interface Episode {
  link: string;
  name: string;
}

function MangaList() {
  const [noUpdateMangaList, setNoUpdateMangaList] = useState<Manga[]>([]);
  const [updatedMangaList, setUpdatedMangaList] = useState<Manga[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchMangaList = async () => {
      try {
        //const apiUrl = process.env.BACKEND_API_URL + "/api/manga-list"; // FOR PROD
        const apiUrl = "http://localhost:5001/api/manga-list"; // FOR DEV
        const response = await axios.get(apiUrl);

        if (response.status !== 200) {
          // issues with response
          throw new Error(response.data);
        }

        const mangaList = response.data.data;
        setNoUpdateMangaList(
          mangaList.filter(
            (obj) => obj.episode_currently_on.link === obj.episode_latest.link
          )
        );
        setUpdatedMangaList(
          mangaList.filter(
            (obj) => obj.episode_currently_on.link !== obj.episode_latest.link
          )
        );

        setIsLoading(false);
      } catch (error) {
        console.log(error);
        setIsLoading(true);
      }
    };
    fetchMangaList();
  }, []);

  return (
    <div>
      {isLoading ? (
        <CircularProgress />
      ) : (
        <div>
          <div>
            New Episodes <FiberNewIcon />
          </div>
          <List>
            {updatedMangaList.map((manga) => (
              <ListItem key={manga.name}>
                <ListItemAvatar>
                  <Avatar alt="Manga PFP" src={"/images/" + manga.pfp_loc} />
                </ListItemAvatar>
                <ListItemText primary={manga.name} />
              </ListItem>
            ))}
          </List>
          <div>Other Episodes</div>
          <List>
            {noUpdateMangaList.map((manga) => (
              <ListItem key={manga.name}>
                <ListItemAvatar>
                  <Avatar alt="Manga PFP" src={"/images/" + manga.pfp_loc} />
                </ListItemAvatar>
                <ListItemText primary={manga.name} />
              </ListItem>
            ))}
          </List>
        </div>
      )}
    </div>
  );
}

export default MangaList;
