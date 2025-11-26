import React from 'react';
import { Handle, Position } from 'reactflow';
import usePetriNetStore from '../../hooks/usePetriNet';

/**
 * Custom Place Node cho React Flow
 * Hiển thị hình tròn với token count và label
 */
const PlaceNode = ({ id, data, selected }) => {
  const { updatePlace, setSelectedElement, currentMarking } = usePetriNetStore();
  
  // Lấy số token hiện tại (ưu tiên từ simulation marking)
  const tokens = currentMarking[id] !== undefined ? currentMarking[id] : (data.tokens || 0);
  
  const handleClick = () => {
    setSelectedElement({
      type: 'place',
      id,
      data: { ...data, tokens }
    });
  };
  
  // Render tokens as dots
  const renderTokens = () => {
    if (tokens === 0) return null;
    
    // Logic vẽ token thông minh hơn
    if (tokens <= 5) {
      // Định nghĩa vị trí tương đối so với tâm (30,30)
      let pos = [];
      if (tokens === 1) pos = [[0,0]];
      else if (tokens === 2) pos = [[-10,0], [10,0]];
      else if (tokens === 3) pos = [[-10,-8], [10,-8], [0,10]];
      else if (tokens === 4) pos = [[-10,-10], [10,-10], [-10,10], [10,10]];
      else if (tokens === 5) pos = [[-12,-12], [12,-12], [-12,12], [12,12], [0,0]];
      
      return pos.map((p, idx) => (
        <circle
          key={idx}
          cx={30 + p[0]}
          cy={30 + p[1]}
          r="4" // Tăng kích thước token một chút
          fill="#1e293b"
        />
      ));
    } else {
      return (
        <text x="30" y="36" textAnchor="middle" fontSize="18" fontWeight="bold" fill="#1e293b">
          {tokens}
        </text>
      );
    }
};
  
  return (
    <div
      onClick={handleClick}
      className={`place-node ${selected ? 'selected' : ''}`}
    >
      <svg width="60" height="60" className="place-svg">
        {/* Main circle */}
        <circle
          cx="30"
          cy="30"
          r="25"
          fill="white"
          stroke={selected ? '#3b82f6' : '#64748b'}
          strokeWidth={selected ? 3 : 2}
          className="place-circle transition-all duration-200"
        />
        
        {/* Tokens */}
        {renderTokens()}
        
        {/* Hover effect circle */}
        <circle
          cx="30"
          cy="30"
          r="25"
          fill="transparent"
          className="hover:fill-blue-50 hover:fill-opacity-30 transition-all duration-200"
        />
      </svg>
      
      {/* Label */}
      <div className="place-label text-xs font-medium text-gray-700 text-center mt-1">
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

export default PlaceNode;


