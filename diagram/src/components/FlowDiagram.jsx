import React, { useState, useEffect, useCallback } from 'react';
import ReactFlow, {
  ReactFlowProvider,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  Handle
} from 'react-flow-renderer';
import axios from 'axios';

const CustomNode = ({ data }) => {
  return (
    <div style={{ padding: '10px', border: '1px solid #ddd', borderRadius: '5px' }}>
      <div>{data.label}</div>
      {data.inputs.map((input, index) => (
        <div key={`input-${index}`}>
          <Handle type="target" position="top" id={`input-${index}`} style={{top: 10 + index * 10}} />
          <input
            value={input}
            onChange={(e) => data.onInputChange(index, e.target.value)}
            style={{marginBottom: '5px'}}
          />
        </div>
      ))}
      <button onClick={data.onAddInput}>+</button>
      <div>
        {data.outputs.map((output, index) => (
          <Handle key={`output-${index}`} type="source" position="bottom" id={`output-${index}`} style={{bottom: 10 + index * 10}} />
        ))}
      </div>
      <button onClick={(event) => {
        event.stopPropagation();
        data.onDelete();
      }}>X</button>
    </div>
  );
};

const FlowDiagram = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [functions, setFunctions] = useState([]);
  const [objects, setObjects] = useState([]);
  const [flowName, setFlowName] = useState('');

  useEffect(() => {
    fetchFunctions();
    fetchObjects();
  }, []);

  const fetchFunctions = async () => {
    const response = await axios.get('http://localhost:5000/api/functions');
    setFunctions(response.data);
  };

  const fetchObjects = async () => {
    const response = await axios.get('http://localhost:5000/api/objects');
    setObjects(response.data);
  };

  const onConnect = useCallback((params) => setEdges((eds) => addEdge(params, eds)), [setEdges]);

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
      type: 'custom',
      position,
      data: {
        label: functions.find(f => f.id === parseInt(functionId)).name,
        inputs: [''],
        outputs: [''],
        onInputChange: (index, value) => {
          setNodes(nds =>
            nds.map(node =>
              node.id === newNode.id
                ? { ...node, data: { ...node.data, inputs: node.data.inputs.map((input, i) => i === index ? value : input) } }
                : node
            )
          );
        },
        onAddInput: () => {
          setNodes(nds =>
            nds.map(node =>
              node.id === newNode.id
                ? { ...node, data: { ...node.data, inputs: [...node.data.inputs, ''] } }
                : node
            )
          );
        },
        onDelete: () => deleteNode(newNode.id)
      }
    };

    setNodes((nds) => {
      const updatedNodes = nds.concat(newNode);

      // Find the last node (excluding the new one)
      const lastNode = nds[nds.length - 1];

      if (lastNode) {
        // Connect the new node to the last node
        setEdges((eds) => eds.concat({
          id: `e${lastNode.id}-${newNode.id}`,
          source: lastNode.id,
          target: newNode.id,
          sourceHandle: 'output-0',
          targetHandle: 'input-0'
        }));
      }

      return updatedNodes;
    });
  };

  const deleteNode = useCallback((nodeId) => {
    setNodes((nds) => nds.filter((node) => node.id !== nodeId));
    setEdges((eds) => eds.filter(
      (edge) => edge.source !== nodeId && edge.target !== nodeId
    ));
  }, [setNodes, setEdges]);

  const runFlow = async () => {
    console.log('Running flow:', { nodes, edges, flowName });
    try {
      const response = await axios.post('http://localhost:5000/api/run_flow', {
        nodes,
        edges,
        flowName
      });
      console.log('Flow result:', response.data);
      await fetchObjects();
    } catch (error) {
      console.error('Error running flow:', error);
    }
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
              nodeTypes={{ custom: CustomNode }}
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