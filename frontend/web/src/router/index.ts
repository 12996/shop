import { createRouter, createWebHistory } from "vue-router";

import AdminLayout from "../layouts/AdminLayout.vue";
import LoginView from "../views/LoginView.vue";
import AnnouncementView from "../views/admin/AnnouncementView.vue";
import CategoryManageView from "../views/admin/CategoryManageView.vue";
import DashboardView from "../views/admin/DashboardView.vue";
import InventoryView from "../views/admin/InventoryView.vue";
import OrderManageView from "../views/admin/OrderManageView.vue";
import ProductManageView from "../views/admin/ProductManageView.vue";
import RecommendationView from "../views/admin/RecommendationView.vue";
import StatisticsView from "../views/admin/StatisticsView.vue";
import UserCartView from "../views/user/UserCartView.vue";
import UserCheckoutView from "../views/user/UserCheckoutView.vue";
import UserHomeView from "../views/user/UserHomeView.vue";
import UserOrderView from "../views/user/UserOrderView.vue";
import UserProductView from "../views/user/UserProductView.vue";
import UserProfileView from "../views/user/UserProfileView.vue";
import { pinia } from "../stores/pinia";
import { useWebAuthStore } from "../stores/auth";

const routes = [
  {
    path: "/",
    redirect: "/user/home",
  },
  {
    path: "/login",
    name: "web-login",
    component: LoginView,
    meta: { guestOnly: true },
  },
  {
    path: "/",
    component: AdminLayout,
    children: [
      { path: "user/home", name: "web-user-home", component: UserHomeView, meta: { requiresAuth: true } },
      { path: "user/products", name: "web-user-products", component: UserProductView, meta: { requiresAuth: true } },
      { path: "user/cart", name: "web-user-cart", component: UserCartView, meta: { requiresAuth: true } },
      { path: "user/checkout", name: "web-user-checkout", component: UserCheckoutView, meta: { requiresAuth: true } },
      { path: "user/orders", name: "web-user-orders", component: UserOrderView, meta: { requiresAuth: true } },
      { path: "user/profile", name: "web-user-profile", component: UserProfileView, meta: { requiresAuth: true } },
      { path: "admin/dashboard", name: "web-admin-dashboard", component: DashboardView, meta: { requiresAuth: true, requiresMerchant: true } },
      { path: "admin/products", name: "web-admin-products", component: ProductManageView, meta: { requiresAuth: true, requiresMerchant: true } },
      { path: "admin/categories", name: "web-admin-categories", component: CategoryManageView, meta: { requiresAuth: true, requiresMerchant: true } },
      { path: "admin/inventory", name: "web-admin-inventory", component: InventoryView, meta: { requiresAuth: true, requiresMerchant: true } },
      { path: "admin/orders", name: "web-admin-orders", component: OrderManageView, meta: { requiresAuth: true, requiresMerchant: true } },
      { path: "admin/announcements", name: "web-admin-announcements", component: AnnouncementView, meta: { requiresAuth: true, requiresMerchant: true } },
      { path: "admin/recommendations", name: "web-admin-recommendations", component: RecommendationView, meta: { requiresAuth: true, requiresMerchant: true } },
      { path: "admin/statistics", name: "web-admin-statistics", component: StatisticsView, meta: { requiresAuth: true, requiresMerchant: true } },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to) => {
  const authStore = useWebAuthStore(pinia);
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
  const requiresMerchant = to.matched.some((record) => record.meta.requiresMerchant);
  const guestOnly = to.matched.some((record) => record.meta.guestOnly);

  if (requiresAuth && !authStore.isAuthenticated) {
    return {
      path: "/login",
      query: {
        redirect: to.fullPath,
      },
    };
  }

  if (guestOnly && authStore.isAuthenticated) {
    return authStore.isMerchant ? "/admin/dashboard" : "/user/home";
  }

  if (requiresMerchant && !authStore.isMerchant) {
    return "/user/home";
  }

  return true;
});

export default router;
