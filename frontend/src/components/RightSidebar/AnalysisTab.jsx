import React from 'react';
import { 
  FaSpinner, 
  FaEye, 
  FaExclamationTriangle, 
  FaCheckCircle, 
  FaBug, 
  FaProjectDiagram, 
  FaLayerGroup 
} from 'react-icons/fa';
import { useState } from 'react';
import usePetriNetStore from '../../hooks/usePetriNet';

/**
 * Analysis Tab - Updated UI with Larger Fonts
 */
const AnalysisTab = ({ onAnalyze }) => {
  const {
    loading,
    analysisResults,
    openModal,
    places,
    transitions,
  } = usePetriNetStore();
  
  // State quản lý việc mở rộng/thu gọn các phần
  const [expandedSection, setExpandedSection] = useState({
    structural: true,
    behavioral: true
  });

  const toggleSection = (section) => {
    setExpandedSection(prev => ({ ...prev, [section]: !prev[section] }));
  };
  
  const hasNet = places.length > 0 || transitions.length > 0;
  
  const handleAnalyze = (type) => {
    if (!hasNet) {
      alert('Vui lòng vẽ Petri Net trước khi phân tích!');
      return;
    }
    onAnalyze(type);
  };
  
  const renderNodeSetChips = (nodeSets, colorClass = "bg-blue-100 text-blue-800") => {
    if (!nodeSets || nodeSets.length === 0) return <div className="text-sm text-gray-500 italic">None found</div>;
    
    return (
      <div className="flex flex-wrap gap-1 mt-1">
        {nodeSets.map((set, idx) => (
          <span 
            key={idx} 
            className={`text-sm px-2 py-1 rounded-full border border-opacity-20 cursor-help transition-colors hover:bg-opacity-80 ${colorClass}`}
            title={`Nodes: ${set.join(', ')}`}
          >
            {set.join(', ')}
          </span>
        ))}
      </div>
    );
  };

  return (
    <div className="p-4 space-y-4 overflow-y-auto h-full bg-gray-50">
      
      {/* --- SECTION 1: STRUCTURAL ANALYSIS --- */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <div 
          className="bg-gray-100 p-3 font-semibold text-gray-800 flex justify-between items-center cursor-pointer hover:bg-gray-200 transition"
          onClick={() => toggleSection('structural')}
        >
          <span className="flex items-center gap-2"><FaProjectDiagram className="text-blue-600"/> Structural Analysis</span>
          <span>{expandedSection.structural ? '' : '+'}</span>
        </div>
        
        {expandedSection.structural && (
          <div className="p-3 space-y-4">
            {/* Siphons & Traps */}
            <div>
              <button
                onClick={() => handleAnalyze('siphonsTraps')}
                disabled={loading.siphonsTraps}
                className="w-full btn-secondary btn-sm mb-2"
              >
                {loading.siphonsTraps ? <FaSpinner className="animate-spin inline mr-2" /> : null}
                Compute Siphons & Traps
              </button>
              
              {analysisResults.siphonsTraps && (
                <div className="space-y-3 mt-2">
                  <div className="bg-blue-50 p-2 rounded border border-blue-100">
                    <div className="text-sm font-bold text-blue-700 uppercase mb-1">
                      Minimal Siphons ({analysisResults.siphonsTraps.minimal_siphons?.length || 0})
                    </div>
                    {renderNodeSetChips(analysisResults.siphonsTraps.minimal_siphons, "bg-indigo-100 text-indigo-700 border-indigo-200")}
                  </div>
                  
                  <div className="bg-green-50 p-2 rounded border border-green-100">
                    <div className="text-sm font-bold text-green-700 uppercase mb-1">
                      Minimal Traps ({analysisResults.siphonsTraps.minimal_traps?.length || 0})
                    </div>
                    {renderNodeSetChips(analysisResults.siphonsTraps.minimal_traps, "bg-teal-100 text-teal-700 border-teal-200")}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* --- SECTION 2: BEHAVIORAL PROPERTIES --- */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <div 
          className="bg-gray-100 p-3 font-semibold text-gray-800 flex justify-between items-center cursor-pointer hover:bg-gray-200 transition"
          onClick={() => toggleSection('behavioral')}
        >
          <span className="flex items-center gap-2"><FaLayerGroup className="text-purple-600"/> Behavioral Properties</span>
          <span>{expandedSection.behavioral ? '' : '+'}</span>
        </div>
        
        {expandedSection.behavioral && (
          <div className="p-3 space-y-4">
            
            {/* 1. Reachability */}
            <div className="border-b border-gray-100 pb-3">
              <div className="text-sm font-bold text-gray-500 uppercase mb-2">State Space</div>
              <button
                onClick={() => handleAnalyze('reachability')}
                disabled={loading.reachability}
                className="w-full btn-primary btn-sm flex items-center justify-center gap-2 mb-2"
              >
                {loading.reachability ? (
                  <><FaSpinner className="animate-spin" /> Building...</>
                ) : 'Build Reachability Graph'}
              </button>
              
              {analysisResults.reachability && (
                <div className="bg-gray-50 p-3 rounded border border-gray-200">
                  <div className="flex justify-between items-center mb-2">
                    <div className="text-base">
                      <div className="flex gap-4">
                        <span className="text-gray-600">Nodes: <strong className="text-gray-900">{analysisResults.reachability.states?.length || 0}</strong></span>
                        <span className="text-gray-600">Edges: <strong className="text-gray-900">{analysisResults.reachability.edges?.length || 0}</strong></span>
                      </div>
                    </div>
                    <button onClick={() => openModal('reachabilityGraph')} className="text-blue-600 hover:text-blue-800 btn-sm border border-blue-200 rounded px-2 py-1 bg-white">
                      <FaEye className="inline mr-1"/> View
                    </button>
                  </div>
                  {analysisResults.reachability.truncated && (
                    <div className="text-yellow-600 text-sm flex items-center gap-1 bg-yellow-50 p-2 rounded">
                      <FaExclamationTriangle /> State explosion detected (truncated)
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* 2. Boundedness */}
            <div className="border-b border-gray-100 pb-3">
               <div className="text-sm font-bold text-gray-500 uppercase mb-2">Boundedness</div>
              <button
                onClick={() => handleAnalyze('boundedness')}
                disabled={loading.boundedness}
                className="w-full btn-secondary btn-sm mb-2"
              >
                {loading.boundedness ? <FaSpinner className="animate-spin inline mr-2" /> : null}
                Check Boundedness
              </button>
              
              {analysisResults.boundedness && (
                <div className={`text-base p-3 rounded border ${analysisResults.boundedness.is_bounded ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'}`}>
                  <div className="flex items-center gap-2 mb-2">
                    {analysisResults.boundedness.is_bounded ? <FaCheckCircle className="text-green-600 text-lg"/> : <FaExclamationTriangle className="text-red-600 text-lg"/>}
                    <span className={`font-bold ${analysisResults.boundedness.is_bounded ? 'text-green-800' : 'text-red-800'}`}>
                      {analysisResults.boundedness.is_bounded ? 'Bounded Net' : 'Unbounded Net'}
                    </span>
                  </div>
                  
                  {analysisResults.boundedness.is_bounded ? (
                    <div className="text-sm text-green-700 ml-7">
                      System is <strong>{analysisResults.boundedness.bound}-bounded</strong>
                    </div>
                  ) : (
                    <div className="ml-7">
                      <div className="text-sm text-red-700 mb-1">Unbounded places ():</div>
                      <div className="flex flex-wrap gap-1">
                        {analysisResults.boundedness.unbounded_places?.map(p => (
                          <span key={p} className="text-sm bg-red-100 text-red-800 px-2 py-0.5 rounded border border-red-200">{p}</span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* 3. Deadlock */}
            <div className="border-b border-gray-100 pb-3">
              <div className="text-sm font-bold text-gray-500 uppercase mb-2">Deadlocks</div>
              <button
                onClick={() => handleAnalyze('deadlock')}
                disabled={loading.deadlock}
                className="w-full btn-secondary btn-sm mb-2"
              >
                Find Deadlocks
              </button>
              
              {analysisResults.deadlock && (
                <div className="bg-gray-50 p-3 rounded border border-gray-200">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-base text-gray-600">Total Found:</span>
                    <span className={`font-bold text-base ${analysisResults.deadlock.total_deadlocks > 0 ? 'text-red-600' : 'text-green-600'}`}>
                      {analysisResults.deadlock.total_deadlocks}
                    </span>
                  </div>
                  
                  {analysisResults.deadlock.deadlock_markings?.length > 0 ? (
                    <div className="space-y-2 max-h-48 overflow-y-auto custom-scrollbar">
                      {analysisResults.deadlock.deadlock_markings.map((marking, idx) => (
                        <div key={idx} className="text-sm bg-white border border-gray-200 p-2 rounded shadow-sm">
                          <div className="font-semibold text-gray-500 mb-1 border-b border-gray-100 pb-1 flex justify-between">
                            <span>Deadlock #{idx + 1}</span>
                            <FaBug className="text-red-400"/>
                          </div>
                          <div className="flex flex-wrap gap-x-3 gap-y-1">
                            {Object.entries(marking).map(([place, tokens]) => (
                              <span key={place} className="text-gray-700 font-mono">
                                {place}: <span className={tokens > 0 ? "text-blue-600 font-bold" : "text-gray-400"}>{tokens}</span>
                              </span>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-sm text-green-600 italic flex items-center gap-1">
                      <FaCheckCircle/> No deadlocks found (in analyzed states)
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* 4. Liveness */}
            <div>
              <div className="text-sm font-bold text-gray-500 uppercase mb-2">Liveness</div>
              <button
                onClick={() => handleAnalyze('liveness')}
                disabled={loading.liveness}
                className="w-full btn-secondary btn-sm mb-2"
              >
                {loading.liveness ? <FaSpinner className="animate-spin inline mr-2" /> : null}
                Check Liveness
              </button>
              
                {analysisResults.liveness && (
                    <div className="bg-gray-50 p-4 rounded-lg border border-gray-200 shadow-sm space-y-4">

                      {/* --- Tổng quan Live Net --- */}
                      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 border-b border-gray-200 pb-2">
                        <span className={`font-bold text-lg sm:text-xl ${analysisResults.liveness.is_live ? 'text-green-600' : 'text-orange-600'}`}>
                          {analysisResults.liveness.is_live ? 'Live' : 'Not Live'}
                        </span>
                        {!analysisResults.liveness.is_live && (
                          <span className="text-sm text-gray-500">
                            Liveness Level: <span className="font-bold">{analysisResults.liveness.liveness_level}</span>
                          </span>
                        )}
                      </div>


                      {/* --- Dead / Unreachable Transitions --- */}
                      {analysisResults.liveness.unreachable_transitions?.length > 0 && (
                        <div>
                          <div className="text-sm font-semibold text-gray-600 mb-1">Dead / Unreachable Transitions:</div>
                          <div className="flex flex-wrap gap-2">
                            {analysisResults.liveness.unreachable_transitions.map(t => (
                              <span key={t} className="text-sm bg-red-50 text-red-700 px-3 py-1 rounded-full font-medium">{t}</span>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* --- Legend màu nhẹ --- */}
                      <div className="flex flex-wrap gap-2 text-sm items-center">
                        <span className="px-2 py-1 rounded-full bg-red-100 text-red-700 font-medium">Dead</span>
                        <span className="px-2 py-1 rounded-full bg-orange-100 text-orange-700 font-medium">L1</span>
                        <span className="px-2 py-1 rounded-full bg-yellow-100 text-yellow-800 font-medium">L2</span>
                        <span className="px-2 py-1 rounded-full bg-blue-100 text-blue-700 font-medium">L3</span>
                        <span className="px-2 py-1 rounded-full bg-green-100 text-green-700 font-medium">L4</span>
                      </div>

                      {/* --- Bảng liveness từng transition --- */}
                      {analysisResults.liveness.transition_liveness_levels && (
                        <div className="overflow-x-auto">
                          <table className="table-auto w-full border border-gray-200 rounded-lg overflow-hidden text-sm">
                            <thead className="bg-gray-50">
                              <tr>
                                <th className="px-2 py-1 border-b border-gray-200 text-center">ID</th>
                                <th className="px-2 py-1 border-b border-gray-200 text-center">Label</th>
                                <th className="px-2 py-1 border-b border-gray-200 text-center whitespace-nowrap">Levels of Liveness </th>
                              </tr>
                            </thead>
                            <tbody>
                              {Object.entries(analysisResults.liveness.transition_liveness_levels).sort().map(([id, level]) => {
                                const transition = transitions.find(t => t.id === id);
                                const labelText = transition?.label || id;

                                let label = '';
                                let bgColor = '';
                                let textColor = '';
                                switch(level) {
                                  case 0: label = 'Dead'; bgColor = 'bg-red-400'; textColor = 'text-white'; break;
                                  case 1: label = 'L1'; bgColor = 'bg-orange-200'; textColor = 'text-orange-800'; break;
                                  case 2: label = 'L2'; bgColor = 'bg-yellow-200'; textColor = 'text-yellow-800'; break;
                                  case 3: label = 'L3'; bgColor = 'bg-blue-200'; textColor = 'text-blue-800'; break;
                                  case 4: label = 'L4'; bgColor = 'bg-green-200'; textColor = 'text-green-800'; break;
                                  default: label = level; bgColor = 'bg-gray-200'; textColor = 'text-gray-600';
                                }

                                return (
                                  <tr key={id} className="even:bg-gray-50">
                                    <td className="px-2 py-1 border-b border-gray-200 text-center">{id}</td>
                                    <td className="px-2 py-1 border-b border-gray-200 text-center">{labelText}</td>
                                    <td className="px-2 py-1 border-b border-gray-200 text-center">
                                      <span className={`inline-block px-2 py-0.5 text-xs rounded-full ${bgColor} ${textColor} font-semibold`}>
                                        {label}
                                      </span>
                                    </td>
                                  </tr>
                                );
                              })}
                            </tbody>
                          </table>




                        </div>
                      )}

                    </div>
                  )}


            </div>

          </div>
        )}
      </div>
      
    </div>
  );
};

export default AnalysisTab;


