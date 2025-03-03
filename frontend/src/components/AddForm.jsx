import {
  Box,
  Button,
  Input,
  Modal,
  Checkbox,
  FormControlLabel,
  Typography,
} from "@mui/material";
import { useRef } from "react";
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
  const dispatch = useDispatch();
  const isAddOverlayOpen = useSelector(selectAppIsAddOverlayOpen);
  const urlRef = useRef("");
  const caughtUpRef = useRef(true);

  const onUrlSubmit = async () => {
    if (!isURL(urlRef.current)) {
      alert("Please enter a valid URL");
      return;
    }

    try {
      const response = await AddUrl(urlRef.current, caughtUpRef.current);
      console.log("Submit Response:", response);

      if (response.status === 200) {
        dispatch(triggerReload());
        dispatch(closeForm());
        urlRef.current = "";
        caughtUpRef.current = true;
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
              value={urlRef.current}
              onChange={(e) => (urlRef.current = e.target.value)}
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
            control={
              <Checkbox
                defaultChecked
                onChange={(e) => (caughtUpRef.current = e.target.checked)}
              />
            }
            label="I'm on the latest chapter"
          />
        </Box>
      </Modal>
    </>
  );
}

export default AddForm;
