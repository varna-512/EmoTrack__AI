import axios from "axios";

const api = axios.create({

  baseURL: "http://127.0.0.1:8000/api/",
});
export const getHistory = () => api.get("history/");

export const getDashboard = () => api.get("dashboard/");

export default api;