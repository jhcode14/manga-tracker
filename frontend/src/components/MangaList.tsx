import React, { useEffect, useState } from "react";
import MangaCard from "./MangaCard";
import axios from "axios";
import { Grid2, CircularProgress } from "@mui/material";
import { useSelector, useDispatch } from "react-redux";
import { triggerReload, selectAppReload } from "./store/appSlices";
import "../styles/mangaList.css";
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

const apiUrl = "/api/manga-list";

function MangaList() {
  const [noUpdateMangaList, setNoUpdateMangaList] = useState<Manga[]>([]);
  const [updatedMangaList, setUpdatedMangaList] = useState<Manga[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const shouldReload = useSelector(selectAppReload);
  const dispatch = useDispatch();

  useEffect(() => {
    const fetchMangaList = async () => {
      try {
        const response = await axios.get(apiUrl);

        console.log(response);

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
        if (shouldReload) {
          dispatch(triggerReload()); // This will set reload back to false
        }
      } catch (error) {
        console.log(error);
        setIsLoading(true);
      }
    };
    fetchMangaList();
  }, [shouldReload, dispatch]);

  return (
    <div>
      {isLoading ? (
        <CircularProgress />
      ) : (
        <div>
          <div className="manga-list-title">
            In Progress
            <div
              className="manga-list-title-icon"
              style={{ backgroundColor: "#F6B17A", color: "#2D3250" }}
            >
              {updatedMangaList.length}
            </div>
          </div>
          <Grid2
            container
            spacing={0}
            sx={{
              width: "auto",
              padding: "0 .5rem",
              maxWidth: "900px",
              margin: "0 auto",
            }}
          >
            {updatedMangaList.map((manga, index) => (
              <MangaCard
                key={manga.name}
                manga={manga}
                isFirst={index === 0}
                isLast={index === updatedMangaList.length - 1}
                isUpdated={true}
              />
            ))}
          </Grid2>

          <div className="manga-list-title">
            On the Shelf
            <div
              className="manga-list-title-icon"
              style={{ backgroundColor: "#7077A1", color: "#2D3250" }}
            >
              {noUpdateMangaList.length}
            </div>
          </div>
          <Grid2
            container
            spacing={0}
            sx={{
              width: "auto",
              padding: "0 .5rem",
              maxWidth: "900px",
              margin: "0 auto",
            }}
          >
            {noUpdateMangaList.map((manga, index) => (
              <MangaCard
                key={manga.name}
                manga={manga}
                isFirst={index === 0}
                isLast={index === noUpdateMangaList.length - 1}
                isUpdated={false}
              />
            ))}
          </Grid2>
        </div>
      )}
    </div>
  );
}

export default MangaList;
