import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  Avatar,
  ButtonBase,
  ListItemAvatar,
  Button,
  Grid2,
  Box,
  Card,
  CardMedia,
  Typography,
  List,
  ListItem,
  ListItemText,
  CircularProgress,
} from "@mui/material";
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

function openNewTab(url) {
  window.open(url, "_blank")?.focus();
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
            <Grid2 container spacing={0.5}>
              {updatedMangaList.map((manga) => (
                <Grid2 size={{ xs: 6, md: 12 }}>
                  <Card sx={{ display: "flex", backgroundColor: "gray" }}>
                    <ButtonBase onClick={(event) => openNewTab(manga.link)}>
                      <CardMedia
                        component="img"
                        sx={{ width: 75 }}
                        image={"/images/" + manga.pfp_loc}
                        alt={manga.name + " PFP"}
                      />
                    </ButtonBase>
                    <Box sx={{ display: "flex", flexDirection: "column" }}>
                      <ButtonBase onClick={(event) => openNewTab(manga.link)}>
                        <Typography component="div" variant="h5">
                          {manga.name}
                        </Typography>
                      </ButtonBase>
                      <Box sx={{ display: "flex", flexDirection: "row" }}>
                        <Button
                          variant="contained"
                          onClick={(event) =>
                            openNewTab(manga.episode_currently_on.link)
                          }
                        >
                          <Typography component="div" variant="subtitle1">
                            {"Read " + manga.episode_currently_on.name}
                          </Typography>
                        </Button>
                        <Button variant="outlined">
                          <Typography component="div" variant="subtitle1">
                            Restart
                          </Typography>
                        </Button>
                        <Button variant="outlined">
                          <Typography component="div" variant="subtitle1">
                            I'm Caught-up
                          </Typography>
                        </Button>
                      </Box>
                    </Box>
                  </Card>
                </Grid2>
              ))}
            </Grid2>
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
