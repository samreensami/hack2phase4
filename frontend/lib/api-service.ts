import axios, { AxiosRequestConfig } from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

// Axios instance
export const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

// Attach token from localStorage
api.interceptors.request.use(
  (config) => {
    if (typeof window !== "undefined") {
      const token = localStorage.getItem("token");
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Auto logout / redirect on 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      if (typeof window !== "undefined") {
        console.log("Unauthorized, clearing token");
        localStorage.removeItem("token");
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

// Generic helper
export const apiClient = {
  get: async <T = any>(url: string, config?: AxiosRequestConfig) => {
    const res = await api.get<T>(url, config);
    return res.data;
  },
  post: async <T = any>(url: string, data?: any, config?: AxiosRequestConfig) => {
    const res = await api.post<T>(url, data, config);
    return res.data;
  },
  put: async <T = any>(url: string, data?: any, config?: AxiosRequestConfig) => {
    const res = await api.put<T>(url, data, config);
    return res.data;
  },
  delete: async <T = any>(url: string, config?: AxiosRequestConfig) => {
    const res = await api.delete<T>(url, config);
    return res.data;
  },
};

// Task-specific APIs
export const taskAPI = {
  getTasks: () => apiClient.get("/dashboard/tasks/"),
  createTask: (data: any) => apiClient.post("/dashboard/tasks/", data),
  updateTask: (id: number, data: any) => apiClient.put(`/dashboard/tasks/${id}`, data),
  deleteTask: (id: number) => apiClient.delete(`/dashboard/tasks/${id}`),
};
