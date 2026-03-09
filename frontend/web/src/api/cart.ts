import { request } from "./http";

export type CartItem = {
  id: number;
  product: number;
  product_name: string;
  product_price: string;
  quantity: number;
  selected: boolean;
};

export type Cart = {
  id: number;
  user: number;
  items: CartItem[];
  created_at: string;
  updated_at: string;
};

export type CheckoutPreview = {
  cart_id: number;
  items: CartItem[];
  total_amount: string;
};

export function fetchCart() {
  return request<Cart>("/api/cart/");
}

export function addCartItem(payload: { product_id: number; quantity: number }) {
  return request<CartItem>("/api/cart/items", {
    method: "POST",
    body: payload,
  });
}

export function updateCartItem(itemId: number, payload: { quantity: number; selected?: boolean }) {
  return request<CartItem>(`/api/cart/items/${itemId}`, {
    method: "PUT",
    body: payload,
  });
}

export function deleteCartItem(itemId: number) {
  return request<null>(`/api/cart/items/${itemId}`, {
    method: "DELETE",
  });
}

export function fetchCheckoutPreview() {
  return request<CheckoutPreview>("/api/cart/checkout", {
    method: "POST",
  });
}
