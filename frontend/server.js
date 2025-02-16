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

app.post("/api/add-manga", async (req, res) => {
  try {
    const apiUrl =
      ((process.env && process.env.BACKEND_API_URL) ||
        "http://localhost:5001") + "/api/add-manga";

    console.log("Received request body:", req.body); // Debug log

    const response = await axios.post(
      apiUrl,
      {
        manga_link: req.body.manga_link,
        latest: req.body.latest,
      },
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    console.log("Backend response:", response.data); // Debug log
    res.json(response.data);
  } catch (error) {
    console.error("Error adding manga:", error.response?.data || error);
    res.status(error.response?.status || 500).json(
      error.response?.data || {
        error: "Internal Server Error",
      }
    );
  }
});

app.put("/api/update-progress", async (req, res) => {
  const apiUrl =
    ((process.env && process.env.BACKEND_API_URL) || "http://localhost:5001") +
    "/api/update-progress";

  console.log("Received request body:", req.body); // Debug log

  axios
    .put(
      apiUrl,
      {
        manga_link: req.body.manga_link,
        action: req.body.action,
      },
      {
        "Content-Type": "application/json",
      }
    )
    .then(function (response) {
      console.log(response.data);
      res.json(response.data);
    })
    .catch(function (error) {
      console.error("Error updating progress:", error.message);
      res
        .status(500)
        .json({ success: false, message: "Internal Server Error" });
    });
});

app.delete("/api/delete-manga", async (req, res) => {
  const apiUrl =
    ((process.env && process.env.BACKEND_API_URL) || "http://localhost:5001") +
    "/api/delete-manga";

  console.log("Received request body:", req.body); // Debug log

  axios
    .delete(apiUrl, {
      headers: {
        "Content-Type": "application/json",
      },
      data: {
        manga_link: req.body.manga_link,
      },
    })
    .then(function (response) {
      console.log(response.data);
      res.json(response.data);
    })
    .catch(function (error) {
      console.error("Error deleting manga:", error.message);
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
