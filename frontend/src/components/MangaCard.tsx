import React from "react";
import axios from "axios";
import {
  ButtonBase,
  Button,
  Grid2,
  Box,
  Card,
  CardMedia,
  Typography,
} from "@mui/material";
import { useSelector, useDispatch } from "react-redux";
import { selectAppIsEditMode, triggerReload } from "./store/appSlices";
import DeleteIcon from "@mui/icons-material/Delete";

const MANGA_BASE_URL = "https://m.manhuagui.com";

function openNewTab(url) {
  window.open(url, "_blank")?.focus();
}

function MangaCard({ manga }) {
  const isEditMode = useSelector(selectAppIsEditMode);
  const dispatch = useDispatch();

  const handleDelete = async (mangaLink) => {
    try {
      const response = await axios.delete("/api/delete-manga", {
        data: { manga_link: mangaLink },
      });
      if (response.status === 200) {
        dispatch(triggerReload());
      }
    } catch (error) {
      console.error("Error deleting manga:", error);
    }
  };

  return (
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
                  openNewTab(MANGA_BASE_URL + manga.episode_currently_on.link)
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
              {isEditMode && (
                <Button
                  variant="contained"
                  color="error"
                  onClick={() => handleDelete(manga.link)}
                  startIcon={<DeleteIcon />}
                >
                  Delete
                </Button>
              )}
            </div>
          </Box>
        </Box>
      </Card>
    </Grid2>
  );
}

export default MangaCard;
