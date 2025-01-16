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

const apiUrl = "/api/manga-list";

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
          <Grid2
            container
            spacing={0.5}
            sx={{
              width: "auto",
            }}
          >
            {updatedMangaList.map((manga) => (
              <Grid2 size={{ xs: 12, md: 6 }} sx={{ display: "block" }}>
                <Card sx={{ display: "flex", backgroundColor: "gray" }}>
                  <ButtonBase onClick={(event) => openNewTab(manga.link)}>
                    <CardMedia
                      component="img"
                      sx={{ width: 120 }}
                      image={"/images/" + manga.pfp_loc}
                      alt={manga.name + " PFP"}
                    />
                  </ButtonBase>
                  <Box sx={{ display: "flex", flexDirection: "column" }}>
                    <ButtonBase onClick={(event) => openNewTab(manga.link)}>
                      <Typography component="div" variant="h6">
                        {manga.name}
                      </Typography>
                    </ButtonBase>
                    <Typography component="div" variant="subtitle1">
                      {"At: " + manga.episode_currently_on.name}
                    </Typography>
                    <Box sx={{ display: "flex", flexDirection: "row" }}>
                      <div>
                        <Button
                          variant="contained"
                          onClick={(event) =>
                            openNewTab(manga.episode_currently_on.link)
                          }
                        >
                          <Typography component="div" variant="body2">
                            Continue
                          </Typography>
                        </Button>
                        <Button variant="outlined">
                          <Typography component="div" variant="body2">
                            Restart
                          </Typography>
                        </Button>
                        <Button variant="outlined">
                          <Typography component="div" variant="body2">
                            I'm Caught-up
                          </Typography>
                        </Button>
                      </div>
                    </Box>
                  </Box>
                </Card>
              </Grid2>
            ))}
          </Grid2>
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
