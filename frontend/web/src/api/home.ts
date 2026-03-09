import { request } from "./http";

export type HomeAnnouncement = {
  id: number;
  title: string;
  content: string;
  status: "draft" | "published";
  published_at: string | null;
};

export type HomeRecommendation = {
  id: number;
  product: number;
  product_name: string;
  product_image: string | null;
  product_price: string;
  sort_order: number;
};

export type HomePayload = {
  announcement: HomeAnnouncement | null;
  recommendations: HomeRecommendation[];
};

export function fetchHomeData() {
  return request<HomePayload>("/api/home");
}
