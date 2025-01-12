import { Button, Input } from "@mui/material";
import { useState } from "react";
import { isURL } from "validator";
import axios from "axios";

async function AddUrl(url) {
  //const apiUrl = process.env.BACKEND_API_URL + "/api/add-manga"; // FOR PROD
  const apiUrl = "http://localhost:5001/api/add-manga"; // FOR DEV

  axios
    .post(apiUrl, {
      manga_link: url,
      latest: false,
    })
    .then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });
}

function ActionBar() {
  const [url, setUrl] = useState("");

  const onUrlChange = (event) => {
    setUrl(event.target.value);
  };

  const onUrlSubmit = async () => {
    if (isURL(url) == false) {
      alert("Please enter a valid URL");
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
