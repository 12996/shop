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

export type AdminProduct = {
  id: number;
  category: number;
  category_name: string;
  name: string;
  main_image: string | null;
  description: string | null;
  price: string;
  status: string;
  quantity: number;
  alert_threshold: number;
};

export type Category = {
  id: number;
  name: string;
  sort_order: number;
};

export type InventoryItem = {
  product_id: number;
  product_name: string;
  category_name: string;
  product_status: string;
  quantity: number;
  alert_threshold: number;
  is_alert: boolean;
  updated_at: string;
};

export type AdminProductPayload = {
  category: number;
  name: string;
  main_image: string;
  description: string;
  price: string;
  status: string;
  quantity: number;
  alert_threshold: number;
};

export function fetchCategories() {
  return request<Category[]>("/api/categories");
}

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

export function fetchProductDetail(productId: number) {
  return request<Product>(`/api/products/${productId}`);
}

export function fetchAdminProducts() {
  return request<AdminProduct[]>("/api/admin/products");
}

export function createAdminProduct(payload: AdminProductPayload) {
  return request<AdminProduct>("/api/admin/products", {
    method: "POST",
    body: payload,
  });
}

export function updateAdminProduct(productId: number, payload: AdminProductPayload) {
  return request<AdminProduct>(`/api/admin/products/${productId}`, {
    method: "PUT",
    body: payload,
  });
}

export function onShelfProduct(productId: number) {
  return request<AdminProduct>(`/api/admin/products/${productId}/on_shelf`, {
    method: "POST",
  });
}

export function offShelfProduct(productId: number) {
  return request<AdminProduct>(`/api/admin/products/${productId}/off_shelf`, {
    method: "POST",
  });
}

export function fetchInventory() {
  return request<InventoryItem[]>("/api/admin/inventory");
}

export function adjustInventory(productId: number, payload: { quantity: number; remark?: string }) {
  return request<InventoryItem>(`/api/admin/inventory/${productId}/adjust`, {
    method: "POST",
    body: payload,
  });
}
