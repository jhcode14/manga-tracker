import express from "express";
import axios from "axios";

const app = express();

app.use(express.json());

// GET manga list
app.get("/api/manga-list", async (req, res) => {
  try {
    const apiUrl =
      ((process.env && process.env.BACKEND_API_URL) ||
        "http://localhost:5001") + "/api/manga-list";

    console.log(apiUrl);

    // Fetch data from backend API
    const response = await axios.get(apiUrl);

    // Optionally process or transform the data here
    res.json({ success: true, data: response.data.data });
  } catch (error) {
    console.error("Error fetching manga list:", error);
    res.status(500).json({ success: false, message: "Internal Server Error" });
  }
});

// TODO: POST add manga
app.post("/api/add-manga", async (req, res) => {
  const { url, latest } = req.body;
  const apiUrl =
    (process.env && process.env.VITE_BACKEND_API_URL) ||
    "http://localhost:5001" + "/api/add-manga";

  // Forward POST request to backend API
  axios
    .post(apiUrl, {
      manga_link: url,
      latest: latest,
    })
    .then(function (response) {
      console.log(response);
      res.json(response);
    })
    .catch(function (error) {
      console.error("Error adding manga:", error.message);
      res
        .status(500)
        .json({ success: false, message: "Internal Server Error" });
    });
});

// Start Express server
const PORT = (import.meta.env && import.meta.env.EXPRESS_SERVER_PORT) || 3000;
app.listen(PORT, () => {
  console.log(`Express server running on http://localhost:${PORT}`);
});
