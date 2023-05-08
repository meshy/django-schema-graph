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
  edges: [],
  showAll: function(ev) {
    Object.keys(this.activeModels).forEach((app) => {
      this.activeModels[app].visible = true;
    });
  },
  hideAll: function(ev) {
    Object.keys(this.activeModels).forEach((app) => {
      this.activeModels[app].visible = false;
    });
  },
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
  getNodes: function () {
    const modelsAndFunctions = [
      [models, modelNode],
      [abstractModels, abstractModelNode]
    ];
    var nodes = [];
    this.allApps.forEach((app, appIndex) => {
      var appData = this.activeModels[app];
      if (appData.visible) {
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
      }
    });
    return nodes;
  },
  setup() {
    const allApps = [...new Set([
      ...Object.keys(models),
      ...Object.keys(abstractModels)
    ])].sort();
    let activeModels = {};
    allApps.forEach((app, i) => {
      activeModels[app] = {
        expanded: true,
        visible: true,
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

    this.activeModels = activeModels
    this.allApps = allApps
    this.edges = edges
  },
};
