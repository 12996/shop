import { request } from "./http";

export type OrderItem = {
  id: number;
  product_id: number;
  product_name: string;
  product_image: string | null;
  product_price: string;
  quantity: number;
  subtotal: string;
};

export type Order = {
  id: number;
  order_number: string;
  status: string;
  total_amount: string;
  pay_amount: string;
  payment_method: string | null;
  address_id: number | null;
  address_snapshot: Record<string, unknown> | null;
  created_at: string;
  items: OrderItem[];
};

export function createOrder() {
  return request<Order>("/api/orders", {
    method: "POST",
  });
}

export function payOrder(orderId: number, paymentMethod: string) {
  return request<Order>(`/api/orders/${orderId}/pay`, {
    method: "POST",
    body: { payment_method: paymentMethod },
  });
}

export function cancelOrder(orderId: number) {
  return request<Order>(`/api/orders/${orderId}/cancel`, {
    method: "POST",
  });
}

export function fetchOrders() {
  return request<Order[]>("/api/orders");
}
