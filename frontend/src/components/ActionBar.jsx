import { Button, Input } from "@mui/material";
import { useState } from "react";
import { isURL } from "validator";
import axios from "axios";

const apiUrl = "/api/add-manga";

async function AddUrl(url) {
  const response = await axios.post(apiUrl, {
    url: url,
    latest: false,
  });

  return response;
}

function ActionBar() {
  const [url, setUrl] = useState("");

  const onUrlChange = (event) => {
    setUrl(event.target.value);
  };

  const onUrlSubmit = async () => {
    if (isURL(url) == false) {
      alert("Please enter a valid URL");
      return;
    }
    AddUrl(url);
  };

  return (
    <>
      <Input
        type="text"
        placeholder="Enter Manga Url"
        value={url}
        onChange={onUrlChange}
      />
      <Button variant="contained" onClick={onUrlSubmit}>
        Add
      </Button>
    </>
  );
}

export default ActionBar;
