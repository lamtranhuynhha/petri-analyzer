import React from 'react';
import { FaTrash } from 'react-icons/fa';
import usePetriNetStore from '../../hooks/usePetriNet';

/**
 * Properties Tab - Hiển thị và edit properties của element được chọn
 */
const PropertiesTab = () => {
  const {
    selectedElement,
    updatePlace,
    updateTransition,
    updateArc,
    deletePlace,
    deleteTransition,
    deleteArc,
    arcs,
    getEnabledTransitions,
    analysisResults,
  } = usePetriNetStore();
  
  if (!selectedElement) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-gray-500">
        <div className="text-4xl mb-2">👆</div>
        <p className="text-sm text-center">Chọn một element để xem properties</p>
      </div>
    );
  }
  
  const { type, id, data } = selectedElement;
  
  // PLACE properties
  if (type === 'place') {
    const handleTokenChange = (value) => {
      const tokens = Math.max(0, parseInt(value) || 0);
      updatePlace(id, { tokens });
    };
    
    const handleLabelChange = (value) => {
      updatePlace(id, { label: value });
    };
    
    // Tìm connections
    const inputArcs = arcs.filter(a => a.target === id);
    const outputArcs = arcs.filter(a => a.source === id);
    
    return (
      <div className="p-4 space-y-4">
        <div className="bg-blue-50 p-3 rounded">
          <div className="font-semibold text-blue-900">📍 Place: {id}</div>
        </div>
        
        <div className="space-y-3">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              ID
            </label>
            <input
              type="text"
              value={id}
              disabled
              className="input w-full bg-gray-100 cursor-not-allowed"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Label
            </label>
            <input
              type="text"
              value={data.label || id}
              onChange={(e) => handleLabelChange(e.target.value)}
              className="input w-full"
              placeholder="Nhập label..."
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Tokens
            </label>
            <div className="flex items-center gap-2">
              <input
                type="number"
                min="0"
                value={data.tokens || 0}
                onChange={(e) => handleTokenChange(e.target.value)}
                className="input w-full"
              />
              <button
                onClick={() => handleTokenChange((data.tokens || 0) + 1)}
                className="px-3 py-2 bg-green-500 text-white rounded hover:bg-green-600"
              >
                +
              </button>
              <button
                onClick={() => handleTokenChange((data.tokens || 0) - 1)}
                className="px-3 py-2 bg-red-500 text-white rounded hover:bg-red-600"
              >
                -
              </button>
            </div>
          </div>
        </div>
        
        <div className="border-t pt-3">
          <div className="text-sm font-medium text-gray-700 mb-2">Connections</div>
          
          {inputArcs.length > 0 && (
            <div className="mb-2">
              <div className="text-xs text-gray-500 mb-1">Input from:</div>
              {inputArcs.map(arc => (
                <div key={arc.id} className="text-sm text-gray-700 ml-2">
                  • {arc.source} (weight: {arc.weight || 1})
                </div>
              ))}
            </div>
          )}
          
          {outputArcs.length > 0 && (
            <div>
              <div className="text-xs text-gray-500 mb-1">Output to:</div>
              {outputArcs.map(arc => (
                <div key={arc.id} className="text-sm text-gray-700 ml-2">
                  • {arc.target} (weight: {arc.weight || 1})
                </div>
              ))}
            </div>
          )}
          
          {inputArcs.length === 0 && outputArcs.length === 0 && (
            <div className="text-sm text-gray-400 italic">No connections</div>
          )}
        </div>
        
        <button
          onClick={() => deletePlace(id)}
          className="w-full btn-danger flex items-center justify-center gap-2"
        >
          <FaTrash />
          Delete Place
        </button>
      </div>
    );
  }
  
  // TRANSITION properties
  if (type === 'transition') {
    const handleLabelChange = (value) => {
      updateTransition(id, { label: value });
    };
    
    const inputArcs = arcs.filter(a => a.target === id);
    const outputArcs = arcs.filter(a => a.source === id);
    const enabledTransitions = getEnabledTransitions();
    const isEnabled = enabledTransitions.some(t => t.id === id);
    const livenessLevel = data.livenessLevel || analysisResults.liveness?.details?.[id];
    
    return (
      <div className="p-4 space-y-4">
        <div className="bg-purple-50 p-3 rounded">
          <div className="font-semibold text-purple-900">🔄 Transition: {id}</div>
        </div>
        
        <div className="space-y-3">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              ID
            </label>
            <input
              type="text"
              value={id}
              disabled
              className="input w-full bg-gray-100 cursor-not-allowed"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Label
            </label>
            <input
              type="text"
              value={data.label || id}
              onChange={(e) => handleLabelChange(e.target.value)}
              className="input w-full"
              placeholder="Nhập label..."
            />
          </div>
        </div>
        
        <div className="border-t pt-3">
          <div className="text-sm font-medium text-gray-700 mb-2">Information</div>
          
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-600">Preconditions:</span>
              <span className="font-semibold">{inputArcs.length}</span>
            </div>
            
            <div className="flex justify-between">
              <span className="text-gray-600">Postconditions:</span>
              <span className="font-semibold">{outputArcs.length}</span>
            </div>
            
            <div className="flex justify-between">
              <span className="text-gray-600">Status:</span>
              <span className={`font-semibold ${isEnabled ? 'text-green-600' : 'text-red-600'}`}>
                {isEnabled ? '✅ Enabled' : '❌ Disabled'}
              </span>
            </div>
            
            {livenessLevel && (
              <div className="flex justify-between">
                <span className="text-gray-600">Liveness:</span>
                <span className="font-semibold text-blue-600">{livenessLevel}</span>
              </div>
            )}
          </div>
        </div>
        
        <button
          onClick={() => deleteTransition(id)}
          className="w-full btn-danger flex items-center justify-center gap-2"
        >
          <FaTrash />
          Delete Transition
        </button>
      </div>
    );
  }
  
  // ARC properties
  if (type === 'arc') {
    const handleWeightChange = (value) => {
      const weight = Math.max(1, parseInt(value) || 1);
      updateArc(id, { weight });
    };
    
    return (
      <div className="p-4 space-y-4">
        <div className="bg-green-50 p-3 rounded">
          <div className="font-semibold text-green-900">→ Arc: {id}</div>
        </div>
        
        <div className="space-y-3">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              From
            </label>
            <input
              type="text"
              value={data.source || ''}
              disabled
              className="input w-full bg-gray-100 cursor-not-allowed"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              To
            </label>
            <input
              type="text"
              value={data.target || ''}
              disabled
              className="input w-full bg-gray-100 cursor-not-allowed"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Weight
            </label>
            <input
              type="number"
              min="1"
              value={data.weight || 1}
              onChange={(e) => handleWeightChange(e.target.value)}
              className="input w-full"
            />
          </div>
        </div>
        
        <button
          onClick={() => deleteArc(id)}
          className="w-full btn-danger flex items-center justify-center gap-2"
        >
          <FaTrash />
          Delete Arc
        </button>
      </div>
    );
  }
  
  return null;
};

export default PropertiesTab;


