import {
  Box,
  Button,
  Input,
  Modal,
  Checkbox,
  FormControlLabel,
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

const apiUrl = "/api/add-manga";

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "white",
  border: "2px solid #000",
  borderRadius: 5,
  boxShadow: 24,
  p: 4,
};

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
        <Box sx={style}>
          <Input
            type="text"
            placeholder="Enter Manga Url"
            value={url}
            onChange={onUrlChange}
          />
          <Button variant="contained" onClick={onUrlSubmit}>
            Add
          </Button>
          <FormControlLabel
            sx={{ color: "black" }}
            control={<Checkbox defaultChecked onChange={onCaughtUpChange} />}
            label="I've caught-up"
          />
        </Box>
      </Modal>
    </>
  );
}

export default AddForm;
