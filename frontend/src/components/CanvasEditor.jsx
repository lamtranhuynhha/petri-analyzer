import React, { useCallback, useRef, useEffect, useMemo } from 'react';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  MarkerType,
  applyNodeChanges,
  applyEdgeChanges,
  ConnectionLineType
} from 'reactflow';
import 'reactflow/dist/style.css';

import usePetriNetStore from '../hooks/usePetriNet';
import PlaceNode from './nodes/PlaceNode';
import TransitionNode from './nodes/TransitionNode';
import ArcEdge from './edges/ArcEdge';

// Hàm helper để tạo Label tự động tăng (p1, p2, t1, t2...)
const generateNextLabel = (prefix, elements) => {
  let maxIndex = 0;
  
  elements.forEach(el => {
    // Kiểm tra xem label hiện tại có bắt đầu bằng prefix không (ví dụ "p1" bắt đầu bằng "p")
    const label = el.label || '';
    if (label.startsWith(prefix)) {
      // Lấy phần số phía sau (ví dụ "p12" -> 12)
      const numberPart = parseInt(label.substring(prefix.length));
      if (!isNaN(numberPart) && numberPart > maxIndex) {
        maxIndex = numberPart;
      }
    }
  });

  return `${prefix}${maxIndex + 1}`;
};

const CanvasEditor = () => {
  const {
    selectedTool,
    places,
    transitions,
    arcs,
    addPlace,
    addTransition,
    addArc,
    updatePlace,
    updateTransition,
    setSelectedElement,
    deleteArc,
    deletePlace,
    deleteTransition,
    firstSelectedNode,
    setFirstSelectedNode
  } = usePetriNetStore();
  
  const reactFlowWrapper = useRef(null);
  const [nodes, setNodes] = useNodesState([]);
  const [edges, setEdges] = useEdgesState([]);
  const [reactFlowInstance, setReactFlowInstance] = React.useState(null);
  const [arcCreationMode, setArcCreationMode] = React.useState(false);

  const nodeTypes = useMemo(() => ({
    place: PlaceNode,
    transition: TransitionNode,
  }), []);

  const edgeTypes = useMemo(() => ({
    arc: ArcEdge,
  }), []);

  // Xác định handle (điểm nối) phù hợp dựa trên vị trí tương đối giữa hai node
  const getHandleIdsForArc = useCallback((sourceNode, targetNode) => {
    if (!sourceNode || !targetNode) {
      return { sourceHandle: undefined, targetHandle: undefined };
    }

    const dx = (targetNode.position?.x || 0) - (sourceNode.position?.x || 0);
    const dy = (targetNode.position?.y || 0) - (sourceNode.position?.y || 0);

    if (Math.abs(dx) > Math.abs(dy)) {
      // Nối theo phương ngang
      if (dx >= 0) {
        return { sourceHandle: 'right-source', targetHandle: 'left-target' };
      }
      return { sourceHandle: 'left-source', targetHandle: 'right-target' };
    } else {
      // Nối theo phương dọc
      if (dy >= 0) {
        return { sourceHandle: 'bottom-source', targetHandle: 'top-target' };
      }
      return { sourceHandle: 'top-source', targetHandle: 'bottom-target' };
    }
  }, []);

  useEffect(() => {
    const newNodes = [
      ...places.map((p) => ({
        id: p.id,
        type: 'place',
        position: p.position || { x: 0, y: 0 },
        data: { label: p.label, tokens: p.tokens },
      })),
      ...transitions.map((t) => ({
        id: t.id,
        type: 'transition',
        position: t.position || { x: 0, y: 0 },
        data: { label: t.label, livenessLevel: t.livenessLevel },
      })),
    ];

    if (JSON.stringify(newNodes.map(n => n.id)) !== JSON.stringify(nodes.map(n => n.id))) {
       setNodes(newNodes);
    } else {
       setNodes((nds) => nds.map(node => {
         const source = newNodes.find(n => n.id === node.id);
         if (source) return { ...node, data: source.data };
         return node;
       }));
    }

    const newEdges = arcs.map((arc) => {
      const sourceNode = newNodes.find((n) => n.id === arc.source);
      const targetNode = newNodes.find((n) => n.id === arc.target);
      const { sourceHandle, targetHandle } = getHandleIdsForArc(sourceNode, targetNode);

      return {
        id: arc.id,
        source: arc.source,
        target: arc.target,
        sourceHandle,
        targetHandle,
        type: 'arc',
        markerEnd: { type: MarkerType.Arrow, width: 20, height: 20 },
        data: { weight: arc.weight },
      };
    });
    
    setEdges(newEdges);
  }, [places, transitions, arcs, setNodes, setEdges, getHandleIdsForArc]);

  const onNodesChange = useCallback(
    (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
    [setNodes]
  );

  const onEdgesChange = useCallback(
    (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)),
    [setEdges]
  );

  const onNodeDragStop = useCallback((event, node) => {
    if (node.type === 'place') {
      updatePlace(node.id, { position: node.position });
    } else if (node.type === 'transition') {
      updateTransition(node.id, { position: node.position });
    }
  }, [updatePlace, updateTransition]);

  const onConnect = useCallback((params) => {
    const { source, target } = params;
    const sourceNode = reactFlowInstance.getNode(source);
    const targetNode = reactFlowInstance.getNode(target);

    if (!sourceNode || !targetNode) return;
    if (sourceNode.type === targetNode.type) return;

    addArc({
      id: `a${Date.now()}`,
      source,
      target,
      weight: 1
    });
  }, [reactFlowInstance, addArc]);

  const onPaneClick = useCallback((event) => {
    if (!reactFlowInstance || !selectedTool) return;
    
    if (selectedTool === 'select') {
      setSelectedElement(null);
      return;
    }

    const position = reactFlowInstance.screenToFlowPosition({
        x: event.clientX,
        y: event.clientY,
    });

    if (selectedTool === 'place') {
      const nextLabel = generateNextLabel('p', places);
      const id = nextLabel; 

      addPlace({
        id: id,
        label: nextLabel, 
        tokens: 0,
        position,
      });
    } else if (selectedTool === 'transition') {
      const nextLabel = generateNextLabel('t', transitions);
      const id = nextLabel;

      addTransition({
        id: id,
        label: nextLabel,
        position,
      });
    }
  }, [reactFlowInstance, selectedTool, addPlace, addTransition, setSelectedElement, places, transitions]);

  const onNodeClick = useCallback((event, node) => {
    console.log('onNodeClick:', { selectedTool, nodeType: node.type, nodeId: node.id, firstSelectedNode });
    
    if (selectedTool === 'token' && node.type === 'place') {
      event.preventDefault(); 
      const currentTokens = node.data.tokens || 0;
      const newTokens = event.shiftKey ? Math.max(0, currentTokens - 1) : currentTokens + 1;
      updatePlace(node.id, { tokens: newTokens });
    } else if (selectedTool === 'arc') {
      event.preventDefault();
      
      if (!firstSelectedNode) {
        console.log('Setting first selected node:', node);
        setFirstSelectedNode(node);
      } else {
        console.log('Second click - checking types:', { firstType: firstSelectedNode.type, secondType: node.type });
        
        if (firstSelectedNode.type !== node.type) {
          const sourceId = firstSelectedNode.id;
          const targetId = node.id;
          
          console.log('Creating arc:', { sourceId, targetId });
          
          const existingArc = arcs.find(arc => 
            (arc.source === sourceId && arc.target === targetId)
          );
          
          if (!existingArc) {
            console.log('Adding new arc');
            addArc({
              id: `a${Date.now()}`,
              source: sourceId,
              target: targetId,
              weight: 1
            });
          } else {
            console.log('Arc already exists');
          }
        } else {
          console.log('Same type nodes - not creating arc');
        }
        setFirstSelectedNode(null);
      }
    } else {
      setSelectedElement({
        type: node.type,
        id: node.id,
        data: node.data,
      });
    }
  }, [selectedTool, updatePlace, setSelectedElement, firstSelectedNode, arcs, addArc]);

  const onNodesDelete = useCallback(
    (nodesToDelete) => {
      nodesToDelete.forEach((node) => {
        if (node.type === 'place') {
          deletePlace(node.id);
        } else if (node.type === 'transition') {
          deleteTransition(node.id);
        }
      });
      setSelectedElement(null);
    },
    [deletePlace, deleteTransition, setSelectedElement]
  );
  
  const onEdgesDelete = useCallback(
    (edgesToDelete) => {
      edgesToDelete.forEach((edge) => {
        deleteArc(edge.id);
      });
      setSelectedElement(null);
    },
    [deleteArc, setSelectedElement]
  );

  return (
    <div className="flex-1 relative" ref={reactFlowWrapper}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeDragStop={onNodeDragStop}
        onConnect={onConnect}
        onNodeClick={onNodeClick}
        onPaneClick={onPaneClick}
        onNodesDelete={onNodesDelete}
        onEdgesDelete={onEdgesDelete}
        onInit={setReactFlowInstance}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        connectionLineType={ConnectionLineType.Straight }
        fitView
        snapToGrid
        minZoom={0.1}
        className="bg-canvas-bg"
        nodesConnectable={false}
        nodesDraggable={selectedTool === 'select'}
      >
        <Background color="#e2e8f0" gap={20} />
        <Controls />
        <MiniMap 
            nodeColor={(n) => n.type === 'place' ? '#3b82f6' : '#1e293b'} 
            maskColor="rgba(0, 0, 0, 0.1)"
        />
      </ReactFlow>

      <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-white/90 backdrop-blur px-4 py-2 rounded shadow text-sm text-gray-600 border border-gray-200">
        Mode: <strong>{selectedTool.toUpperCase()}</strong>
        {selectedTool === 'token' && <span className="ml-2 text-xs text-gray-500">(Click: +1, Shift+Click: -1)</span>}
        {selectedTool === 'arc' && (
          <span className="ml-2 text-xs text-blue-600">
            {firstSelectedNode 
              ? `Selected ${firstSelectedNode.type}: ${firstSelectedNode.data.label || firstSelectedNode.id}. Click another node to connect.`
              : 'Click a place or transition to start connecting.'}
          </span>
        )}
      </div>
    </div>
  );
};

export default CanvasEditor;