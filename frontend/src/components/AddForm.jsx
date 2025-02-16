import {
  Box,
  Button,
  Input,
  Modal,
  Checkbox,
  FormControlLabel,
  Typography,
} from "@mui/material";
import { useState } from "react";
import { isURL } from "validator";
import axios from "axios";
import {
  closeForm,
  triggerReload,
  selectAppIsAddOverlayOpen,
} from "./store/appSlices";
import { useSelector, useDispatch } from "react-redux";
import "../styles/addForm.css";
const apiUrl = "/api/add-manga";

async function AddUrl(url, caughtUp) {
  try {
    const response = await axios.post(
      apiUrl,
      {
        manga_link: url,
        latest: caughtUp,
      },
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    console.log("AddUrl Response:", response);
    return response;
  } catch (error) {
    console.error("AddUrl Error:", error.response?.data || error);
    throw error;
  }
}

function AddForm() {
  const [url, setUrl] = useState("");
  const [caughtUp, setCaughtUp] = useState(true);
  const dispatch = useDispatch();
  const isAddOverlayOpen = useSelector(selectAppIsAddOverlayOpen);

  const onUrlChange = (event) => {
    setUrl(event.target.value);
  };

  const onCaughtUpChange = (event) => {
    setCaughtUp(event.target.checked);
  };

  const onUrlSubmit = async () => {
    if (!isURL(url)) {
      alert("Please enter a valid URL");
      return;
    }

    try {
      const response = await AddUrl(url, caughtUp);
      console.log("Submit Response:", response);

      if (response.status === 200) {
        dispatch(triggerReload());
        dispatch(closeForm());
        setUrl("");
      }
    } catch (error) {
      alert(error.response?.data?.error || "Failed to add manga");
    }
  };

  return (
    <>
      <Modal
        open={isAddOverlayOpen}
        onClose={() => dispatch(closeForm())}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box className="add-form">
          <Typography
            sx={{ color: "white", fontSize: "1.3rem", fontWeight: "500" }}
          >
            Add Manga
          </Typography>
          <Box
            sx={{ display: "flex", flexDirection: "row", paddingTop: "1rem" }}
          >
            <Input
              type="text"
              placeholder="Enter Manga Url"
              value={url}
              onChange={onUrlChange}
              sx={{
                backgroundColor: "#7077A1",
                color: "white",
                height: "2.5rem",
                borderRadius: "0.3rem 0 0 0.3rem",
                flexGrow: 1,
              }}
            />
            <Button
              onClick={onUrlSubmit}
              sx={{
                backgroundColor: "#F6B17A",
                color: "#2D3250",
                height: "2.4rem",
                borderRadius: "0 0.3rem 0.3rem 0",
                marginLeft: "-1px",
              }}
            >
              Add
            </Button>
          </Box>
          <FormControlLabel
            sx={{ color: "white" }}
            control={<Checkbox defaultChecked onChange={onCaughtUpChange} />}
            label="I'm on the latest chapter"
          />
        </Box>
      </Modal>
    </>
  );
}

export default AddForm;
