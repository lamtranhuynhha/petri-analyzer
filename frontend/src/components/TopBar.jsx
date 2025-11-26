import React, { useRef } from 'react';
import logoImage from '../assets/hcmut.png';
import { FaFile, FaFolderOpen, FaSave, FaDownload, FaChartBar, FaPlay, FaInfoCircle } from 'react-icons/fa';
import usePetriNetStore from '../hooks/usePetriNet';

/**
 * Top Bar Component - Header với file operations, mode buttons, và status
 */
const TopBar = ({ onNew, onOpen, onSave, onExport }) => {
  const { 
    status, 
    setActiveTab, 
    activeTab,
    places,
    transitions,
    openModal,
    setConfirmAction,
  } = usePetriNetStore();
  
  const [showExportMenu, setShowExportMenu] = React.useState(false);
  const fileInputRef = useRef(null);
  
  const handleNew = () => {
    setConfirmAction({
      title: 'Tạo mới Petri Net?',
      message: 'Tất cả thay đổi chưa lưu sẽ bị mất. Bạn có chắc chắn?',
      onConfirm: onNew,
    });
    openModal('confirm');
  };
  
  const handleOpenClick = () => {
    fileInputRef.current?.click();
  };
  
  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      onOpen(file);
    }
    e.target.value = ''; // Reset input
  };
  
  const handleExport = (format) => {
    onExport(format);
    setShowExportMenu(false);
  };
  
  return (
    <div className="h-topbar bg-white border-b border-gray-300 shadow-sm flex items-center justify-between px-4 z-topbar">
      {/* Left: Logo & File Operations */}
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <img 
            src={logoImage} 
            alt="Petri Analyzer Logo" 
            className="h-16 w-16 object-contain"
          />
          <h1 className="text-xl font-bold text-gray-800">Petri Analyzer</h1>
        </div>
        
        <div className="h-8 w-px bg-gray-300"></div>
        
        <div className="flex items-center gap-2">
          <button
            onClick={handleNew}
            className="btn-icon tooltip-container"
            title="Tạo mới (Ctrl+N)"
          >
            <FaFile className="text-gray-600" />
          </button>
          
          <button
            onClick={handleOpenClick}
            className="btn-icon tooltip-container"
            title="Mở file (Ctrl+O)"
          >
            <FaFolderOpen className="text-gray-600" />
          </button>
          <input
            ref={fileInputRef}
            type="file"
            accept=".pnml,.json"
            onChange={handleFileChange}
            className="hidden"
          />
          
          <button
            onClick={onSave}
            className="btn-icon tooltip-container"
            title="Lưu (Ctrl+S)"
          >
            <FaSave className="text-gray-600" />
          </button>
          
          <div className="relative">
            <button
              onClick={() => setShowExportMenu(!showExportMenu)}
              className="btn-icon tooltip-container"
              title="Xuất file"
            >
              <FaDownload className="text-gray-600" />
              <span className="ml-1 text-xs">▼</span>
            </button>
            
            {showExportMenu && (
              <div className="absolute top-full left-0 mt-1 bg-white border border-gray-300 rounded shadow-lg py-1 z-50 min-w-[160px]">
                <button
                  onClick={() => handleExport('png')}
                  className="w-full px-4 py-2 text-left hover:bg-gray-100 text-sm"
                >
                  🖼️ Export PNG
                </button>
                <button
                  onClick={() => handleExport('svg')}
                  className="w-full px-4 py-2 text-left hover:bg-gray-100 text-sm"
                >
                  🖼️ Export SVG
                </button>
                <div className="border-t border-gray-200 my-1"></div>
                <button
                  onClick={() => handleExport('pnml')}
                  className="w-full px-4 py-2 text-left hover:bg-gray-100 text-sm"
                >
                  📄 Export PNML
                </button>
                <button
                  onClick={() => handleExport('json')}
                  className="w-full px-4 py-2 text-left hover:bg-gray-100 text-sm"
                >
                  📄 Export JSON
                </button>
                <div className="border-t border-gray-200 my-1"></div>
                <button
                  onClick={() => handleExport('rg')}
                  className="w-full px-4 py-2 text-left hover:bg-gray-100 text-sm"
                >
                  📊 Export RG
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
      
      {/* Center: Mode Buttons */}
      <div className="flex items-center gap-2">
        <button
          onClick={() => setActiveTab('analysis')}
          className={`px-4 py-2 rounded font-medium transition-colors duration-200 flex items-center gap-2 ${
            activeTab === 'analysis'
              ? 'bg-primary-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          <FaChartBar />
          Analyze
        </button>
        
        <button
          onClick={() => setActiveTab('simulation')}
          className={`px-4 py-2 rounded font-medium transition-colors duration-200 flex items-center gap-2 ${
            activeTab === 'simulation'
              ? 'bg-primary-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          <FaPlay />
          Simulate
        </button>
      </div>
      
      {/* Right: Status Panel */}
      <div className="flex items-center gap-3 text-sm">
        <div className="flex items-center gap-2 px-3 py-1 bg-gray-100 rounded">
          <span className="font-medium text-gray-600">Net:</span>
          {status.isBounded === null ? (
            <span className="text-gray-500">-</span>
          ) : status.isBounded ? (
            <span className="text-green-600 font-semibold">✅ BOUNDED</span>
          ) : (
            <span className="text-red-600 font-semibold">⚠️ UNBOUNDED</span>
          )}
        </div>
        
        <div className="flex items-center gap-2 px-3 py-1 bg-gray-100 rounded">
          <span className="font-medium text-gray-600">Elements:</span>
          <span className="text-gray-800">
            {places.length}P, {transitions.length}T
          </span>
        </div>
        
        {status.stateCount > 0 && (
          <div className="flex items-center gap-2 px-3 py-1 bg-gray-100 rounded">
            <span className="font-medium text-gray-600">States:</span>
            <span className="text-gray-800">{status.stateCount}</span>
          </div>
        )}
        
        {status.hasWarning && (
          <div className="flex items-center gap-2 px-3 py-1 bg-yellow-100 rounded text-yellow-700">
            <FaInfoCircle />
            <span className="text-xs font-medium">{status.warningMessage || 'State explosion'}</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default TopBar;


