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

export type AdminOrder = Order & {
  user: number;
  username: string;
};

export function createOrder() {
  return request<Order>("/api/orders", {
    method: "POST",
  });
}

export function fetchOrders() {
  return request<Order[]>("/api/orders");
}

export function fetchOrderDetail(orderId: number) {
  return request<Order>(`/api/orders/${orderId}`);
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

export function fetchAdminOrders(status?: string) {
  const query = status && status !== "all" ? `?status=${status}` : "";
  return request<AdminOrder[]>(`/api/admin/orders${query}`);
}

export function fetchAdminOrderDetail(orderId: number) {
  return request<AdminOrder>(`/api/admin/orders/${orderId}`);
}

export function completeAdminOrder(orderId: number) {
  return request<AdminOrder>(`/api/admin/orders/${orderId}/complete`, {
    method: "POST",
  });
}
