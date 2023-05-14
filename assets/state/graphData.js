import _ from 'lodash';

// Helpers for deciding what colors to use.
const getColor = (index, numColors) => `hsl(${index * (360 / numColors)},50%,85%)`;
const getBorderColor = (index, numColors) => `hsl(${index * (360 / numColors)},70%,40%)`;

const makeGroupNode = (group) => {
  return {
    id: group.id,
    label: group.name,
    color: {
      background: group.softColor,
      border: group.hardColor,
    },
    shape: "box",
  }
};

const makeNode = (node, background, border, nodeModifiers) => {
  let nodeData = {
    id: node.id,
    label: node.name,
    color: {
      background,
      border,
    },
  }
  _.merge(nodeData, ...node.tags.map((tag) => nodeModifiers[tag]));
  return nodeData;
};

const makeNodeEdge = (edge, edgeModifiers) => {
  let edgeData = {
    from: edge.source,
    to: edge.target,
  };
  _.merge(edgeData, ...edge.tags.map((tag) => edgeModifiers[tag]));
  return edgeData;
};


const makeGroupEdge = (source, target) => {
  let edgeData = {
    from: source,
    to: target,
    arrows: 'middle',
  };
  return edgeData;
};

export default {
  allEdges: [],
  nodes: [],
  edges: [],
  groups: [],
  activeNodeIDs: new Set(),
  activeGroupIDs: new Set(),
  collapsedGroupIDs: new Set(),

  // Toolbar.
  showAll: function () {
    Object.keys(this.allGroups).map((groupID) => {
      this.activeGroupIDs.add(groupID)
    });
    this.update();
  },
  hideAll: function () {
    this.activeGroupIDs.clear();
    this.update();
  },
  expandAll: function () {
    this.collapsedGroupIDs.clear();
    this.update();
  },
  collapseAll: function () {
    Object.keys(this.allGroups).map((groupID) => {
      this.collapsedGroupIDs.add(groupID)
    });
    this.update();
  },

  // Node operations.
  enableNode: function (nodeID) {
    this.activeNodeIDs.add(nodeID);
    this.update();
  },
  disableNode: function (nodeID) {
    this.activeNodeIDs.delete(nodeID);
    this.update();
  },

  //Group operations.
  enableGroup: function (groupID) {
    this.activeGroupIDs.add(groupID);
    this.update();
  },
  disableGroup: function (groupID) {
    this.activeGroupIDs.delete(groupID);
    this.update();
  },
  expandGroup: function (groupID) {
    this.collapsedGroupIDs.delete(groupID);
    this.update();
  },
  collapseGroup: function (groupID) {
    this.collapsedGroupIDs.add(groupID);
    this.update();
  },

  // State queries.
  isNodeEnabled: function (nodeID) {
    let node = this.allNodes[nodeID];
    if (this.collapsedGroupIDs.has(node.group)) {
      return false;
    };
    if (!this.activeGroupIDs.has(node.group)) {
      return false;
    };
    return this.activeNodeIDs.has(nodeID);
  },
  isGroupEnabled: function (groupID) {
    return this.activeGroupIDs.has(groupID);
  },
  isGroupExpanded: function (groupID) {
    return !this.collapsedGroupIDs.has(groupID);
  },
  // Data update.
  update: function () {
    // Empty the nodes array.
    this.nodes.splice(0, this.nodes.length);
    // Add normal nodes.
    Object.keys(this.allNodes).forEach((nodeID) => {
      var node = this.allNodes[nodeID];
      if (this.isNodeEnabled(nodeID)) {
        let group = this.allGroups[node.group];
        this.nodes.push(
          makeNode(node, group.softColor, group.hardColor, this.nodeModifiers)
        );
      }
    });
    // Add group nodes.
    Object.keys(this.allGroups).forEach((groupID) => {
      if (this.isGroupEnabled(groupID) && !this.isGroupExpanded(groupID)) {
        var group = this.allGroups[groupID];
        this.nodes.push(makeGroupNode(group));
      }
    });

    // Empty the groups array.
    this.groups.splice(0, this.groups.length);

    // Populate the groups array.
    Object.keys(this.allGroups).forEach((groupID) => {
      let group = this.allGroups[groupID];
      let softColor;
      let hardColor;
      if (this.isGroupEnabled(groupID)) {
        softColor = group.softColor;
        hardColor = group.hardColor;
      } else {
        softColor = this.inactiveColor;
        hardColor = this.inactiveColor;
      }
      let data = {
        id: group.id,
        label: group.name,
        softColor,
        hardColor,
      };
      this.groups.push(data);
    });
  },
  setup: function(inactiveColor) {
    this.inactiveColor = inactiveColor;
    this.nodeModifiers = window.nodeModifiers;
    this.edgeModifiers = window.edgeModifiers;

    // Store group data for later.
    this.allGroups = {};
    window.schema.groups.forEach((group, i) => {
      this.allGroups[group.id] = {
        ...group,
        softColor: getColor(i, window.schema.groups.length),
        hardColor: getBorderColor(i, window.schema.groups.length),
        nodes: [],
      };
    });
    // Store node data for later.
    this.allNodes = {};
    window.schema.nodes.forEach((node, i) => {
      this.allNodes[node.id] = node;
      this.allGroups[node.group].nodes.push(node.id);
    });
    // Store edge data for later.
    this.allEdges = [...window.schema.edges];

    // Set up the initial state.
    this.collapsedGroupIDs.clear();
    Object.keys(this.allGroups).forEach((groupID) => {
      this.activeGroupIDs.add(groupID);
    });
    Object.keys(this.allNodes).map((nodeID) => {
      this.activeNodeIDs.add(nodeID);
    });
    // Empty the edges array.
    this.edges.splice(0, this.edges.length);
    // Populate the edges array.
    this.allEdges.forEach((edge) => {
      edge = makeNodeEdge(edge, this.edgeModifiers);
      this.edges.push(edge);
    });
    // Also add edges to/from the groups.
    let interGroupRelations = [];
    window.schema.edges.forEach((edge) => {
      // Only external relations matter, not relations to self.
      if (edge.source != edge.target) {
        const fromGroup = this.allNodes[edge.source].group;
        const toGroup = this.allNodes[edge.target].group;
        // Node -> Group
        interGroupRelations.push(makeGroupEdge(edge.source, toGroup));
        // Group -> Node
        interGroupRelations.push(makeGroupEdge(fromGroup, edge.target));
        // Group -> Group
        if (fromGroup != toGroup) {
          interGroupRelations.push(makeGroupEdge(fromGroup, toGroup));
        }
      }
    });
    this.edges.push(..._.uniqWith(interGroupRelations, _.isEqual));

    // Set up the graph.
    this.update();
  }
};
