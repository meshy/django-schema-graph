import Vue from "vue";
import App from "../components/App.vue";
import vuetify from '../plugins/vuetify'
import VueProgressBar from "vue-progressbar";


Vue.use(VueProgressBar, {
  transition: {speed: '0s', opacity: '0.6s', termination: 300}
})
new Vue({
  vuetify,
  render: function (h) {
    return h(App);
  }
}).$mount(`#schema-graph-app`);
