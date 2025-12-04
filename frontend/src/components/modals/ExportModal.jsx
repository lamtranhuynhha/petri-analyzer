import React from 'react';
import { FaTimes, FaFileDownload } from 'react-icons/fa';
import usePetriNetStore from '../../hooks/usePetriNet';

/**
 * Export Modal - Chọn format và export
 */
const ExportModal = ({ onExport }) => {
  const { modals, closeModal } = usePetriNetStore();
  const [selectedFormat, setSelectedFormat] = React.useState('json');
  const [includeAnalysis, setIncludeAnalysis] = React.useState(false);
  
  if (!modals?.export) return null;
  
  const formats = [
    { id: 'json', label: 'JSON', icon: '📄', desc: 'JavaScript Object Notation' },
    { id: 'pnml', label: 'PNML', icon: '📄', desc: 'Petri Net Markup Language (XML)' },
    { id: 'png', label: 'PNG', icon: '🖼️', desc: 'Portable Network Graphics' },
    { id: 'svg', label: 'SVG', icon: '🖼️', desc: 'Scalable Vector Graphics' },
  ];
  
  const handleExport = () => {
    onExport(selectedFormat, { includeAnalysis });
    closeModal('export');
  };
  
  return (
    <div className="modal-backdrop" onClick={() => closeModal('export')}>
      <div 
        className="modal-content max-w-lg p-6"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-gray-800">Export Petri Net</h2>
          <button
            onClick={() => closeModal('export')}
            className="text-gray-500 hover:text-gray-700"
          >
            <FaTimes size={20} />
          </button>
        </div>
        
        {/* Format selection */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Chọn định dạng:
          </label>
          <div className="grid grid-cols-2 gap-3">
            {formats.map(format => (
              <button
                key={format.id}
                onClick={() => setSelectedFormat(format.id)}
                className={`
                  p-3 rounded border-2 text-left transition-all duration-200
                  ${selectedFormat === format.id
                    ? 'border-primary-600 bg-primary-50'
                    : 'border-gray-300 hover:border-primary-300'
                  }
                `}
              >
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-2xl">{format.icon}</span>
                  <span className="font-semibold">{format.label}</span>
                </div>
                <div className="text-xs text-gray-600">{format.desc}</div>
              </button>
            ))}
          </div>
        </div>
        
        {/* Options */}
        {(selectedFormat === 'json' || selectedFormat === 'pnml') && (
          <div className="mb-4">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={includeAnalysis}
                onChange={(e) => setIncludeAnalysis(e.target.checked)}
                className="w-4 h-4"
              />
              <span className="text-sm text-gray-700">
                Bao gồm kết quả phân tích
              </span>
            </label>
          </div>
        )}
        
        {/* Actions */}
        <div className="flex gap-3 justify-end pt-4 border-t">
          <button
            onClick={() => closeModal('export')}
            className="btn-secondary"
          >
            Hủy
          </button>
          <button
            onClick={handleExport}
            className="btn-primary flex items-center gap-2"
          >
            <FaFileDownload />
            Export {selectedFormat.toUpperCase()}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ExportModal;


