import { request } from "./http";

export type Announcement = {
  id: number;
  title: string;
  content: string;
  status: "draft" | "published";
  publisher: number | null;
  published_at: string | null;
  created_at: string;
};

export type Recommendation = {
  id: number;
  product: number;
  product_name?: string;
  sort_order: number;
  status: "enabled" | "disabled";
  created_at?: string;
};

export type AnnouncementPayload = {
  title: string;
  content: string;
  status: "draft" | "published";
};

export type RecommendationPayload = {
  product: number;
  sort_order: number;
  status: "enabled" | "disabled";
};

export type StatisticsOverview = {
  order_count: number;
  completed_order_count: number;
  sales_amount: string;
};

export type HotProduct = {
  product_id: number;
  product_name: string;
  sales_count: number;
  order_count: number;
};

export function fetchAnnouncements() {
  return request<Announcement[]>("/api/admin/announcements");
}

export function createAnnouncement(payload: AnnouncementPayload) {
  return request<Announcement>("/api/admin/announcements", {
    method: "POST",
    body: payload,
  });
}

export function updateAnnouncement(announcementId: number, payload: AnnouncementPayload) {
  return request<Announcement>(`/api/admin/announcements/${announcementId}`, {
    method: "PUT",
    body: payload,
  });
}

export function deleteAnnouncement(announcementId: number) {
  return request<null>(`/api/admin/announcements/${announcementId}`, {
    method: "DELETE",
  });
}

export function fetchRecommendations() {
  return request<Recommendation[]>("/api/admin/recommendations");
}

export function createRecommendation(payload: RecommendationPayload) {
  return request<Recommendation>("/api/admin/recommendations", {
    method: "POST",
    body: payload,
  });
}

export function updateRecommendation(recommendationId: number, payload: RecommendationPayload) {
  return request<Recommendation>(`/api/admin/recommendations/${recommendationId}`, {
    method: "PUT",
    body: payload,
  });
}

export function deleteRecommendation(recommendationId: number) {
  return request<null>(`/api/admin/recommendations/${recommendationId}`, {
    method: "DELETE",
  });
}

export function fetchStatisticsOverview() {
  return request<StatisticsOverview>("/api/admin/statistics/overview");
}

export function fetchHotProducts() {
  return request<HotProduct[]>("/api/admin/statistics/hot-products");
}
