import React, { useState, useEffect, useCallback, useMemo } from 'react';
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

const CustomNode = ({ id, data }) => {
  const onInputChange = (event, index) => {
    event.stopPropagation();
    data.onInputChange(id, index, event.target.value);
  };

  const onAddInput = (event) => {
    event.stopPropagation();
    data.onAddInput(id);
  };

  const onDelete = (event) => {
    event.stopPropagation();
    data.onDelete(id);
  };

  return (
    <div style={{ padding: '10px', border: '1px solid #ddd', borderRadius: '5px', background: 'white' }}>
      <div>{data.label}</div>
      {data.inputs.map((input, index) => (
        <div key={`input-${index}`}>
          <Handle type="target" position="top" id={`input-${index}`} style={{top: 10 + index * 10}} />
          <input
            value={input}
            onChange={(e) => onInputChange(e, index)}
            onClick={(e) => e.stopPropagation()}
            style={{marginBottom: '5px'}}
          />
        </div>
      ))}
      <button onClick={onAddInput}>+</button>
      <div>
        {data.outputs.map((output, index) => (
          <Handle key={`output-${index}`} type="source" position="bottom" id={`output-${index}`} style={{bottom: 10 + index * 10}} />
        ))}
      </div>
      <button onClick={onDelete}>X</button>
    </div>
  );
};

const FlowDiagram = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [functions, setFunctions] = useState([]);
  const [objects, setObjects] = useState([]);
  const [flowName, setFlowName] = useState('');
  const [commandObjects, setCommandObjects] = useState([]);

  useEffect(() => {
    fetchFunctions();
    fetchCommandObjects();
  }, []);

  const fetchFunctions = async () => {
    const response = await axios.get('http://localhost:5000/api/functions');
    setFunctions(response.data);
  };

  const fetchCommandObjects = async () => {
    const response = await axios.get('http://localhost:5000/api/command_objects');
    setCommandObjects(response.data);
  };

  const onConnect = useCallback((params) => {
    setEdges((eds) => addEdge({ ...params, id: `e${params.source}-${params.target}` }, eds));
  }, [setEdges]);

  const onDragOver = (event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  };

  const createNode = useCallback((functionId, position) => {
    const id = `node_${Date.now()}`;
    return {
      id,
      type: 'custom',
      position,
      data: {
        label: functions.find(f => f.id === parseInt(functionId)).name,
        inputs: [''],
        outputs: [''],
        onInputChange: (nodeId, index, value) => {
          setNodes(nds =>
            nds.map(node =>
              node.id === nodeId
                ? { ...node, data: { ...node.data, inputs: node.data.inputs.map((input, i) => i === index ? value : input) } }
                : node
            )
          );
        },
        onAddInput: (nodeId) => {
          setNodes(nds =>
            nds.map(node =>
              node.id === nodeId
                ? { ...node, data: { ...node.data, inputs: [...node.data.inputs, ''] } }
                : node
            )
          );
        },
        onDelete: deleteNode
      }
    };
  }, [functions, setNodes]);

  const addNodeToFlow = useCallback((functionId, position) => {
    const newNode = createNode(functionId, position);
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
  }, [createNode, setNodes, setEdges]);

  const onDrop = useCallback((event) => {
    event.preventDefault();
    const functionId = event.dataTransfer.getData('application/reactflow');
    const position = { x: event.clientX - 250, y: event.clientY };
    addNodeToFlow(functionId, position);
  }, [addNodeToFlow]);

  const onFunctionClick = useCallback((functionId) => {
    const position = { x: 100, y: (nodes.length * 100) + 100 };
    addNodeToFlow(functionId, position);
  }, [nodes.length, addNodeToFlow]);

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
      await fetchCommandObjects();
    } catch (error) {
      console.error('Error running flow:', error);
    }
  };

  const nodeTypes = useMemo(() => ({ custom: CustomNode }), []);

  return (
      <div style={{height: '100vh', display: 'flex'}}>
        <div style={{width: '200px', padding: '10px'}}>
          <h3>Functions</h3>
          {functions.map((func) => (
              <div
                  key={func.id}
                  draggable
                  onDragStart={(event) => event.dataTransfer.setData('application/reactflow', func.id)}
                  onClick={() => onFunctionClick(func.id)}
                  style={{margin: '5px', padding: '5px', border: '1px solid black', cursor: 'pointer'}}
              >
                {func.name}
              </div>
          ))}
        </div>
        <div style={{flex: 1, display: 'flex', flexDirection: 'column'}}>
          <div style={{display: 'flex', alignItems: 'center', padding: '10px'}}>
            <input
                type="text"
                value={flowName}
                onChange={(e) => setFlowName(e.target.value)}
                placeholder="Enter flow name"
                style={{flex: 1, marginRight: '10px', padding: '5px'}}
            />
            <button onClick={runFlow} style={{padding: '5px 10px'}}>Run Flow</button>
          </div>
          <ReactFlowProvider>
            <div style={{flex: 1}}>
              <ReactFlow
                  nodes={nodes}
                  edges={edges}
                  onNodesChange={onNodesChange}
                  onEdgesChange={onEdgesChange}
                  onConnect={onConnect}
                  onDrop={onDrop}
                  onDragOver={onDragOver}
                  nodeTypes={nodeTypes}
              >
                <Controls/>
                <Background/>
              </ReactFlow>
            </div>
          </ReactFlowProvider>
        </div>
        <div style={{width: '300px', padding: '10px', overflowY: 'auto'}}>
          <h3>Command Objects</h3>
          <table style={{width: '100%', borderCollapse: 'collapse'}}>
            <thead>
            <tr>
              <th style={tableHeaderStyle}>Flow</th>
              <th style={tableHeaderStyle}>Function</th>
              <th style={tableHeaderStyle}>Input</th>
              <th style={tableHeaderStyle}>Output</th>
            </tr>
            </thead>
            <tbody>
            {commandObjects.map((obj) => (
                <tr key={obj.id}>
                  <td style={tableCellStyle}>{obj.flow_name}</td>
                  <td style={tableCellStyle}>{obj.function_name}</td>
                  <td style={tableCellStyle}>{obj.input}</td>
                  <td style={tableCellStyle}>{obj.output}</td>
                </tr>
            ))}
            </tbody>
          </table>
        </div>
      </div>
  );
};

const tableHeaderStyle = {
  backgroundColor: '#f2f2f2',
  padding: '8px',
  textAlign: 'left',
  borderBottom: '1px solid #ddd'
};

const tableCellStyle = {
  padding: '8px',
  borderBottom: '1px solid #ddd'
};

export default FlowDiagram;
