const template = `
  <div class="main-app">
    <network
      class="graph"
      :nodes=nodes
      :edges=edges
      :options=options
    />
  </div>
`;

const getColor = (index, numColors) => `hsl(${index * (360 / numColors)},50%,70%)`;
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
  template,
  props: ['models', 'connections'],
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
              color: getColor(appIndex, Object.keys(models).length),
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
