import React from 'react';
import { Handle, Position } from 'reactflow';
import usePetriNetStore from '../../hooks/usePetriNet';

/**
 * Custom Transition Node cho React Flow
 * Hiển thị hình chữ nhật với color coding theo liveness level
 */
const TransitionNode = ({ id, data, selected }) => {
  const { setSelectedElement, getEnabledTransitions, analysisResults = {} } = usePetriNetStore();
  
  // Kiểm tra transition có enabled không - với null safety
  const enabledTransitions =
    typeof getEnabledTransitions === 'function' ? getEnabledTransitions() || [] : [];
  const isEnabled = Array.isArray(enabledTransitions) && enabledTransitions.some((t) => t && t.id === id);
  
  // Lấy liveness level từ analysis results
  const livenessLevel = analysisResults?.liveness?.details?.[id] || null;
  
  const handleClick = () => {
    setSelectedElement({
      type: 'transition',
      id,
      data: { ...data, isEnabled, livenessLevel }
    });
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
      className={`transition-node ${selected ? 'selected' : ''}`}
    >
      <div
        className={`
          relative w-12 h-16 rounded-sm
          flex flex-col items-center justify-center
          transition-all duration-200
          ${selected ? 'ring-2 ring-blue-500 ring-offset-2' : ''}
          ${isEnabled ? 'shadow-md' : 'shadow-sm'}
        `}
        style={{
          backgroundColor: getColor(),
          border: `2px solid ${selected ? '#3b82f6' : '#475569'}`,
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
      <div className="transition-label text-xs font-medium text-gray-700 text-center mt-1">
        {data.label || id}
      </div>
      
      {/* Handles for connections */}
      <Handle
        type="target"
        position={Position.Top}
        className="w-2 h-2 !bg-blue-500"
      />
      <Handle
        type="source"
        position={Position.Bottom}
        className="w-2 h-2 !bg-blue-500"
      />
      <Handle
        type="target"
        position={Position.Left}
        className="w-2 h-2 !bg-blue-500"
      />
      <Handle
        type="source"
        position={Position.Right}
        className="w-2 h-2 !bg-blue-500"
      />
    </div>
  );
};

export default TransitionNode;


