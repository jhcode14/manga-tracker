import { Box, Button, Input, Modal } from "@mui/material";
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

async function AddUrl(url) {
  const response = await axios.post(apiUrl, {
    url: url,
    latest: false,
  });

  return response;
}

function AddForm() {
  const [url, setUrl] = useState("");
  const dispatch = useDispatch();
  const isAddOverlayOpen = useSelector(selectAppIsAddOverlayOpen);

  const onUrlChange = (event) => {
    setUrl(event.target.value);
  };

  const onUrlSubmit = async () => {
    if (isURL(url) == false) {
      alert("Please enter a valid URL");
      return;
    }
    const response = await AddUrl(url);
    console.log(response);
    if (response.status == 200) {
      dispatch(triggerReload());
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
        </Box>
      </Modal>
    </>
  );
}

export default AddForm;
