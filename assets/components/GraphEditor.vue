<template>
  <div>
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
              <v-btn small v-on="on" @click="hideAll">
                <v-icon>mdi-eye-off</v-icon>
              </v-btn>
            </template>
            <span>Hide all</span>
          </v-tooltip>
          <v-spacer></v-spacer>
          <v-tooltip bottom attach=".main-app">
            <template v-slot:activator="{ on }">
              <v-btn small v-on="on" @click="showAll">
                <v-icon>mdi-eye</v-icon>
              </v-btn>
            </template>
            <span>Show all</span>
          </v-tooltip>
          <v-spacer></v-spacer>
          <v-tooltip bottom attach=".main-app">
            <template v-slot:activator="{ on }">
              <v-btn small v-on="on" @click="collapseAll">
                <v-icon>mdi-arrow-collapse-all</v-icon>
              </v-btn>
            </template>
            <span>Collapse all</span>
          </v-tooltip>
          <v-spacer></v-spacer>
          <v-tooltip bottom attach=".main-app">
            <template v-slot:activator="{ on }">
              <v-btn small v-on="on" @click="expandAll">
                <v-icon>mdi-arrow-expand-all</v-icon>
              </v-btn>
            </template>
            <span>Expand all</span>
          </v-tooltip>
        </v-toolbar>

        <v-list expand dense>
          <v-list-group
            v-for="app in Object.keys(graphData.activeModels)"
            :key="app"
            :value="graphData.activeModels[app].expanded"
            :color="graphData.activeModels[app].visible ? graphData.activeModels[app].hardColor : inactiveColor"
          >

            <template v-slot:activator>
              <v-list-item-icon
                @click.stop="graphData.setAppVisible(app, !graphData.activeModels[app].visible)"
              >
                <v-icon
                  v-if="graphData.activeModels[app].visible"
                  v-bind:style="{color: graphData.activeModels[app].visible ? graphData.activeModels[app].hardColor : inactiveColor}"
                >mdi-eye-outline</v-icon>
                <v-icon v-else
                  v-bind:style="{color: graphData.activeModels[app].visible ? graphData.activeModels[app].hardColor : inactiveColor}"
                >mdi-eye-off-outline</v-icon>
              </v-list-item-icon>
              <v-list-item-content
                @click.stop="graphData.setAppExpanded(app, !graphData.activeModels[app].expanded)"
              >
                <v-list-item-title
                  v-text="app"
                  v-bind:style="{color: graphData.activeModels[app].visible ? graphData.activeModels[app].hardColor : inactiveColor}"
                ></v-list-item-title>
              </v-list-item-content>
            </template>
            <v-list-item dense link
              class="menu-model"
              v-for="model, modelIndex in graphData.activeModels[app].models"
              :key="model.id"
              :disabled="!graphData.activeModels[app].visible"
              @click.stop="graphData.setModelActive(app, model.label, !model.active)"
            >
              <v-list-item-content>
                <v-list-item-title v-text="model.label"></v-list-item-title>
              </v-list-item-content>
              <v-list-item-action>
                <v-icon v-if="!graphData.activeModels[app].visible && model.active">
                  mdi-eye-outline
                </v-icon>
                <v-icon v-else-if="graphData.activeModels[app].visible && model.active" :color="graphData.activeModels[app].hardColor" >
                  mdi-eye-outline
                </v-icon>
                <v-icon v-else>
                  mdi-eye-off-outline
                </v-icon>
              </v-list-item-action>
            </v-list-item>

          </v-list-group>
        </v-list>

      </v-navigation-drawer>
  </div>
</template>

<style scoped>
  /* Own styles */
  .menu-model {
    padding-left: 52px;
  }
</style>

<script>
import graphData from "../state/graphData.js";
export default {
  name: "GraphEditor",
  components: {},
  props: ["loaded", "inactiveColor"],
  data() {
    return {
      sidebar: false,
      graphData
    }
  },
  methods: {
    hideAll: function () {
      graphData.hideAll();
    },
    showAll: function () {
      graphData.showAll();
    },
    collapseAll: function () {
      graphData.collapseAll();
    },
    expandAll: function () {
      graphData.expandAll();
    },
  },
};
</script>
