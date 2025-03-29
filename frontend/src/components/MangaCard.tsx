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
  Stack,
} from "@mui/material";
import { useSelector, useDispatch } from "react-redux";
import { selectAppIsEditMode, triggerReload } from "./store/appSlices";
import { Delete, RestartAlt, CheckCircle } from "@mui/icons-material";
import { Manga } from "./MangaList"; // Import the Manga type
import "../styles/mangaList.css";

const MANGA_BASE_URL = import.meta.env.VITE_MANGA_BASE_URL;

function openNewTab(url) {
  window.open(url, "_blank")?.focus();
}

interface MangaCardProps {
  manga: Manga;
  isFirst?: boolean;
  isLast?: boolean;
  isUpdated?: boolean;
  currentChapterNumber?: number;
  latestChapterNumber?: number;
}

function MangaCard({
  manga,
  isFirst,
  isLast,
  isUpdated,
  currentChapterNumber,
  latestChapterNumber,
}: MangaCardProps) {
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

  const handleUpdate = async (mangaLink, action) => {
    try {
      const response = await axios.put("/api/update-progress", {
        manga_link: mangaLink,
        action: action,
      });
      if (response.status === 200) {
        dispatch(triggerReload());
      }
    } catch (error) {
      console.error("Error restarting manga:", error);
    }
  };

  const progress =
    currentChapterNumber && latestChapterNumber
      ? (currentChapterNumber / latestChapterNumber) * 100
      : 0;

  return (
    <Stack gap={1} sx={{ width: "100%" }}>
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
          position: "relative", // Keep this for progress bar positioning
          "&:hover": {
            backgroundColor: "#4a4f75", // Slightly lighter on hover
          },
        }}
      >
        <div className="progress-bar-container">
          <div className="progress-bar" style={{ height: `${progress}%` }} />
        </div>

        <ButtonBase onClick={(event) => openNewTab(manga.link)}>
          <CardMedia
            component="img"
            sx={{
              width: (100 * 9) / 10,
              height: (140 * 9) / 10, // Add fixed height for consistency
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
            height: (140 * 9) / 10,
            justifyContent: "space-between",
          }}
        >
          <div style={{ display: "flex", flexDirection: "column" }}>
            <Typography
              component="div"
              sx={{
                fontSize: "1.2rem",
                color: "white",
                fontWeight: "600",
                textAlign: "left",
              }}
            >
              {manga.name}
            </Typography>
            <Typography
              component="div"
              sx={{
                alignSelf: "start",
                fontSize: ".8rem",
                color: "#FEFAF6",
                textAlign: "left",
              }}
            >
              {manga.episode_currently_on.name} ({currentChapterNumber}/
              {latestChapterNumber})
            </Typography>
          </div>

          <Box
            sx={{
              display: "flex",
              flexDirection: "column",
              gap: "0.5rem",
            }}
          >
            <div className="button-container">
              <div style={{ display: "flex", gap: "0.3rem" }}>
                <Button
                  variant="contained"
                  onClick={(event) =>
                    openNewTab(MANGA_BASE_URL + manga.episode_currently_on.link)
                  }
                  className="button"
                >
                  <Typography component="div" variant="body2">
                    Read
                  </Typography>
                </Button>

                <Button
                  className="button-outlined"
                  onClick={() => handleUpdate(manga.link, "restart")}
                >
                  <RestartAlt style={{ margin: 0 }} />
                </Button>
                {isUpdated && (
                  <Button
                    className="button-outlined"
                    onClick={() => handleUpdate(manga.link, "latest")}
                  >
                    <CheckCircle style={{ margin: 0 }} />
                  </Button>
                )}
              </div>
              {isEditMode && (
                <div style={{ marginLeft: "auto" }}>
                  <Button
                    onClick={() => handleDelete(manga.link)}
                    className="button-delete"
                  >
                    <Delete style={{ color: "#C63C51", margin: 0 }} />
                  </Button>
                </div>
              )}
            </div>
          </Box>
        </Box>
      </Card>
    </Stack>
  );
}

export default MangaCard;
