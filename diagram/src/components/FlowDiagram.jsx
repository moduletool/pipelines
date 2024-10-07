import React, { useState, useEffect } from 'react';
import ReactFlow, { 
  ReactFlowProvider, 
  Controls, 
  Background, 
  useNodesState, 
  useEdgesState,
  addEdge
} from 'react-flow-renderer';
import axios from 'axios';

const FlowDiagram = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [functions, setFunctions] = useState([]);
  const [objects, setObjects] = useState([]);
  const [flowName, setFlowName] = useState('');

  useEffect(() => {
    // Fetch functions and objects from the backend
    fetchFunctions();
    fetchObjects();
  }, []);

  const fetchFunctions = async () => {
    const response = await axios.get('/api/functions');
    setFunctions(response.data);
  };

  const fetchObjects = async () => {
    const response = await axios.get('/api/objects');
    setObjects(response.data);
  };

  const onConnect = (params) => setEdges((eds) => addEdge(params, eds));

  const onDragOver = (event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  };

  const onDrop = (event) => {
    event.preventDefault();
    const functionId = event.dataTransfer.getData('application/reactflow');
    const position = { x: event.clientX, y: event.clientY };
    const newNode = {
      id: `${Date.now()}`,
      type: 'default',
      position,
      data: { label: functions.find(f => f.id === parseInt(functionId)).name }
    };
    setNodes((nds) => nds.concat(newNode));
  };

  const runFlow = async () => {
    // Implement the logic to run the flow
    // This should send the flow data to the backend for processing
    console.log('Running flow:', { nodes, edges, flowName });
    // After running, fetch updated objects
    await fetchObjects();
  };

  return (
    <div style={{ height: '100vh', display: 'flex' }}>
      <div style={{ width: '200px', padding: '10px' }}>
        <h3>Functions</h3>
        {functions.map((func) => (
          <div
            key={func.id}
            draggable
            onDragStart={(event) => event.dataTransfer.setData('application/reactflow', func.id)}
            style={{ margin: '5px', padding: '5px', border: '1px solid black', cursor: 'move' }}
          >
            {func.name}
          </div>
        ))}
      </div>
      <div style={{ flex: 1 }}>
        <input
          type="text"
          value={flowName}
          onChange={(e) => setFlowName(e.target.value)}
          placeholder="Enter flow name"
          style={{ width: '100%', padding: '5px' }}
        />
        <ReactFlowProvider>
          <div style={{ height: 'calc(100% - 40px)' }}>
            <ReactFlow
              nodes={nodes}
              edges={edges}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              onConnect={onConnect}
              onDrop={onDrop}
              onDragOver={onDragOver}
            >
              <Controls />
              <Background />
            </ReactFlow>
          </div>
        </ReactFlowProvider>
        <button onClick={runFlow} style={{ width: '100%', padding: '10px' }}>Run Flow</button>
      </div>
      <div style={{ width: '200px', padding: '10px' }}>
        <h3>Objects</h3>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Input</th>
              <th>Output</th>
            </tr>
          </thead>
          <tbody>
            {objects.map((obj) => (
              <tr key={obj.id}>
                <td>{obj.id}</td>
                <td>{obj.input}</td>
                <td>{obj.output}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default FlowDiagram;