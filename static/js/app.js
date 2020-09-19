var local_url = "http://localhost:8000";

let navItemCart = Vue.component("nav-cart-item", {
  name: "nav-cart-item",
  template: "#navbar-cart-item",
  delimiters: ["{", "}"],
  data() {
    return {
      cart_items: [],
    };
  },
  mounted() {
    this.getCartItems();
    console.log("Mounted Cart Items");
    console.log(this.cart_items);
  },
  methods: {
    getCartItems() {
      axios({
        method: "GET",
        url: `${local_url}/api/cart-list`,
      })
        .then((res) => {
          this.cart_items = res.data;
        })
        .catch((err) => console.log(err));
    },
  },
});

let LightroomComp = Vue.component("lightroom", {
  template: "#lightroom",
  delimiters: ["{", "}"],
  data() {
    return {
      items: [],
      test: "Lightroom Component",
    };
  },
  mounted() {
    this.getLightroom();
    console.log("Mounted");
    console.log(this.items);
  },
  methods: {
    addCart(item) {
      this.$emit("new-lightroom-preset", item);
      console.log(item);
      console.log("emit new lightroom item cart!");
    },
    getLightroom() {
      axios({
        method: "GET",
        url: `${local_url}/api/lightroom-list`,
      })
        .then((res) => {
          this.items = res.data;
        })
        .catch((err) => console.log(err));
    },
  },
});

let PhotoshopComp = Vue.component("photoshop", {
  name: "Photoshop",
  template: "#photoshop-root",
  delimiters: ["{", "}"],
  data() {
    return {
      items: [],
      cart_items: [],
    };
  },
  props: {},
  mounted() {
    this.getPhotoshop();
    // this.getCartItems();
    console.log("Mounted");
    console.log(this.items);
  },
  methods: {
    getPhotoshop() {
      axios({
        method: "GET",
        url: `${local_url}/api/photoshop-list`,
      })
        .then((res) => {
          this.items = res.data;
        })
        .catch((err) => console.log(err));
    },
    addCart(item) {
      this.$emit("new-photoshop-item", item);
      console.log(item);
      console.log("emit new photoshop item to cart!");
    },
    deleteCart(item) {
      axios({
        method: "GET",
        url: `${local_url}/api/cart-list/${item.slug}`,
      })
        .then(() => {
          this.getCartItems();
          console.log("Cart!!");
        })
        .catch((err) => console.log(err));
    },
  },
});

let CartComponent = Vue.component("cart-component", {
  name: "cart-component",
  delimiters: ["{", "}"],
  template: "#cart-root",
  data() {
    return {
      cart_items: [],
      is_loading: false,
      message: "",
      coupon: null,
    };
  },
  mounted() {
    this.getCartItems();
  },
  methods: {
    getCartItems() {
      axios({
        method: "GET",
        url: `${local_url}/api/cart-list`,
      })
        .then((res) => {
          this.cart_items = res.data;
        })
        .catch((err) => console.log(err));
    },
    addCoupon() {
      axios({
        method: "POST",
        url: `${local_url}/api/get-coupon/${this.coupon}`,
        data: {
          coupon: this.coupon
        },
        headers: {
          "X-CSRFToken": "{{ csrf_token }}",
          "content-type": "application/json",
        },
      })
        .then((res) => {
          this.message = res.data.coupon;
          console.log(res.data);
        })
        .catch((err) => console.log(err));
    },
  },
});

new Vue({
  el: "#app",
  name: "root",
  delimiters: ["{", "}"],
  components: {
    lightroom: LightroomComp,
    "nav-cart-item": navItemCart,
    photoshop: PhotoshopComp,
    cart: CartComponent,
  },
  data: {
    message: "TESTSETSETSET",
    items: [],
    cart_items: [],
  },
  mounted() {
    this.getCartItems();
  },
  methods: {
    newItemFromPhotoshop(item) {
      console.log("neItemFromPhotoshop executing...");
      console.log(item);
      axios({
        method: "GET",
        url: `${local_url}/api/add-to-cart/${item.slug}`,
      })
        .then(() => {
          this.getCartItems();
          console.log("Cart!! from child!!");
        })
        .catch((err) => console.log(err));
    },
    addCart(item) {
      axios({
        method: "GET",
        url: `${local_url}/api/add-to-cart/${item.slug}`,
      })
        .then(() => {
          this.getCartItems();
          console.log("Cart!!");
        })
        .catch((err) => console.log(err));
    },
    deleteCart(item) {
      axios({
        method: "GET",
        url: `${local_url}/api/remove-from-cart/${item.slug}`,
      })
        .then(() => {
          console.log(item.title + " was remove from cart!");
          this.getCartItems();
        })
        .catch((err) => console.log(err));
    },
    getCartItems() {
      axios({
        method: "GET",
        url: `${local_url}/api/cart-list`,
      })
        .then((res) => {
          this.cart_items = res.data;
        })
        .catch((err) => console.log(err));
    },
  },
});
