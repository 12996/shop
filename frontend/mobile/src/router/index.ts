import { createRouter, createWebHistory } from "vue-router";

import CartView from "../views/CartView.vue";
import CheckoutView from "../views/CheckoutView.vue";
import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
import OrderListView from "../views/OrderListView.vue";
import ProfileView from "../views/ProfileView.vue";
import ProductListView from "../views/ProductListView.vue";

const routes = [
  {
    path: "/login",
    name: "mobile-login",
    component: LoginView,
    meta: {
      title: "用户登录",
      showTopNav: false,
    },
  },
  {
    path: "/",
    name: "mobile-home",
    component: HomeView,
    meta: { title: "首页" },
  },
  {
    path: "/products",
    name: "mobile-products",
    component: ProductListView,
    meta: { title: "商品列表" },
  },
  {
    path: "/cart",
    name: "mobile-cart",
    component: CartView,
    meta: { title: "购物车" },
  },
  {
    path: "/checkout",
    name: "mobile-checkout",
    component: CheckoutView,
    meta: { title: "确认订单" },
  },
  {
    path: "/orders",
    name: "mobile-orders",
    component: OrderListView,
    meta: { title: "我的订单" },
  },
  {
    path: "/profile",
    name: "mobile-profile",
    component: ProfileView,
    meta: { title: "用户中心" },
  },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
