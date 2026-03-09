const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";

type RequestOptions = {
  method?: string;
  body?: BodyInit | Record<string, unknown> | null;
  headers?: Record<string, string>;
};

function getAuthHeaders() {
  const token = window.localStorage.getItem("mobile-auth-token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function parseResponse<T>(response: Response): Promise<T> {
  if (response.status === 204) {
    return null as T;
  }

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data?.detail ?? "请求失败");
  }

  return data as T;
}

export async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { method = "GET", body, headers = {} } = options;
  const isFormData = body instanceof FormData;

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers: {
      ...getAuthHeaders(),
      ...(isFormData ? {} : { "Content-Type": "application/json" }),
      ...headers,
    },
    body: body == null ? null : isFormData || typeof body === "string" ? body : JSON.stringify(body),
    credentials: "include",
  });

  return parseResponse<T>(response);
}
