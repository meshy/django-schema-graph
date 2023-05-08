<template>
  <network
    :nodes=nodes
    :edges=edges
    :options=options
    @stabilization-progress="stabilizationProgress"
    @stabilization-iterations-done="stabilizationIterationsDone"
  />
</template>

<script>
import { Network } from "vue-vis-network";

export default {
  name: "Graph",
  components: { Network },
  props: ["nodes", "edges", "options", "completeLoad"],
  data() {
    const options = {
      edges: {
        smooth: {},
        arrows:{
          to: {scaleFactor: 0.8},
          from: {scaleFactor: 0.8},
        }
      }
    };
    return {
      options
    };
  },
  methods: {
    stabilizationProgress: function (ev) {
      const progress = (ev.iterations / ev.total) * 100;
      console.log(`Stabilization progress ${progress}%`);
      this.$Progress.set(progress);
    },
    stabilizationIterationsDone: function () {
      console.log('Stabilization complete');
      this.$Progress.finish();
      this.completeLoad();
    }
  },
};
</script>
