import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

// https://vite.dev/config/
export default defineConfig({
  server: {
    host: "0.0.0.0",
    port: 5173,
    proxy: {
      // Proxy API requests during development
      "/api": "http://localhost:3000",
    },
  },
  plugins: [react()],
});
