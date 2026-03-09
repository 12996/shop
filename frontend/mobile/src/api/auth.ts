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
