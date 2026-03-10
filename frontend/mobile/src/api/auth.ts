import { request } from "./http";

export type AuthUser = {
  id: number;
  username: string;
  phone: string | null;
  avatar: string | null;
  role: string;
  status: string;
  email: string;
};

export type AuthPayload = {
  token: string;
  user: AuthUser;
};

export type RegisterPayload = {
  username: string;
  password: string;
  phone?: string;
  email?: string;
};

export type ProfileUpdatePayload = {
  username?: string;
  phone?: string;
  email?: string;
};

export type PasswordUpdatePayload = {
  old_password: string;
  new_password: string;
};

export function register(payload: RegisterPayload) {
  return request<AuthUser>("/api/auth/register", {
    method: "POST",
    body: payload,
  });
}

export function loginWithPassword(payload: { username: string; password: string }) {
  return request<AuthPayload>("/api/auth/login/password", {
    method: "POST",
    body: payload,
  });
}

export function loginWithCode(payload: { phone: string; code: string }) {
  return request<AuthPayload>("/api/auth/login/code", {
    method: "POST",
    body: payload,
  });
}

export function fetchProfile() {
  return request<AuthUser>("/api/auth/profile");
}

export function updateProfile(payload: ProfileUpdatePayload) {
  return request<AuthUser>("/api/auth/profile", {
    method: "PUT",
    body: payload,
  });
}

export function uploadAvatar(file: File) {
  const formData = new FormData();
  formData.append("avatar", file);
  return request<AuthUser>("/api/auth/avatar", {
    method: "POST",
    body: formData,
  });
}

export function updatePassword(payload: PasswordUpdatePayload) {
  return request<null>("/api/auth/password", {
    method: "PUT",
    body: payload,
  });
}
