<template>
  <div class="main-app">
    <network
      class="graph"
      :nodes=nodes
      :edges=edges
      :options=options
      @stabilization-progress="stabilizationProgress"
      @stabilization-iterations-done="stabilizationIterationsDone"
    />
    <vue-progress-bar></vue-progress-bar>
  </div>
</template>

<style scoped>
  .main-app {
    display: flex;
    height: 100vh;
  }
  .main-app > .graph {
    flex-grow: 1;
  }
</style>

<script>
const getColor = (index, numColors) => `hsl(${index * (360 / numColors)},50%,85%)`;
const getBorderColor = (index, numColors) => `hsl(${index * (360 / numColors)},70%,40%)`;
const joinModelStrings = (appModelPair) => `${appModelPair[0]}/${appModelPair[1]}`;
const fixModelStrings = (edges) => edges.map((pair) => {
  return [joinModelStrings(pair[0]), joinModelStrings(pair[1])]
});


const edge_fk = {arrows: 'to'};
const edge_m2m = {arrows: 'from;to'};
const edge_1to1 = {arrows: {middle: {enabled: true}}};


const options = {
  edges: {
    smooth: {},
    arrows:{
      to: {scaleFactor: 0.8},
      middle: {scaleFactor: 0.9, type: 'bar'},
      from: {scaleFactor: 0.8},
    }
  }
};


export default {
  name: 'App',
  props: ['models', 'connections'],
  methods: {
    stabilizationProgress: function (ev) {
      const progress = (ev.iterations / ev.total) * 100;
      console.log(`Stabilization progress ${progress}%`);
      this.$Progress.set(progress);
    },
    stabilizationIterationsDone: function () {
      console.log('Stabilization complete');
      this.$Progress.finish();
    }
  },
  data() {
    const models = this.models;
    const connections = this.connections;
    const groupedNodes = new Map(
      Object
      .keys(models)
      .map((app, appIndex) => (
        [
          app,
          models[app].map(model => (
            {
              app,
              id: joinModelStrings([app, model]),
              label: model,
              color: {
                background: getColor(appIndex, Object.keys(models).length),
                border: getBorderColor(appIndex, Object.keys(models).length),
              },
            }
          ))
        ]
      ))
    );

    const nodes = [].concat.apply([], Array.from(groupedNodes.keys()).map(app => groupedNodes.get(app)));

    const edges = [
      ...fixModelStrings(connections.foreignkey).map(([from, to]) => ({...edge_fk, from, to})),
      ...fixModelStrings(connections.many2many).map(([from, to]) => ({...edge_m2m, from, to})),
      ...fixModelStrings(connections.one2one).map(([from, to]) => ({...edge_1to1, from, to})),
    ];

    return {
      nodes,
      edges,
      options,
    };
  }
};
</script>
