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
      {Array.isArray(data.inputs) ? data.inputs.map((input, index) => (
        <div key={`input-${index}`}>
          <Handle type="target" position="top" id={`input-${index}`} style={{top: 10 + index * 10}} />
          <input
            value={input}
            onChange={(e) => onInputChange(e, index)}
            onClick={(e) => e.stopPropagation()}
            style={{marginBottom: '5px'}}
          />
        </div>
      )) : (
        <div>
          <Handle type="target" position="top" id="input-0" style={{top: 10}} />
          <input
            value={data.inputs || ''}
            onChange={(e) => onInputChange(e, 0)}
            onClick={(e) => e.stopPropagation()}
            style={{marginBottom: '5px'}}
          />
        </div>
      )}
      <button onClick={onAddInput}>+</button>
      <div>
        {Array.isArray(data.outputs) ? data.outputs.map((output, index) => (
          <Handle key={`output-${index}`} type="source" position="bottom" id={`output-${index}`} style={{bottom: 10 + index * 10}} />
        )) : (
          <Handle type="source" position="bottom" id="output-0" style={{bottom: 10}} />
        )}
      </div>
      <button onClick={onDelete}>X</button>
    </div>
  );
};

const FlowDiagram = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [functions, setFunctions] = useState([]);
  const [commandObjects, setCommandObjects] = useState([]);
  const [flowName, setFlowName] = useState('');
  const [flows, setFlows] = useState([]);
  const [selectedFlow, setSelectedFlow] = useState('');

  useEffect(() => {
    fetchFunctions();
    fetchFlows();
  }, []);

  useEffect(() => {
    if (selectedFlow) {
      fetchCommandObjects(selectedFlow);
      loadFlow(selectedFlow);
    } else {
      setNodes([]);
      setEdges([]);
      setFlowName('');
      setCommandObjects([]);
    }
  }, [selectedFlow]);

  const fetchFunctions = async () => {
    const response = await axios.get('http://localhost:5000/api/functions');
    setFunctions(response.data);
  };

  const fetchFlows = async () => {
    const response = await axios.get('http://localhost:5000/api/flows');
    setFlows(response.data);
  };

  const fetchCommandObjects = async (flowId) => {
    const response = await axios.get(`http://localhost:5000/api/command_objects/${flowId}`);
    setCommandObjects(response.data);
  };


  const loadFlow = async (flowId) => {
    const response = await axios.get(`http://localhost:5000/api/flow/${flowId}`);
    const flowData = response.data;
    setFlowName(flowData.name);

    const newNodes = flowData.commands.map((command, index) => ({
      id: command.id.toString(),
      type: 'custom',
      position: { x: 100, y: index * 150 },
      data: {
        label: command.function_name,
        inputs: command.inputs ? command.inputs.split(',') : [''],
        outputs: command.outputs ? command.outputs.split(',') : [''],
        onInputChange: (nodeId, index, value) => {
          setNodes(nds =>
            nds.map(node =>
              node.id === nodeId
                ? { ...node, data: { ...node.data, inputs: Array.isArray(node.data.inputs)
                    ? node.data.inputs.map((input, i) => i === index ? value : input)
                    : [value] } }
                : node
            )
          );
        },
        onAddInput: (nodeId) => {
          setNodes(nds =>
            nds.map(node =>
              node.id === nodeId
                ? { ...node, data: { ...node.data, inputs: Array.isArray(node.data.inputs)
                    ? [...node.data.inputs, '']
                    : [node.data.inputs || '', ''] } }
                : node
            )
          );
        },
        onDelete: deleteNode
      }
    }));

    const newEdges = flowData.commands.slice(0, -1).map((command, index) => ({
      id: `e${command.id}-${flowData.commands[index + 1].id}`,
      source: command.id.toString(),
      target: flowData.commands[index + 1].id.toString(),
      sourceHandle: 'output-0',
      targetHandle: 'input-0'
    }));

    setNodes(newNodes);
    setEdges(newEdges);
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
        // Adjust the position of the new node to create more space
        newNode.position.y = lastNode.position.y + 150; // Increase this value for more vertical space
        newNode.position.x = lastNode.position.x + 50; // Add some horizontal offset as well

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
    const position = {
      x: 100,
      y: (nodes.length * 150) + 100 // Increase vertical spacing here as well
    };
    addNodeToFlow(functionId, position);
  }, [nodes.length, addNodeToFlow]);

  const deleteNode = useCallback((nodeId) => {
    setNodes((nds) => nds.filter((node) => node.id !== nodeId));
    setEdges((eds) => eds.filter(
      (edge) => edge.source !== nodeId && edge.target !== nodeId
    ));
  }, [setNodes, setEdges]);

  const onConnect = useCallback((params) => setEdges((eds) => addEdge(params, eds)), [setEdges]);

  const onDragOver = useCallback((event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const runFlow = async () => {
    console.log('Running flow:', { nodes, edges, flowName });
    try {
      const response = await axios.post('http://localhost:5000/api/run_flow', {
        nodes,
        edges,
        flowName
      });
      console.log('Flow result:', response.data);

      // Odśwież listę flows
      await fetchFlows();

      // Jeśli jest wybrany flow, odśwież jego command objects
      if (selectedFlow) {
        await fetchCommandObjects(selectedFlow);
      } else {
        // Jeśli nie ma wybranego flow, wybierz nowo utworzony flow
        const newFlow = response.data.flow_id;
        setSelectedFlow(newFlow);
        await fetchCommandObjects(newFlow);
      }

      // Odśwież listę wszystkich command objects
      await fetchAllCommandObjects();
    } catch (error) {
      console.error('Error running flow:', error);
    }
  };

  // Dodaj nową funkcję do pobierania wszystkich command objects
  const fetchAllCommandObjects = async () => {
    const response = await axios.get('http://localhost:5000/api/all_command_objects');
    setCommandObjects(response.data);
  };

  const deleteFlow = async () => {
    if (!selectedFlow) return;

    try {
      await axios.delete(`http://localhost:5000/api/flow/${selectedFlow}`);
      setSelectedFlow('');
      setNodes([]);
      setEdges([]);
      setFlowName('');
      fetchFlows(); // Odśwież listę flows po usunięciu
      setCommandObjects([]); // Wyczyść command objects
    } catch (error) {
      console.error('Error deleting flow:', error);
    }
  };

  const nodeTypes = useMemo(() => ({ custom: CustomNode }), []);

  return (
    <div style={{ height: '100vh', display: 'flex' }}>
      <div style={{ width: '200px', padding: '10px' }}>
        <h3>Functions</h3>
        {functions.map((func) => (
          <div
            key={func.id}
            draggable
            onDragStart={(event) => event.dataTransfer.setData('application/reactflow', func.id)}
            onClick={() => onFunctionClick(func.id)}
            style={{ margin: '5px', padding: '5px', border: '1px solid black', cursor: 'pointer' }}
          >
            {func.name}
          </div>
        ))}
      </div>
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <div style={{ display: 'flex', alignItems: 'center', padding: '10px' }}>
          <input
            type="text"
            value={flowName}
            onChange={(e) => setFlowName(e.target.value)}
            placeholder="Enter flow name"
            style={{ flex: 1, marginRight: '10px', padding: '5px' }}
          />
          <button onClick={runFlow} style={{ padding: '5px 10px' }}>Run Flow</button>
        </div>
        <ReactFlowProvider>
          <div style={{ flex: 1 }}>
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
              <Controls />
              <Background />
            </ReactFlow>
          </div>
        </ReactFlowProvider>
      </div>
      <div style={{ width: '300px', padding: '10px', overflowY: 'auto' }}>
        <h3>Flows</h3>
        <div style={{ display: 'flex', marginBottom: '10px' }}>
          <select
            value={selectedFlow}
            onChange={(e) => setSelectedFlow(e.target.value)}
            style={{ flex: 1, marginRight: '10px', padding: '5px' }}
          >
            <option value="">Select a flow</option>
            {flows.map(flow => (
              <option key={flow.id} value={flow.id}>{flow.name}</option>
            ))}
          </select>
          <button
            onClick={deleteFlow}
            disabled={!selectedFlow}
            style={{ padding: '5px 10px' }}
          >
            Delete Flow
          </button>
        </div>
        <h3>Command Objects</h3>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th style={tableHeaderStyle}>Function</th>
              <th style={tableHeaderStyle}>Input</th>
              <th style={tableHeaderStyle}>Output</th>
            </tr>
          </thead>
          <tbody>
            {commandObjects.map((obj) => (
              <tr key={obj.id}>
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
