<template>
  <v-app>
    <GraphEditor
      :loaded=loaded
    />
    <Graph
      class="graph"
      :completeLoad=completeLoad
    />
    <vue-progress-bar></vue-progress-bar>
  </v-app>
</template>

<style>
  /* Override vuetify */
  .v-btn:not(.v-btn--text):not(.v-btn--outlined):focus::before {
    opacity: 0;
  }
  .v-application--is-ltr .v-list-item__icon:first-child {
    margin-right: 12px !important;
  }
  .v-application--is-ltr .v-list-item__icon:last-of-type:not(:only-child) {
    margin-left: 0 !important;
  }
  .v-list-group .v-list-group__header .v-list-item__icon.v-list-group__header__append-icon {
    min-width: 24px !important;
  }
</style>

<style scoped>
  /* Own styles */
  .graph {
    height: 100vh;
  }
</style>

<script>
import Graph from "./Graph.vue";
import GraphEditor from "./GraphEditor.vue";
import graphData from "../state/graphData.js";

export default {
  name: 'App',
  components: {Graph, GraphEditor},
  props: [],
  methods: {
    completeLoad: function() {
      this.loaded = true;
    }
  },
  data() {
    let loaded = false;
    graphData.setup('rgba(0, 0, 0, 0.54)');

    return {
      loaded,
    }
  },
};
</script>
