import React, { useEffect, useState } from "react";
import axios from "axios";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import CircularProgress from "@mui/material/CircularProgress";

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
  const [mangaList, setMangaList] = useState<Manga[]>([]);
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

        setMangaList(response.data.data);

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
        <List>
          {mangaList.map((manga) => (
            <ListItem key={manga.name}>
              <ListItemText primary={manga.name} />
            </ListItem>
          ))}
        </List>
      )}
    </div>
  );
}

export default MangaList;
