import React from 'react';
import { Handle, Position } from 'reactflow';
import usePetriNetStore from '../../hooks/usePetriNet';

/**
 * Custom Transition Node cho React Flow
 * Hiển thị hình chữ nhật lớn với color coding theo liveness level
 */
const TransitionNode = ({ id, data, selected }) => {
  const { setSelectedElement, getEnabledTransitions, analysisResults = {}, selectedTool, firstSelectedNode } = usePetriNetStore();
  
  // Kiểm tra transition có enabled không - với null safety
  const enabledTransitions = (getEnabledTransitions && typeof getEnabledTransitions === 'function') 
    ? (getEnabledTransitions() || []) 
    : [];
  const isEnabled = Array.isArray(enabledTransitions) && enabledTransitions.some(t => t?.id === id);
  
  // Lấy liveness level từ analysis results
  const livenessLevel = analysisResults?.liveness?.details?.[id] || null;
  
  // Kiểm tra nếu node đang được chọn để tạo arc
  const isArcSource = selectedTool === 'arc' && firstSelectedNode?.id === id;
  
  const handleClick = () => {
    if (selectedTool !== 'arc') {
      setSelectedElement({
        type: 'transition',
        id,
        data: { ...data, isEnabled, livenessLevel }
      });
    }
  };
  
  // Xác định màu sắc theo liveness level
  const getColor = () => {
    if (livenessLevel === 'Dead') return '#9ca3af'; // gray
    if (livenessLevel === 'L1') return '#93c5fd'; // light blue
    if (livenessLevel === 'L3') return '#fb923c'; // orange
    if (livenessLevel === 'Live' || livenessLevel === 'L4') return '#22c55e'; // green
    
    // Mặc định: màu theo enabled state
    return isEnabled ? '#10b981' : '#1e293b';
  };
  
  // const getStatusIndicator = () => {
  //   if (isEnabled) return '✓';
  //   return '';
  // };
  
  return (
    <div
      onClick={handleClick}
      className={`transition-node ${selected ? 'selected' : ''} ${isArcSource ? 'arc-source' : ''}`}
    >
      <div
        className={`
          relative w-5 h-12 rounded-sm
          flex flex-col items-center justify-center
          transition-all duration-200 cursor-pointer
          ${selected ? 'ring-2 ring-blue-500 ring-offset-2' : ''}
          ${isEnabled ? 'shadow-md' : 'shadow-sm'}
          ${isArcSource ? 'ring-4 ring-green-500 ring-offset-2' : ''}
        `}
        style={{
          backgroundColor: getColor(),
          border: `1px solid ${isArcSource ? '#10b981' : (selected ? '#3b82f6' : '#475569')}`,
        }}
      >
        {/* Status indicator */}
        {isEnabled && (
          <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full flex items-center justify-center text-white text-xs">
            ✓
          </div>
        )}
        
        {/* Liveness indicator (nếu có) */}
        {livenessLevel && (
          <div className="absolute -top-2 -left-2 px-1 text-xs bg-white rounded shadow text-gray-700 font-semibold">
            {livenessLevel}
          </div>
        )}
      </div>
      
      {/* Label */}
      <div className="transition-label text-sm font-medium text-gray-700 text-center mt-2">
        {data.label || id}
      </div>

      {/* Handles for connections (ẩn, chỉ để React Flow gắn edge) */}
      {/* Top side */}
      <Handle
        id="top-target"
        type="target"
        position={Position.Top}
        className="opacity-0 w-1 h-1 pointer-events-none"
      />
      <Handle
        id="top-source"
        type="source"
        position={Position.Top}
        className="opacity-0 w-1 h-1 pointer-events-none"
      />

      {/* Bottom side */}
      <Handle
        id="bottom-target"
        type="target"
        position={Position.Bottom}
        className="opacity-0 w-1 h-1 pointer-events-none"
      />
      <Handle
        id="bottom-source"
        type="source"
        position={Position.Bottom}
        className="opacity-0 w-1 h-1 pointer-events-none"
      />

      {/* Left side */}
      <Handle
        id="left-target"
        type="target"
        position={Position.Left}
        className="opacity-0 w-1 h-1 pointer-events-none"
      />
      <Handle
        id="left-source"
        type="source"
        position={Position.Left}
        className="opacity-0 w-1 h-1 pointer-events-none"
      />

      {/* Right side */}
      <Handle
        id="right-target"
        type="target"
        position={Position.Right}
        className="opacity-0 w-1 h-1 pointer-events-none"
      />
      <Handle
        id="right-source"
        type="source"
        position={Position.Right}
        className="opacity-0 w-1 h-1 pointer-events-none"
      />
    </div>
  );
};

export default TransitionNode;


