import { request } from "./http";

export type Announcement = {
  id: number;
  title: string;
  content: string;
  status: string;
  published_at: string | null;
};

export type Recommendation = {
  id: number;
  sort_order: number;
  status: string;
  product: number;
  product_name: string;
  product_price: string;
  product_image: string | null;
};

export type Category = {
  id: number;
  name: string;
  sort_order: number;
};

export function fetchHomeData() {
  return request<{ announcement: Announcement | null; recommendations: Recommendation[] }>("/api/home");
}

export function fetchCategories() {
  return request<Category[]>("/api/categories");
}
