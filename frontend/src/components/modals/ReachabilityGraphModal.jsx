import React from 'react';
import { FaTimes, FaSearchPlus, FaSearchMinus, FaExpand, FaDownload } from 'react-icons/fa';
import usePetriNetStore from '../../hooks/usePetriNet';

/**
 * Reachability Graph Modal - Hiển thị RG với zoom, pan, legend
 */
const ReachabilityGraphModal = () => {
  const { modals, closeModal, analysisResults } = usePetriNetStore();
  const [zoom, setZoom] = React.useState(100);
  const [showLegend, setShowLegend] = React.useState(true);
  
  if (!modals?.reachabilityGraph) return null;
  
  const rgData = analysisResults.reachability;
  
  if (!rgData) {
    return (
      <div className="modal-backdrop" onClick={() => closeModal('reachabilityGraph')}>
        <div className="modal-content p-6" onClick={(e) => e.stopPropagation()}>
          <p>Chưa có dữ liệu Reachability Graph. Vui lòng chạy phân tích trước.</p>
          <button onClick={() => closeModal('reachabilityGraph')} className="btn-secondary mt-4">
            Đóng
          </button>
        </div>
      </div>
    );
  }
  
  const handleZoomIn = () => setZoom(Math.min(200, zoom + 10));
  const handleZoomOut = () => setZoom(Math.max(50, zoom - 10));
  const handleFit = () => setZoom(100);
  
  const handleExport = () => {
    // Export RG as image
    alert('Export RG functionality coming soon!');
  };
  
  return (
    <div className="modal-backdrop" onClick={() => closeModal('reachabilityGraph')}>
      <div 
        className="modal-content max-w-6xl w-full h-5/6 flex flex-col"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b">
          <h2 className="text-xl font-bold text-gray-800">
            Reachability Graph Viewer
          </h2>
          <div className="flex items-center gap-2">
            <button onClick={handleExport} className="btn-icon" title="Export">
              <FaDownload />
            </button>
            <button onClick={() => closeModal('reachabilityGraph')} className="btn-icon">
              <FaTimes size={20} />
            </button>
          </div>
        </div>
        
        {/* Controls */}
        <div className="flex items-center justify-between p-3 bg-gray-50 border-b">
          <div className="flex items-center gap-2">
            <button onClick={handleZoomOut} className="btn-icon" title="Zoom out">
              <FaSearchMinus />
            </button>
            <span className="text-sm font-medium text-gray-700 min-w-[60px] text-center">
              {zoom}%
            </span>
            <button onClick={handleZoomIn} className="btn-icon" title="Zoom in">
              <FaSearchPlus />
            </button>
            <button onClick={handleFit} className="btn-icon" title="Fit to view">
              <FaExpand />
            </button>
          </div>
          
          <div className="flex items-center gap-2">
            <label className="flex items-center gap-2 text-sm cursor-pointer">
              <input
                type="checkbox"
                checked={showLegend}
                onChange={(e) => setShowLegend(e.target.checked)}
              />
              <span>Show Legend</span>
            </label>
          </div>
        </div>
        
        {/* Graph Content */}
        <div className="flex-1 overflow-auto p-4 bg-gray-100">
          <div 
            className="bg-white rounded shadow-sm p-4 inline-block min-w-full"
            style={{ transform: `scale(${zoom / 100})`, transformOrigin: 'top left' }}
          >
            {/* RG Visualization - sẽ render từ backend SVG hoặc dùng library */}
            {rgData.graph_image ? (
              <img 
                src={rgData.graph_image} 
                alt="Reachability Graph"
                className="max-w-full h-auto"
              />
            ) : (
              <div className="text-center py-20">
                <div className="text-4xl mb-4">📊</div>
                <p className="text-gray-600">
                  Rendering Reachability Graph...
                </p>
                <div className="mt-4 text-sm text-gray-500">
                  <div>States: {rgData.states?.length || 0}</div>
                  <div>Edges: {rgData.edges?.length || 0}</div>
                </div>
              </div>
            )}
          </div>
        </div>
        
        {/* Legend */}
        {showLegend && (
          <div className="p-4 border-t bg-gray-50">
            <div className="flex items-center gap-6 text-sm">
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded-full bg-green-500"></div>
                <span>Initial state</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded-full bg-red-500"></div>
                <span>Deadlock</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded-full bg-blue-500"></div>
                <span>Current (simulation)</span>
              </div>
              <div className="flex items-center gap-2">
                <span>→</span>
                <span>Transitions</span>
              </div>
            </div>
          </div>
        )}
        
        {/* Statistics */}
        <div className="p-4 border-t bg-white">
          <div className="flex items-center gap-6 text-sm">
            <div>
              <span className="text-gray-600">Total states:</span>{' '}
              <span className="font-semibold">{rgData.states?.length || 0}</span>
            </div>
            <div>
              <span className="text-gray-600">Deadlocks:</span>{' '}
              <span className="font-semibold text-red-600">
                {rgData.deadlocks?.length || 0}
              </span>
            </div>
            {rgData.max_tokens && (
              <div>
                <span className="text-gray-600">Max tokens:</span>{' '}
                <span className="font-semibold">{rgData.max_tokens}</span>
              </div>
            )}
          </div>
        </div>
        
        {/* Close button */}
        <div className="p-4 border-t flex justify-center">
          <button
            onClick={() => closeModal('reachabilityGraph')}
            className="btn-secondary"
          >
            Đóng
          </button>
        </div>
      </div>
    </div>
  );
};

export default ReachabilityGraphModal;


