export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const getAuthToken = () => {
    if (typeof window !== "undefined") {
        return localStorage.getItem("token");
    }
    return null;
};

export const setAuthToken = (token: string) => {
    localStorage.setItem("token", token);
};

export const clearAuthToken = () => {
    localStorage.removeItem("token");
};

async function handleResponse(response: Response) {
    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: "Unknown error" }));
        throw new Error(error.detail || response.statusText);
    }
    if (response.status === 204) return null;
    return response.json();
}

export const api = {
    async get(endpoint: string) {
        const token = getAuthToken();
        const headers: any = { "Content-Type": "application/json" };
        if (token) headers["Authorization"] = `Bearer ${token}`;

        const res = await fetch(`${API_BASE_URL}${endpoint}`, { headers });
        return handleResponse(res);
    },

    async post(endpoint: string, body: any, useFormData: boolean = false) {
        const token = getAuthToken();
        const headers: any = {};
        if (token) headers["Authorization"] = `Bearer ${token}`;

        let requestBody;
        if (useFormData) {
            requestBody = new URLSearchParams(body);
            headers["Content-Type"] = "application/x-www-form-urlencoded";
        } else {
            requestBody = JSON.stringify(body);
            headers["Content-Type"] = "application/json";
        }

        const res = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: "POST",
            headers,
            body: requestBody,
        });
        return handleResponse(res);
    },

    async put(endpoint: string, body: any) {
        const token = getAuthToken();
        const headers: any = { "Content-Type": "application/json" };
        if (token) headers["Authorization"] = `Bearer ${token}`;

        const res = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: "PUT",
            headers,
            body: JSON.stringify(body),
        });
        return handleResponse(res);
    },

    async delete(endpoint: string) {
        const token = getAuthToken();
        const headers: any = { "Content-Type": "application/json" };
        if (token) headers["Authorization"] = `Bearer ${token}`;

        const res = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: "DELETE",
            headers,
        });
        return handleResponse(res);
    },
};
