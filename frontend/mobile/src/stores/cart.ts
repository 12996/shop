import { computed, ref } from "vue";
import { defineStore } from "pinia";

import {
  addCartItem,
  deleteCartItem,
  fetchCart,
  fetchCheckoutPreview,
  updateCartItem,
  type Cart,
  type CheckoutPreview,
} from "../api/cart";

export const useCartStore = defineStore("mobile-cart", () => {
  const cart = ref<Cart | null>(null);
  const checkoutPreview = ref<CheckoutPreview | null>(null);
  const loading = ref(false);

  const itemCount = computed(() => (cart.value?.items ?? []).reduce((sum, item) => sum + item.quantity, 0));
  const selectedTotal = computed(() =>
    (cart.value?.items ?? []).reduce((sum, item) => {
      if (!item.selected) {
        return sum;
      }
      return sum + Number(item.product_price) * item.quantity;
    }, 0),
  );

  async function loadCart() {
    loading.value = true;
    try {
      cart.value = await fetchCart();
      return cart.value;
    } finally {
      loading.value = false;
    }
  }

  async function addItem(productId: number, quantity = 1) {
    await addCartItem({ product_id: productId, quantity });
    return loadCart();
  }

  async function changeItem(itemId: number, payload: { quantity: number; selected?: boolean }) {
    await updateCartItem(itemId, payload);
    return loadCart();
  }

  async function removeItem(itemId: number) {
    await deleteCartItem(itemId);
    return loadCart();
  }

  async function loadCheckoutPreview() {
    loading.value = true;
    try {
      checkoutPreview.value = await fetchCheckoutPreview();
      return checkoutPreview.value;
    } finally {
      loading.value = false;
    }
  }

  function clearCheckoutPreview() {
    checkoutPreview.value = null;
  }

  return {
    cart,
    checkoutPreview,
    loading,
    itemCount,
    selectedTotal,
    loadCart,
    addItem,
    changeItem,
    removeItem,
    loadCheckoutPreview,
    clearCheckoutPreview,
  };
});
