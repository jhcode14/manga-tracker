import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  isAddOverlayOpen: false,
  reload: false,
  isEditMode: false,
};

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
    toggleEditMode: (state) => {
      state.isEditMode = !state.isEditMode;
    },
  },
});

export const { openForm, closeForm, triggerReload, toggleEditMode } =
  appSlice.actions;
export default appSlice.reducer;

export const selectAppIsAddOverlayOpen = (state) => state.app.isAddOverlayOpen;
export const selectAppReload = (state) => state.app.reload;
export const selectAppIsEditMode = (state) => state.app.isEditMode;
