<template>
  <div class="main-app">
    <v-app>
      <v-btn fixed left top fab small
        color="#64B5F6"
        v-if="loaded"
        @click="sidebar = true"
      >
        <v-icon>mdi-menu</v-icon>
      </v-btn>
      <v-navigation-drawer app temporary v-model="sidebar">

        <v-toolbar flat>
          <v-tooltip bottom attach=".main-app">
            <template v-slot:activator="{ on }">
              <v-btn v-on="on" @click="collapseAll">
                <v-icon>mdi-arrow-collapse-all</v-icon>
              </v-btn>
            </template>
            <span>Collapse all</span>
          </v-tooltip>
          <v-spacer></v-spacer>
          <v-tooltip bottom attach=".main-app">
            <template v-slot:activator="{ on }">
              <v-btn v-on="on" @click="expandAll">
                <v-icon>mdi-arrow-expand-all</v-icon>
              </v-btn>
            </template>
            <span>Expand all</span>
          </v-tooltip>
        </v-toolbar>

        <v-list expand dense>
          <v-list-group
            v-for="app in Object.keys(activeModels)"
            :key="app"
            v-model:value="activeModels[app].expanded"
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
    </v-app>
  </div>
</template>

<style>
  /* Override vuetify */
  .v-btn:not(.v-btn--text):not(.v-btn--outlined):focus::before {
    opacity: 0;
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
import Network from "./Network.vue";

const getColor = (index, numColors) => `hsl(${index * (360 / numColors)},50%,85%)`;
const getBorderColor = (index, numColors) => `hsl(${index * (360 / numColors)},70%,40%)`;
const joinModelStrings = (appModelPair) => `${appModelPair[0]}/${appModelPair[1]}`;
const fixModelStrings = (edges) => edges.map((pair) => {
  return [joinModelStrings(pair[0]), joinModelStrings(pair[1])]
});


const edge_app = {arrows: 'middle'};
const edge_fk = {arrows: 'to'};
const edge_m2m = {arrows: 'from;to'};
const edge_1to1 = {arrows: {middle: {enabled: true, scaleFactor: 0.9, type: 'bar'}}};
const edge_subclass = {dashes: true, arrows: 'to', label: 'Subclass'};
const edge_proxy = {dashes: true, arrows: 'to', label: 'Proxy'};


const options = {
  edges: {
    smooth: {},
    arrows:{
      to: {scaleFactor: 0.8},
      from: {scaleFactor: 0.8},
    }
  }
};

const appNode = (app, softColor, hardColor) => {
  return {
    app,
    id: app,
    label: app,
    color: {
      background: softColor,
      border: hardColor,
    },
    shape: "box",
  }
};
const modelNode = (app, model, softColor, hardColor) => {
  return {
    app,
    id: joinModelStrings([app, model]),
    label: model,
    color: {
      background: softColor,
      border: hardColor,
    },
  }
};
const abstractModelNode = (app, model, softColor, hardColor) => {
  var node = modelNode(app, model, softColor, hardColor);
  node.shapeProperties = {borderDashes: true}
  return node
};


export default {
  name: 'App',
  components: {Network},
  props: ['abstractModels', 'models', 'connections'],
  methods: {
    expandAll: function(ev) {
      Object.keys(this.activeModels).forEach((app) => {
        this.activeModels[app].expanded = true;
      });
    },
    collapseAll: function(ev) {
      Object.keys(this.activeModels).forEach((app) => {
        this.activeModels[app].expanded = false;
      });
    },
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

    const allApps = [...new Set([
      ...Object.keys(models),
      ...Object.keys(abstractModels)
    ])].sort();
    let activeModels = {};
    allApps.forEach((app, i) => {
      activeModels[app] = {
        expanded: true,
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


    var interAppRelations = [];
    Object.keys(connections).forEach((connectionType) => {
      for (const pair of connections[connectionType]) {
        const [from, to] = [pair[0], pair[1]];
        // Only external relations matter, not relations to self.
        if (from[0] != to[0]) {
          // Model -> App
          interAppRelations.push([joinModelStrings(from), to[0]]);
          // App -> Model
          interAppRelations.push([from[0], joinModelStrings(to)]);
          // App -> App
          interAppRelations.push([from[0], to[0]]);
        }
      }
    });
    // Unique sort.
    interAppRelations = interAppRelations.filter(
      function (relation, index, input) {
        return index === input.findIndex(function (n) {
          return n[0] == relation[0] && n[1] == relation[1]
        });
      }
    ).sort();

    const edges = [
      ...fixModelStrings(connections.foreignkey).map(([from, to]) => ({...edge_fk, from, to})),
      ...fixModelStrings(connections.many2many).map(([from, to]) => ({...edge_m2m, from, to})),
      ...fixModelStrings(connections.one2one).map(([from, to]) => ({...edge_1to1, from, to})),
      ...fixModelStrings(connections.subclass).map(([from, to]) => ({...edge_subclass, from, to})),
      ...fixModelStrings(connections.proxy).map(([from, to]) => ({...edge_proxy, from, to})),
      ...interAppRelations.map(([from, to]) => ({...edge_app, from, to})),
    ];

    return {
      activeModels,
      allApps,
      loaded,
      edges,
      options,
      sidebar: false,
    };
  },
  computed: {
    nodes: function () {
      const modelsAndFunctions = [
        [models, modelNode],
        [abstractModels, abstractModelNode]
      ];
      var nodes = [];
      this.allApps.forEach((app, appIndex) => {
        var appData = this.activeModels[app];
        if (appData.expanded) {
          modelsAndFunctions.forEach(([modelSet, node]) => {
            if (modelSet.hasOwnProperty(app)) {
              modelSet[app].forEach((model) => {
                if (this.activeModels[app].models[model].active) {
                  nodes.push(node(app, model, appData.softColor, appData.hardColor));
                }
              });
            }
          });
        } else {
          nodes.push(appNode(app, appData.softColor, appData.hardColor));
        }
      });
      return nodes;
    },
  },
};
</script>
