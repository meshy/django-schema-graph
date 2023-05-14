<template>
  <div>
      <v-btn fixed left top fab small
        color="#64B5F6"
        v-if="loaded"
        @click="sidebar = true"
      >
        <v-icon>mdi-menu</v-icon>
      </v-btn>
      <v-navigation-drawer app temporary v-model="sidebar" width=384>

        <v-toolbar flat>
          <v-tooltip bottom>
            <template v-slot:activator="{ on }">
              <v-btn small v-on="on" @click="hideAll">
                <v-icon>mdi-eye-off</v-icon>
              </v-btn>
            </template>
            <span>Hide all</span>
          </v-tooltip>
          <v-spacer></v-spacer>
          <v-tooltip bottom>
            <template v-slot:activator="{ on }">
              <v-btn small v-on="on" @click="showAll">
                <v-icon>mdi-eye</v-icon>
              </v-btn>
            </template>
            <span>Show all</span>
          </v-tooltip>
          <v-spacer></v-spacer>
          <v-tooltip bottom>
            <template v-slot:activator="{ on }">
              <v-btn small v-on="on" @click="collapseAll">
                <v-icon>mdi-arrow-collapse-all</v-icon>
              </v-btn>
            </template>
            <span>Collapse all</span>
          </v-tooltip>
          <v-spacer></v-spacer>
          <v-tooltip bottom>
            <template v-slot:activator="{ on }">
              <v-btn small v-on="on" @click="expandAll">
                <v-icon>mdi-arrow-expand-all</v-icon>
              </v-btn>
            </template>
            <span>Expand all</span>
          </v-tooltip>
          <v-spacer></v-spacer>
          <v-tooltip bottom>
            <template v-slot:activator="{ on }">
              <v-btn small v-on="on" @click="foldAll">
                <v-icon>mdi-chevron-up</v-icon>
              </v-btn>
            </template>
            <span>Fold all</span>
          </v-tooltip>
          <v-spacer></v-spacer>
          <v-tooltip bottom>
            <template v-slot:activator="{ on }">
              <v-btn small v-on="on" @click="unfoldAll">
                <v-icon>mdi-chevron-down</v-icon>
              </v-btn>
            </template>
            <span>Unfold all</span>
          </v-tooltip>
        </v-toolbar>

        <v-list expand dense>
          <v-list-group
            v-for="group in graphData.groups"
            :key="group.id"
            v-model:value="isOpen[group.id]"
            :color="group.hardColor"
            :title="group.label"
          >

            <template v-slot:activator>
              <v-list-item-content>
                <v-list-item-title
                  v-text="group.label"
                  v-bind:style="{color: group.hardColor}"
                ></v-list-item-title>
              </v-list-item-content>
              <v-icon
                v-if="graphData.isGroupEnabled(group.id)"
                v-bind:style="{color: group.hardColor}"
                @click.stop="toggleGroupEnabled(group.id)"
                title="Hide group"
              >mdi-eye-outline</v-icon>
              <v-icon v-else
                v-bind:style="{color: group.hardColor}"
                @click.stop="toggleGroupEnabled(group.id)"
                title="Show group"
              >mdi-eye-off-outline</v-icon>

              <v-icon
                v-if="graphData.isGroupExpanded(group.id)"
                v-bind:style="{color: group.hardColor}"
                @click.stop="toggleGroupExpanded(group.id)"
                title="Collapse group"
              > mdi-arrow-expand-vertical </v-icon>
              <v-icon v-else
                v-bind:style="{color: group.hardColor}"
                @click.stop="toggleGroupExpanded(group.id)"
                title="Expand group"
              > mdi-arrow-collapse-vertical </v-icon>
            </template>
            <v-list-item dense
              v-for="nodeID in graphData.allGroups[group.id].nodes"
              :key="nodeID"
              :disabled="!graphData.isGroupEnabled(group.id)"
              @click.stop="toggleNodeEnabled(nodeID)"
              :title="graphData.allNodes[nodeID].name"
            >
              <v-list-item-content>
                <v-list-item-title
                  v-text="graphData.allNodes[nodeID].name"
                />
              </v-list-item-content>
              <v-list-item-action title="Show/hide">
                <v-icon
                  v-if="graphData.isNodeEnabled(nodeID)"
                  :color="group.hardColor"
                >
                  mdi-eye-outline
                </v-icon>
                <v-icon v-else>
                  mdi-eye-off-outline
                </v-icon>
              </v-list-item-action>
            </v-list-item>

          <v-divider></v-divider>
          </v-list-group>
        </v-list>

      </v-navigation-drawer>
  </div>
</template>

<script>
import graphData from "../state/graphData.js";
export default {
  name: "GraphEditor",
  components: {},
  props: ["loaded"],
  data() {
    return {
      sidebar: false,
      graphData,
      isOpen: Object.fromEntries(graphData.groups.map((group) => [group.id, false]))
    }
  },
  methods: {
    hideAll: function () {
      graphData.hideAll();
      this.foldAll();
    },
    showAll: function () {
      graphData.showAll();
    },
    collapseAll: function () {
      graphData.collapseAll();
      this.foldAll();
    },
    expandAll: function () {
      graphData.expandAll();
    },
    foldAll: function () {
      Object.keys(this.isOpen).map((key) => {
        this.isOpen[key] = false;
      });
    },
    unfoldAll: function () {
      Object.keys(this.isOpen).map((key) => {
        this.isOpen[key] = true;
      });
    },
    toggleGroupEnabled: function (groupID) {
      if (graphData.isGroupEnabled(groupID)) {
        graphData.disableGroup(groupID);
      } else {
        graphData.enableGroup(groupID);
      }
    },
    toggleGroupExpanded: function (groupID) {
      if (graphData.isGroupExpanded(groupID)) {
        graphData.collapseGroup(groupID);
      } else {
        graphData.expandGroup(groupID);
      }
    },
    toggleNodeEnabled: function (nodeID) {
      if (graphData.isNodeEnabled(nodeID)) {
        graphData.disableNode(nodeID);
      } else {
        graphData.enableNode(nodeID);
      }
    },
  },
};
</script>
