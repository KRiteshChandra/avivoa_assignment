import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: { "Content-Type": "application/json" },
});

export const sendChatMessage = (input_text) =>
  api.post("/interaction/chat", { input_text }).then((res) => res.data);

export const logStructuredInteraction = (payload) =>
  api.post("/interaction/log", payload).then((res) => res.data);

export const fetchHistory = () =>
  api.get("/interaction/history").then((res) => res.data);

export default api;
