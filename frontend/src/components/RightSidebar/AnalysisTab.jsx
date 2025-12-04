import React from 'react';
import { FaSpinner, FaEye, FaExclamationTriangle } from 'react-icons/fa';
import usePetriNetStore from '../../hooks/usePetriNet';

/**
 * Analysis Tab - Chứa các buttons phân tích và hiển thị kết quả
 */
const AnalysisTab = ({ onAnalyze }) => {
  const {
    loading,
    analysisResults,
    openModal,
    places,
    transitions,
  } = usePetriNetStore();
  
  const hasNet = places.length > 0 || transitions.length > 0;
  
  const handleAnalyze = (type) => {
    if (!hasNet) {
      alert('Vui lòng vẽ Petri Net trước khi phân tích!');
      return;
    }
    onAnalyze(type);
  };
  
  return (
    <div className="p-4 space-y-4 overflow-y-auto h-full">
      
      {/* REACHABILITY SECTION */}
      <div className="card p-3">
        <div className="font-semibold text-gray-800 mb-2">REACHABILITY</div>
        
        <div className="space-y-2">
          <button
            onClick={() => handleAnalyze('reachability')}
            disabled={loading.reachability}
            className="w-full btn-primary btn-sm flex items-center justify-center gap-2"
          >
            {loading.reachability ? (
              <>
                <FaSpinner className="animate-spin" />
                Building...
              </>
            ) : (
              'Build RG'
            )}
          </button>
          
          {analysisResults.reachability && (
            <>
              <button
                onClick={() => openModal('reachabilityGraph')}
                className="w-full btn-secondary btn-sm flex items-center justify-center gap-2"
              >
                <FaEye />
                Show RG
              </button>
              
              <div className="text-sm bg-gray-50 p-2 rounded">
                <div className="flex justify-between mb-1">
                  {/* <span className="text-gray-600">States:</span>
                  <span className="font-semibold">{analysisResults.reachability.total_states || 0}</span> */}
                </div>
                {analysisResults.reachability.truncated && (
                  <div className="text-yellow-600 text-xs mt-1 flex items-center gap-1">
                    <FaExclamationTriangle />
                    Large space (truncated)
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      </div>
      
      {/* PROPERTIES SECTION */}
      <div className="card p-3">
        <div className="font-semibold text-gray-800 mb-2">PROPERTIES</div>
        
        <div className="space-y-2">
          {/* Boundedness */}
          <button
            onClick={() => handleAnalyze('boundedness')}
            disabled={loading.boundedness}
            className="w-full btn-secondary btn-sm"
          >
            {loading.boundedness ? (
              <FaSpinner className="animate-spin inline mr-2" />
            ) : null}
            Check Boundedness
          </button>
          
          {analysisResults.boundedness && (
            <div className="text-sm bg-gray-50 p-2 rounded space-y-1">
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Status:</span>
                <span className={`font-semibold ${
                  analysisResults.boundedness.is_bounded 
                    ? 'text-green-600' 
                    : 'text-red-600'
                }`}>
                  {analysisResults.boundedness.is_bounded ? 'Bounded' : 'Unbounded'}
                </span>
              </div>
              
              {analysisResults.boundedness.is_bounded && (
                <div className="text-xs text-gray-600">
                  Max tokens: k ≤ {analysisResults.boundedness.k_value || '?'}
                </div>
              )}
              
              {analysisResults.boundedness.place_bounds && (
                <div className="mt-2">
                  <div className="text-xs text-gray-500 mb-1">Per place:</div>
                  {Object.entries(analysisResults.boundedness.place_bounds).map(([place, bound]) => (
                    <div key={place} className="text-xs text-gray-700">
                      • {place}: {bound === Infinity ? '∞' : bound}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
          
          {/* Deadlock */}
          <button
            onClick={() => handleAnalyze('deadlock')}
            disabled={loading.reachability}
            className="w-full btn-secondary btn-sm"
          >
            Find Deadlocks
          </button>
          
          {analysisResults.deadlock && (
            <div className="text-sm bg-gray-50 p-2 rounded">
              <div className="flex items-center justify-between mb-1">
                <span className="text-gray-600">Found:</span>
                <span className="font-semibold text-red-600">
                  {analysisResults.deadlock.total_deadlocks} deadlocks
                </span>
              </div>
              
              {analysisResults.deadlock.deadlock_markings && 
               analysisResults.deadlock.deadlock_markings.length > 0 && (
                <div className="mt-2 space-y-1 max-h-32 overflow-y-auto">
                  {analysisResults.deadlock.deadlock_markings.slice(0, 5).map((marking, idx) => (
                    <div key={idx} className="text-xs flex items-center justify-between">
                      <span className="text-gray-700">
                        M{idx}: ({Object.values(marking).join(',')})
                      </span>
                      <button className="text-blue-500 hover:text-blue-700">
                        <FaEye />
                      </button>
                    </div>
                  ))}
                  {analysisResults.deadlock.deadlock_markings.length > 5 && (
                    <div className="text-xs text-gray-500 italic">
                      +{analysisResults.deadlock.deadlock_markings.length - 5} more...
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
      
      {/* STRUCTURE SECTION */}
      <div className="card p-3">
        <div className="font-semibold text-gray-800 mb-2">STRUCTURE</div>
        
        <button
          onClick={() => handleAnalyze('siphonsTraps')}
          disabled={loading.siphonsTraps}
          className="w-full btn-secondary btn-sm"
        >
          {loading.siphonsTraps ? (
            <FaSpinner className="animate-spin inline mr-2" />
          ) : null}
          Compute S&T
        </button>
        
        {analysisResults.siphonsTraps && (
          <div className="mt-2 space-y-2">
            {/* Siphons */}
            <div className="text-sm bg-gray-50 p-2 rounded">
              <div className="text-xs font-medium text-gray-700 mb-1">
                Minimal Siphons: {analysisResults.siphonsTraps.minimal_siphons?.length || 0}
              </div>
              {analysisResults.siphonsTraps.minimal_siphons?.map((siphon, idx) => (
                <div key={idx} className="text-xs text-gray-600 flex items-center justify-between">
                  <span>• {'{' + siphon.join(', ') + '}'}</span>
                  <button className="text-blue-500 hover:text-blue-700 text-lg">
                    🎯
                  </button>
                </div>
              ))}
            </div>
            
            {/* Traps */}
            <div className="text-sm bg-gray-50 p-2 rounded">
              <div className="text-xs font-medium text-gray-700 mb-1">
                Minimal Traps: {analysisResults.siphonsTraps.minimal_traps?.length || 0}
              </div>
              {analysisResults.siphonsTraps.minimal_traps?.map((trap, idx) => (
                <div key={idx} className="text-xs text-gray-600 flex items-center justify-between">
                  <span>• {'{' + trap.join(', ') + '}'}</span>
                  <button className="text-blue-500 hover:text-blue-700 text-lg">
                    🎯
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
      
      {/* LIVENESS SECTION */}
      <div className="card p-3">
        <div className="font-semibold text-gray-800 mb-2">LIVENESS</div>
        
        <button
          onClick={() => handleAnalyze('liveness')}
          disabled={loading.liveness}
          className="w-full btn-secondary btn-sm"
        >
          {loading.liveness ? (
            <FaSpinner className="animate-spin inline mr-2" />
          ) : null}
          Check Liveness
        </button>
        
        {!analysisResults.boundedness?.is_bounded && (
          <div className="text-xs text-yellow-600 mt-2 flex items-center gap-1">
            <FaExclamationTriangle />
            Requires bounded net
          </div>
        )}
        
        {analysisResults.liveness && (
          <div className="mt-2 text-sm bg-gray-50 p-2 rounded space-y-1">
            <div className="text-xs font-medium text-gray-700 mb-1">Results:</div>
            {Object.entries(analysisResults.liveness.details || {}).map(([trans, level]) => {
              const colors = {
                'Dead': 'text-gray-500',
                'L1': 'text-blue-400',
                'L3': 'text-orange-500',
                'Live': 'text-green-600',
                'L4': 'text-green-600',
              };
              const color = colors[level] || 'text-gray-600';
              
              return (
                <div key={trans} className="text-xs flex items-center justify-between">
                  <span className="text-gray-700">{trans}:</span>
                  <span className={`font-semibold ${color}`}>{level}</span>
                </div>
              );
            })}
          </div>
        )}
      </div>
      
    </div>
  );
};

export default AnalysisTab;


