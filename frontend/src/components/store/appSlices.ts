import { createSlice } from "@reduxjs/toolkit";

const initialState = { isAddOverlayOpen: false, reload: false };

const appSlice = createSlice({
  name: "app",
  initialState,
  reducers: {
    openForm: (state) => {
      state.isAddOverlayOpen = true;
    },
    closeForm: (state) => {
      state.isAddOverlayOpen = false;
    },
    triggerReload: (state) => {
      state.reload = !state.reload;
    },
  },
});

export const { openForm, closeForm, triggerReload } = appSlice.actions;
export default appSlice.reducer;

export const selectAppIsAddOverlayOpen = (state) => state.app.isAddOverlayOpen;
export const selectAppReload = (state) => state.app.reload;
