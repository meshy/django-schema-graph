import Vue from "vue";
import App from "../components/App.vue";
import { Network } from "vue2vis";
import VueProgressBar from "vue-progressbar";


Vue.use(VueProgressBar, {
  transition: {speed: '0s', opacity: '0.6s', termination: 300}
})
Vue.component('network', Network);
new Vue({
  render: function (h) {
    return h(App, {props: {models: window.models, connections: window.connections}});
  }
}).$mount(`#schema-graph-app`);
