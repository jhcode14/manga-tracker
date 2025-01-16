import { configureStore } from "@reduxjs/toolkit";
import appReducer from "./appSlices";

const store = configureStore({
  reducer: {
    app: appReducer,
  },
});

export default store;
