import { createRouter, createWebHistory } from "vue-router";

import CartView from "../views/CartView.vue";
import CheckoutView from "../views/CheckoutView.vue";
import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
import OrderListView from "../views/OrderListView.vue";
import ProductListView from "../views/ProductListView.vue";

const routes = [
  {
    path: "/login",
    name: "mobile-login",
    component: LoginView,
  },
  {
    path: "/",
    name: "mobile-home",
    component: HomeView,
  },
  {
    path: "/products",
    name: "mobile-products",
    component: ProductListView,
  },
  {
    path: "/cart",
    name: "mobile-cart",
    component: CartView,
  },
  {
    path: "/checkout",
    name: "mobile-checkout",
    component: CheckoutView,
  },
  {
    path: "/orders",
    name: "mobile-orders",
    component: OrderListView,
  },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
