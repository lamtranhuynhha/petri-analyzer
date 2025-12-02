import React from 'react';
import { FaMousePointer, FaCircle, FaSquare, FaArrowRight, FaDotCircle, FaQuestionCircle } from 'react-icons/fa';
import usePetriNetStore from '../hooks/usePetriNet';

/**
 * Left Toolbar Component - Drawing tools và actions
 */
const LeftToolbar = () => {
  const {
    selectedTool,
    setSelectedTool,
    selectedElement, 
    openModal
  } = usePetriNetStore();
  
  const tools = [
    { id: 'select', icon: FaMousePointer, label: 'Select (S)', shortcut: 'S' },
    { id: 'place', icon: FaCircle, label: 'Place (P)', shortcut: 'P' },
    { id: 'transition', icon: FaSquare, label: 'Transition (T)', shortcut: 'T' },
    { id: 'arc', icon: FaArrowRight, label: 'Arc (A)', shortcut: 'A' },
    { id: 'token', icon: FaDotCircle, label: 'Token (K)', shortcut: 'K' },
  ];
  
  return (
    <div className="w-toolbar bg-white border-r border-gray-300 flex flex-col items-center py-4 gap-4 z-toolbar">
      {/* Tools Section */}
      <div className="flex flex-col gap-2">
        <div className="text-xs font-semibold text-gray-500 text-center mb-2">TOOLS</div>
        {tools.map((tool) => {
          const Icon = tool.icon;
          const isActive = selectedTool === tool.id;
          
          return (
            <button
              key={tool.id}
              onClick={() => setSelectedTool(tool.id)}
              className={`
                w-14 h-14 rounded-lg flex items-center justify-center
                transition-all duration-200
                ${isActive
                  ? 'bg-primary-600 text-white shadow-md'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }
              `}
              title={tool.label}
            >
              <Icon className="text-xl" />
            </button>
          );
        })}
      </div>
      
      {/* Divider */}
      <div className="w-12 h-px bg-gray-300"></div> 
      {/* Help */}
      <div className="flex flex-col gap-2">
         <button
          onClick={() => openModal('welcome')}
          className="w-14 h-14 rounded-lg flex items-center justify-center transition-all duration-200 bg-blue-50 text-blue-600 hover:bg-blue-100 hover:text-blue-700"
          title="Thông tin dự án"
        >
          <FaQuestionCircle className="text-xl" />
        </button>
      </div>
      
      {/* Selection Info */}
      {selectedElement && (
        <div className="flex flex-col items-center gap-1 p-2 bg-blue-50 rounded text-xs max-w-[70px]">
          <div className="font-semibold text-gray-700 text-center">Selected:</div>
          <div className="text-blue-600 font-medium text-center break-all">
            {selectedElement.id}
          </div>
          <div className="text-gray-500 capitalize text-center">
            {selectedElement.type}
          </div>
          {selectedElement.type === 'place' && selectedElement.data?.tokens !== undefined && (
            <div className="text-gray-600 text-center">
              Tokens: {selectedElement.data.tokens}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default LeftToolbar;


