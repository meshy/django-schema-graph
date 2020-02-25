<template>
  <div class="main-app">
    <v-btn fixed left top fab small
      color="#64B5F6"
      v-if="loaded"
      @click="sidebar = true"
    >
      <v-icon>mdi-menu</v-icon>
    </v-btn>
    <v-navigation-drawer app temporary v-model="sidebar">

      <v-list expand>
        <v-list-group
          v-for="app in Object.keys(activeModels)"
          :key="app"
          v-model:value="activeModels[app].active"
          :color="activeModels[app].hardColor"
        >

          <template v-slot:activator>
            <v-list-item-content>
              <v-list-item-title
                v-text="app"
                v-bind:style="{color: activeModels[app].hardColor}"
              ></v-list-item-title>
            </v-list-item-content>
          </template>
          <v-list-item dense link
            v-for="model, modelIndex in activeModels[app].models"
            :key="model.id"
            @click="model.active = !model.active"
          >
            <v-list-item-content>
              <v-list-item-title v-text="model.label"></v-list-item-title>
            </v-list-item-content>
            <v-list-item-action>
              <v-checkbox
                :color="activeModels[app].hardColor"
                :input-value="model.active"
              ></v-checkbox>
            </v-list-item-action>
          </v-list-item>

        </v-list-group>
      </v-list>

    </v-navigation-drawer>
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
  .v-btn:not(.v-btn--text):not(.v-btn--outlined):focus::before {
    opacity: 0; /* Override vuetify */
  }
  .main-app {
    display: flex;
    height: 100vh;
  }
  .main-app > .graph {
    flex-grow: 1;
  }
</style>

<script>
import Network from "./Network.vue";

const getColor = (index, numColors) => `hsl(${index * (360 / numColors)},50%,85%)`;
const getBorderColor = (index, numColors) => `hsl(${index * (360 / numColors)},70%,40%)`;
const joinModelStrings = (appModelPair) => `${appModelPair[0]}/${appModelPair[1]}`;
const fixModelStrings = (edges) => edges.map((pair) => {
  return [joinModelStrings(pair[0]), joinModelStrings(pair[1])]
});


const edge_fk = {arrows: 'to'};
const edge_m2m = {arrows: 'from;to'};
const edge_1to1 = {arrows: {middle: {enabled: true}}};
const edge_subclass = {dashes: true, arrows: 'to', label: 'Subclass'};
const edge_proxy = {dashes: true, arrows: 'to', label: 'Proxy'};


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
  components: {Network},
  props: ['abstractModels', 'models', 'connections'],
  methods: {
    stabilizationProgress: function (ev) {
      const progress = (ev.iterations / ev.total) * 100;
      console.log(`Stabilization progress ${progress}%`);
      this.$Progress.set(progress);
    },
    stabilizationIterationsDone: function () {
      console.log('Stabilization complete');
      this.$Progress.finish();
      this.loaded = true;
    }
  },
  data() {
    const models = this.models;
    const connections = this.connections;
    let loaded = false;

    const allApps = Object.keys(models).concat(Object.keys(abstractModels)).sort();
    let activeModels = {};
    allApps.forEach((app, i) => {
      activeModels[app] = {
        active: true,
        models: {},
        hardColor: getBorderColor(i, allApps.length),
        softColor: getColor(i, allApps.length),
      };
    });
    Object.keys(models).forEach((app) => {
      for (const model of models[app]) {
        activeModels[app].models[model] = {
          active: true,
          id: joinModelStrings([app, model]),
          label: model,
        };
      };
    });
    Object.keys(abstractModels).forEach((app) => {
      for (const model of abstractModels[app]) {
        activeModels[app].models[model] = {
          active: true,
          id: joinModelStrings([app, model]),
          label: model,
        };
      };
    });

    const edges = [
      ...fixModelStrings(connections.foreignkey).map(([from, to]) => ({...edge_fk, from, to})),
      ...fixModelStrings(connections.many2many).map(([from, to]) => ({...edge_m2m, from, to})),
      ...fixModelStrings(connections.one2one).map(([from, to]) => ({...edge_1to1, from, to})),
      ...fixModelStrings(connections.subclass).map(([from, to]) => ({...edge_subclass, from, to})),
      ...fixModelStrings(connections.proxy).map(([from, to]) => ({...edge_proxy, from, to})),
    ];

    return {
      activeModels,
      loaded,
      edges,
      options,
      sidebar: false,
    };
  },
  computed: {
    nodes: function () {
      var nodes = [];
      Object.keys(models).forEach((app, appIndex) => {
        if (this.activeModels[app].active) {
          models[app].forEach((model) => {
            if (this.activeModels[app].models[model].active) {
              nodes.push({
                app,
                id: joinModelStrings([app, model]),
                label: model,
                color: {
                  background: this.activeModels[app].softColor,
                  border: this.activeModels[app].hardColor,
                },
              });
            }
          });
        }
      });
      Object.keys(abstractModels).forEach((app, appIndex) => {
        if (this.activeModels[app].active) {
          abstractModels[app].forEach((model) => {
            if (this.activeModels[app].models[model].active) {
              nodes.push({
                app,
                id: joinModelStrings([app, model]),
                label: model,
                color: {
                  background: this.activeModels[app].softColor,
                  border: this.activeModels[app].hardColor,
                },
                shapeProperties: {borderDashes: true},
              });
            }
          });
        }
      });
      return nodes;
    },
  },
};
</script>
