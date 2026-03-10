const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";
const DISCONNECT_MESSAGE = "error:与服务器断连";

type RequestOptions = {
  method?: string;
  body?: BodyInit | Record<string, unknown> | null;
  headers?: Record<string, string>;
};

function getAuthHeaders() {
  const token = window.localStorage.getItem("mobile-auth-token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

function formatApiError(data: unknown): string {
  if (typeof data === "string" && data.trim()) {
    return data;
  }

  if (!data || typeof data !== "object") {
    return DISCONNECT_MESSAGE;
  }

  const detail = (data as { detail?: unknown }).detail;
  if (typeof detail === "string" && detail.trim()) {
    return detail;
  }

  const entries = Object.entries(data as Record<string, unknown>);
  const message = entries
    .map(([field, value]) => {
      if (Array.isArray(value)) {
        return `${field}: ${value.map((item) => String(item)).join(" ")}`;
      }
      return `${field}: ${String(value)}`;
    })
    .join("; ");

  return message || DISCONNECT_MESSAGE;
}

async function parseResponse<T>(response: Response): Promise<T> {
  if (response.status === 204) {
    return null as T;
  }

  const rawText = await response.text();
  let data: unknown = null;
  if (rawText) {
    try {
      data = JSON.parse(rawText);
    } catch {
      data = rawText;
    }
  }

  if (!response.ok) {
    if (!rawText) {
      throw new Error(DISCONNECT_MESSAGE);
    }
    throw new Error(formatApiError(data));
  }

  if (data === null) {
    throw new Error(DISCONNECT_MESSAGE);
  }

  if (typeof data === "string") {
    throw new Error(data);
  }

  return data as T;
}

export async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { method = "GET", body, headers = {} } = options;
  const isFormData = body instanceof FormData;

  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      method,
      headers: {
        ...getAuthHeaders(),
        ...(isFormData ? {} : { "Content-Type": "application/json" }),
        ...headers,
      },
      body: body == null ? null : isFormData || typeof body === "string" ? body : JSON.stringify(body),
      credentials: "include",
    });
  } catch {
    throw new Error(DISCONNECT_MESSAGE);
  }

  return parseResponse<T>(response);
}
