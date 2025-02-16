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
import { Manga } from "./MangaList"; // Import the Manga type
import "../styles/mangaList.css";

const MANGA_BASE_URL = "https://m.manhuagui.com";

function openNewTab(url) {
  window.open(url, "_blank")?.focus();
}

interface MangaCardProps {
  manga: Manga;
  isFirst?: boolean;
  isLast?: boolean;
}

function MangaCard({ manga, isFirst, isLast }: MangaCardProps) {
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
    <Grid2 size={{ xs: 12 }} sx={{ display: "block" }}>
      <Card
        sx={{
          display: "flex",
          backgroundColor: "#424769",
          width: "100%",
          borderRadius: 0, // Remove default border radius
          borderTop: isFirst ? "none" : "1px solid rgba(255, 255, 255, 0.12)", // Light divider
          borderTopLeftRadius: isFirst ? "0.5rem" : 0, // Round top corners of first card
          borderTopRightRadius: isFirst ? "0.5rem" : 0,
          borderBottomLeftRadius: isLast ? "0.5rem" : 0, // Round bottom corners of last card
          borderBottomRightRadius: isLast ? "0.5rem" : 0,
          "&:hover": {
            backgroundColor: "#4a4f75", // Slightly lighter on hover
          },
        }}
      >
        <ButtonBase onClick={(event) => openNewTab(manga.link)}>
          <CardMedia
            component="img"
            sx={{
              width: 100,
              height: 140, // Add fixed height for consistency
              flexShrink: 0, // Prevent image from shrinking
              paddingLeft: "0.5rem",
            }}
            image={"/images/" + manga.pfp_loc}
            alt={manga.name + " PFP"}
          />
        </ButtonBase>
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            flexGrow: 1, // Take up remaining width
            padding: ".5rem 1rem",
            height: 140,
            justifyContent: "space-between",
          }}
        >
          <ButtonBase
            onClick={(event) => openNewTab(manga.link)}
            sx={{ alignSelf: "flex-start" }} // Align text to left
          >
            <Typography
              component="div"
              sx={{ fontSize: "1.2rem", color: "white", fontWeight: "600" }}
            >
              {manga.name}
            </Typography>
          </ButtonBase>
          <Box
            sx={{
              display: "flex",
              flexDirection: "column",
              gap: "0.5rem",
            }}
          >
            <div className="button-container">
              <Button
                variant="contained"
                onClick={(event) =>
                  openNewTab(MANGA_BASE_URL + manga.episode_currently_on.link)
                }
                className="button"
              >
                <Typography component="div" variant="body2">
                  Continue
                </Typography>
              </Button>
              <Typography
                component="div"
                variant="subtitle1"
                sx={{
                  alignSelf: "center",
                  marginLeft: "0.5rem",
                  fontSize: "1rem",
                  color: "white",
                }}
              >
                {manga.episode_currently_on.name}
              </Typography>
            </div>
            <div className="button-container">
              <Button className="button-outlined">
                <Typography component="div" variant="body2">
                  Restart
                </Typography>
              </Button>
              <Button className="button-outlined">
                <Typography component="div" variant="body2">
                  Caught-up
                </Typography>
              </Button>
              {isEditMode && (
                <Button
                  onClick={() => handleDelete(manga.link)}
                  className="button-delete"
                >
                  <DeleteIcon style={{ color: "white", margin: 0 }} />
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
