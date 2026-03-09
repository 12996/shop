import { request } from "./http";

export type WebAuthUser = {
  id: number;
  username: string;
  phone: string | null;
  avatar: string | null;
  role: "user" | "merchant";
  status: string;
  email: string;
};

export type WebAuthPayload = {
  token: string;
  user: WebAuthUser;
};

export type UpdateProfilePayload = {
  username?: string;
  phone?: string;
  email?: string;
};

export function register(payload: {
  username: string;
  password: string;
  phone: string;
  email: string;
  role: "user" | "merchant";
}) {
  return request<WebAuthUser>("/api/auth/register", {
    method: "POST",
    body: payload,
  });
}

export function loginWithPassword(payload: { username: string; password: string }) {
  return request<WebAuthPayload>("/api/auth/login/password", {
    method: "POST",
    body: payload,
  });
}

export function fetchProfile() {
  return request<WebAuthUser>("/api/auth/profile");
}

export function updateProfile(payload: UpdateProfilePayload) {
  return request<WebAuthUser>("/api/auth/profile", {
    method: "PUT",
    body: payload,
  });
}

export function uploadAvatar(file: File) {
  const formData = new FormData();
  formData.append("avatar", file);
  return request<WebAuthUser>("/api/auth/avatar", {
    method: "POST",
    body: formData,
  });
}

export function updatePassword(payload: { old_password: string; new_password: string }) {
  return request<null>("/api/auth/password", {
    method: "PUT",
    body: payload,
  });
}
