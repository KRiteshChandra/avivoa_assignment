import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { sendChatMessage, logStructuredInteraction, fetchHistory } from "../api/api";

export const loadHistory = createAsyncThunk(
  "interactions/loadHistory",
  async () => {
    const data = await fetchHistory();
    return data.response;
  }
);

export const submitChat = createAsyncThunk(
  "interactions/submitChat",
  async (inputText, { dispatch }) => {
    const data = await sendChatMessage(inputText);
    dispatch(loadHistory()); // refresh list after any agent action
    return data.response;
  }
);

export const submitStructuredLog = createAsyncThunk(
  "interactions/submitStructuredLog",
  async (formData, { dispatch }) => {
    const data = await logStructuredInteraction(formData);
    dispatch(loadHistory());
    return data.response;
  }
);

const interactionsSlice = createSlice({
  name: "interactions",
  initialState: {
    history: [],
    chatLog: [], // { role: 'user'|'assistant', content: ... }
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(loadHistory.fulfilled, (state, action) => {
        state.history = action.payload || [];
      })
      .addCase(submitChat.pending, (state, action) => {
        state.loading = true;
        state.error = null;
        state.chatLog.push({ role: "user", content: action.meta.arg });
      })
      .addCase(submitChat.fulfilled, (state, action) => {
        state.loading = false;
        state.chatLog.push({ role: "assistant", content: action.payload });
      })
      .addCase(submitChat.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
        state.chatLog.push({ role: "assistant", content: { error: action.error.message } });
      })
      .addCase(submitStructuredLog.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(submitStructuredLog.fulfilled, (state) => {
        state.loading = false;
      })
      .addCase(submitStructuredLog.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  },
});

export default interactionsSlice.reducer;
