import React, { useState } from "react";
import {
  AppBar,
  Box,
  Toolbar,
  IconButton,
  Typography,
  Menu,
  MenuList,
  Container,
  Button,
  MenuItem,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import {
  openForm,
  toggleEditMode,
  selectAppIsEditMode,
} from "./store/appSlices";
import { useDispatch, useSelector } from "react-redux";
import "../styles/header.css";

function Header() {
  const [anchorElNav, setAnchorElNav] = useState<HTMLElement | null>(null);
  const dispatch = useDispatch();
  const isEditMode = useSelector(selectAppIsEditMode);

  const handleOpenNavMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElNav(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const handleAddButton = () => {
    setAnchorElNav(null);
    dispatch(openForm());
  };

  const handleEditButton = () => {
    setAnchorElNav(null);
    dispatch(toggleEditMode());
  };

  return (
    <AppBar
      position="static"
      style={{ backgroundColor: "#424769", boxShadow: "none" }}
    >
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          <img
            src="/436774.svg"
            alt="logo"
            style={{ width: "2.5vh", paddingRight: "1vh" }}
          ></img>
          <Typography
            variant="h5"
            noWrap
            component="a"
            href="#app-bar-with-responsive-menu"
            sx={{
              mr: 2,
              display: { xs: "flex", md: "flex" },
              flexGrow: 1,
              letterSpacing: "-.02rem",
              fontWeight: 700,
              color: "inherit",
              textDecoration: "none",
            }}
          >
            MANGA SHELF
          </Typography>
          <Box sx={{ flexGrow: 1, display: { xs: "none", md: "flex" } }}>
            <Button
              key={"Add"}
              onClick={() => dispatch(openForm())}
              sx={{ my: 2, color: "white", display: "block" }}
            >
              {"Add"}
            </Button>
            <Button
              key={"Edit"}
              onClick={() => dispatch(toggleEditMode())}
              sx={{
                my: 2,
                color: isEditMode ? "red" : "white",
                display: "block",
              }}
            >
              {isEditMode ? "Editing..." : "Edit"}
            </Button>
          </Box>
          <Box sx={{ flexGrow: 0, display: { xs: "flex", md: "none" } }}>
            <IconButton
              size="large"
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleOpenNavMenu}
              color="inherit"
            >
              <MenuIcon />
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorElNav}
              anchorOrigin={{
                vertical: "bottom",
                horizontal: "right",
              }}
              keepMounted
              transformOrigin={{
                vertical: "top",
                horizontal: "right",
              }}
              open={Boolean(anchorElNav)}
              onClose={handleCloseNavMenu}
              sx={{
                display: { xs: "block", md: "none" },
                paper: { backgroundColor: "#7077A1" },
              }}
              classes={{ paper: "header-paper" }}
            >
              <MenuItem key={"Add"} onClick={handleAddButton}>
                <Typography sx={{ textAlign: "center" }}>{"Add"}</Typography>
              </MenuItem>
              <MenuItem key={"Edit"} onClick={handleEditButton}>
                <Typography
                  sx={{
                    textAlign: "center",
                    color: isEditMode ? "#F6B17A" : "white",
                  }}
                >
                  {isEditMode ? "Editing..." : "Edit"}
                </Typography>
              </MenuItem>
            </Menu>
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
}

export default Header;
