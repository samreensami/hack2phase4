import { api } from "./api-service";

export const fetchCsrfToken = async () => {
  await api.get("/api/auth/csrf");
};

export const signIn = {
  email: async ({
    email,
    password,
  }: {
    email: string;
    password: string;
  }) => {
    try {
      await api.post("/auth/login", { email, password });
      return { error: null };
    } catch (err: any) {
      return {
        error: { message: err.response?.data?.detail || "Login failed" },
      };
    }
  },
};

export const signOut = async () => {
  await api.post("/auth/logout");
};
