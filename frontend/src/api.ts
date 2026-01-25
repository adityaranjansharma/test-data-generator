import axios from 'axios';

export const API_URL = 'http://localhost:3000';

const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use((config) => {
  const apiKey = localStorage.getItem('apiKey');
  if (apiKey) {
    config.headers['X-API-Key'] = apiKey;
  }
  return config;
});

export default api;
