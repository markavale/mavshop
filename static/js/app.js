var local_url = "http://localhost:8000";
var csrftoken = Cookies.get("csrftoken");

let navItemCart = Vue.component("nav-cart-item", {
  name: "nav-cart-item",
  template: "#navbar-cart-item",
  delimiters: ["{", "}"],
  data() {
    return {
      cart_items: [],
      token:null,
    };
  },
  mounted() {
    this.getCartItems();
    console.log("Mounted Cart Items");
    console.log(this.cart_items);
  },
  methods: {
    getCartItems() {
      this.token = localStorage.getItem('user-token');
      axios({
        method: "GET",
        url: `${local_url}/api/cart-list`,
        headers:{
          "Authorization": `Token ${this.token}`,
        },
      })
        .then((res) => {
          this.cart_items = res.data;
          console.log(this.token)
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
      extra_items: [],
      is_loading: false,
      message: "",
      coupon: null,
      token:null,
    };
  },
  mounted() {
    this.getCartItems();
    this.getExtraItems();
  },
  methods: {
    
    getCartItems() {
      this.token= localStorage.getItem('user-token');
      axios({
        method: "GET",
        url: `${local_url}/api/cart-list`,
        Authorization: `Token ${this.token}`
      })
        .then((res) => {
          this.cart_items = res.data;
          console.log(this.token);
        })
        .catch((err) => console.log(err));
    },
    getExtraItems() {
      axios({
        method: "GET",
        url: `${local_url}/api/extra-items`,
      })
        .then((res) => {
          this.extra_items = res.data;
          console.log("Success for get extra items");
        })
        .catch((err) => console.log(err));
    },
    addCoupon() {
      axios({
        method: "POST",
        url: `${local_url}/api/add-coupon/${this.coupon}`,
        data: {
          coupon: this.coupon,
        },
        headers: {
          "X-CSRFToken": csrftoken,
          //"content-type": "application/json",
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

var LoginRegister = Vue.component("login-register", {
  name: "Login-Register",
  template: "#login-register",
  delimiters: ["{", "}"],
  data() {
    return {
      user:{
        username:"",
        email:"",
        password:"",
        errors:[],
      },
    };
  },
  mounted() {},
  methods: {
    login() {
      axios({
        method: "POST",
        url: `${local_url}/auth/login/`,
        data: {
          username: this.user.username,
          email: this.user.email,
          password: this.user.password,
        },
        headers: {
          "X-CSRFToken": csrftoken,
          "Content-Type": "application/json",
        },
      }).then((res) => {
        const token = res.data.key;
        localStorage.setItem("user-token", token); // store the token in localstorage
        this.user.username = "";
        this.user.email = "";
        this.user.password = "";
        //this.$router.push('/');
        window.location.href = "/";
      })
      .catch(err =>{
        localStorage.removeItem('user-token');
        console.log(err);
        this.user.errors = err.data;
      });
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
    login:LoginRegister,
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
