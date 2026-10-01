import axios from 'axios';

const API_BASE_URL = '/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

export const predictFault = async (telemetry) => {
  const response = await apiClient.post('/predict/', telemetry);
  return response.data;
};

export const fetchDashboardStats = async () => {
  const response = await apiClient.get('/dashboard/stats/');
  return response.data;
};

export const fetchPredictionHistory = async (limit = 15) => {
  const response = await apiClient.get(`/history/?limit=${limit}`);
  return response.data;
};

export const clearPredictionHistory = async () => {
  const response = await apiClient.delete('/history/');
  return response.data;
};

export const simulateTelemetry = async (scenario = 'normal') => {
  const response = await apiClient.get(`/telemetry/simulate/?scenario=${scenario}`);
  return response.data;
};

export default apiClient;
