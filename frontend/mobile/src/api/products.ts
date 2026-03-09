import { request } from "./http";

export type Product = {
  id: number;
  category_id: number;
  category_name: string;
  name: string;
  main_image: string | null;
  description: string | null;
  price: string;
  status: string;
  stock_quantity: number;
};

export function fetchProducts(params: { categoryId?: number | null; keyword?: string } = {}) {
  const query = new URLSearchParams();

  if (params.categoryId) {
    query.set("category_id", String(params.categoryId));
  }
  if (params.keyword) {
    query.set("keyword", params.keyword);
  }

  const suffix = query.toString() ? `?${query}` : "";
  return request<Product[]>(`/api/products${suffix}`);
}
