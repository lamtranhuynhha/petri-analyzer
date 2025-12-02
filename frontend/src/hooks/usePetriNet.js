import { create } from 'zustand';

/**
 * Zustand store cho Petri Net state management
 * Quản lý toàn bộ state của ứng dụng: model, UI, simulation, analysis
 */
const usePetriNetStore = create((set, get) => ({
  // ============ PETRI NET MODEL ============
  places: [],
  transitions: [],
  arcs: [],
  weights: {},
  initialMarking: {},
  
  // ============ UI STATE ============
  selectedTool: 'select', // 'select', 'place', 'transition', 'arc', 'token'
  selectedElement: null, // { type: 'place'|'transition'|'arc', id: string, data: object }
  activeTab: 'properties', // 'properties', 'analysis', 'simulation'
  
  // ============ MODALS ============
  modals: {
    reachabilityGraph: false,
    coverabilityTree: false,
    export: false,
    confirm: false,
  },
  confirmAction: null,
  
  // ============ SIMULATION STATE ============
  currentMarking: {},
  simulationHistory: [],
  isSimulating: false,
  autoPlayInterval: null,
  
  // ============ ANALYSIS RESULTS ============
  analysisResults: {
    reachability: null,
    deadlock: null,
    boundedness: null,
    liveness: null,
    siphonsTraps: null,
  },
  
  // ============ STATUS ============
  status: {
    isBounded: null,
    elementCount: { places: 0, transitions: 0 },
    stateCount: 0,
    hasWarning: false,
    warningMessage: '',
  },
  
  // ============ UNDO/REDO ============
  history: [],
  historyIndex: -1,
  maxHistory: 50,
  
  // ============ LOADING STATE ============
  loading: {
    reachability: false,
    boundedness: false,
    liveness: false,
    siphonsTraps: false,
    upload: false,
  },
  
  // ============ ACTIONS - Model Management ============
  
  addPlace: (place) => set((state) => {
    const newPlaces = [...state.places, place];
    const newMarking = { ...state.initialMarking, [place.id]: place.tokens || 0 };
    get().saveToHistory();
    return {
      places: newPlaces,
      initialMarking: newMarking,
      currentMarking: { ...state.currentMarking, [place.id]: place.tokens || 0 },
      status: { ...state.status, elementCount: { ...state.status.elementCount, places: newPlaces.length } }
    };
  }),
  
  updatePlace: (id, updates) => set((state) => {
    const newPlaces = state.places.map(p => p.id === id ? { ...p, ...updates } : p);
    const newMarking = { ...state.initialMarking };
    if (updates.tokens !== undefined) {
      newMarking[id] = updates.tokens;
    }
    return {
      places: newPlaces,
      initialMarking: newMarking,
      currentMarking: { ...state.currentMarking, [id]: newMarking[id] },
      selectedElement: state.selectedElement?.id === id && state.selectedElement?.type === 'place' 
        ? { ...state.selectedElement, data: { ...state.selectedElement.data, ...updates } } 
        : state.selectedElement
    };
  }),
  
  deletePlace: (id) => set((state) => {
    get().saveToHistory();
    const newPlaces = state.places.filter(p => p.id !== id);
    // Xóa arc liên quan
    const arcsToRemove = state.arcs.filter(a => a.source === id || a.target === id);
    const newArcs = state.arcs.filter(a => a.source !== id && a.target !== id);
    
    // CLEANUP WEIGHTS
    const newWeights = { ...state.weights };
    arcsToRemove.forEach(arc => {
        const key = JSON.stringify([arc.source, arc.target]);
        delete newWeights[key];
    });

    const newMarking = { ...state.initialMarking };
    delete newMarking[id];
    
    // Reset selection nếu đang chọn
    const selectedElement = state.selectedElement?.id === id ? null : state.selectedElement;

    return {
      places: newPlaces,
      arcs: newArcs,
      weights: newWeights, // Update weights
      initialMarking: newMarking,
      currentMarking: { ...state.currentMarking }, // Cẩn thận reset current marking nếu cần
      selectedElement,
      status: { ...state.status, elementCount: { ...state.status.elementCount, places: newPlaces.length } }
    };
  }),
  
  addTransition: (transition) => set((state) => {
    const newTransitions = [...state.transitions, transition];
    get().saveToHistory();
    return {
      transitions: newTransitions,
      status: { ...state.status, elementCount: { ...state.status.elementCount, transitions: newTransitions.length } }
    };
  }),
  
  updateTransition: (id, updates) => set((state) => ({
    transitions: state.transitions.map(t => t.id === id ? { ...t, ...updates } : t),
    selectedElement: state.selectedElement?.id === id && state.selectedElement?.type === 'transition' 
      ? { ...state.selectedElement, data: { ...state.selectedElement.data, ...updates } } 
      : state.selectedElement
  })),
  
  deleteTransition: (id) => set((state) => {
    get().saveToHistory();
    const newTransitions = state.transitions.filter(t => t.id !== id);
    
    const arcsToRemove = state.arcs.filter(a => a.source === id || a.target === id);
    const newArcs = state.arcs.filter(a => a.source !== id && a.target !== id);
    
    // CLEANUP WEIGHTS
    const newWeights = { ...state.weights };
    arcsToRemove.forEach(arc => {
        const key = JSON.stringify([arc.source, arc.target]);
        delete newWeights[key];
    });
    
    const selectedElement = state.selectedElement?.id === id ? null : state.selectedElement;

    return {
      transitions: newTransitions,
      arcs: newArcs,
      weights: newWeights,
      selectedElement,
      status: { ...state.status, elementCount: { ...state.status.elementCount, transitions: newTransitions.length } }
    };
  }),
  
  addArc: (arc) => set((state) => {
    const newArcs = [...state.arcs, arc];
    const weightKey = JSON.stringify([arc.source, arc.target]);
    const newWeights = { ...state.weights, [weightKey]: arc.weight || 1 };
    get().saveToHistory();
    return { arcs: newArcs, weights: newWeights };
  }),
  
  updateArc: (id, updates) => set((state) => {
    const newArcs = state.arcs.map(a => a.id === id ? { ...a, ...updates } : a);
    const updatedArc = newArcs.find(a => a.id === id);
    if (!updatedArc) return { arcs: newArcs };
    
    const result = { arcs: newArcs };
    
    if (updates.weight !== undefined) {
      const weightKey = JSON.stringify([updatedArc.source, updatedArc.target]);
      result.weights = { ...state.weights, [weightKey]: updates.weight };
    }
    
    // Update selectedElement if it's the arc being updated
    if (state.selectedElement?.id === id && state.selectedElement?.type === 'arc') {
      result.selectedElement = {
        ...state.selectedElement,
        data: { ...state.selectedElement.data, ...updates }
      };
    }
    
    return result;
  }),
  
  deleteArc: (id) => set((state) => {
    get().saveToHistory();
    const arc = state.arcs.find(a => a.id === id);
    const newArcs = state.arcs.filter(a => a.id !== id);
    if (arc) {
      const weightKey = JSON.stringify([arc.source, arc.target]);
      const newWeights = { ...state.weights };
      delete newWeights[weightKey];
      return { arcs: newArcs, weights: newWeights };
    }
    return { arcs: newArcs };
  }),
  
  // ============ ACTIONS - UI ============
  
  setSelectedTool: (tool) => set({ selectedTool: tool }),
  
  setSelectedElement: (element) => set({ selectedElement: element }),
  
  setActiveTab: (tab) => set({ activeTab: tab }),
  
  openModal: (modalName) => set((state) => ({
    modals: { ...state.modals, [modalName]: true }
  })),
  
  closeModal: (modalName) => set((state) => ({
    modals: { ...state.modals, [modalName]: false }
  })),
  
  setConfirmAction: (action) => set({ confirmAction: action }),
  
  // ============ ACTIONS - Simulation ============
  
  setCurrentMarking: (marking) => set({ currentMarking: marking }),
  
  resetToInitialMarking: () => set((state) => ({
    currentMarking: { ...state.initialMarking },
    simulationHistory: [],
  })),
  
  fireTransition: (transitionId) => set((state) => {
    const transition = state.transitions.find(t => t.id === transitionId);
    if (!transition) return state;
    
    // Tính toán marking mới
    const newMarking = { ...state.currentMarking };
    const inputArcs = state.arcs.filter(a => a.target === transitionId);
    const outputArcs = state.arcs.filter(a => a.source === transitionId);
    
    // Kiểm tra enabled
    const isEnabled = inputArcs.every(arc => {
      const weightKey = JSON.stringify([arc.source, arc.target]);
      const weight = state.weights[weightKey] || 1;
      return newMarking[arc.source] >= weight;
    });
    
    if (!isEnabled) return state;
    
    // Consume tokens từ input places
    inputArcs.forEach(arc => {
      const weightKey = JSON.stringify([arc.source, arc.target]);
      const weight = state.weights[weightKey] || 1;
      newMarking[arc.source] -= weight;
    });
    
    // Produce tokens vào output places
    outputArcs.forEach(arc => {
      const weightKey = JSON.stringify([arc.source, arc.target]);
      const weight = state.weights[weightKey] || 1;
      newMarking[arc.target] = (newMarking[arc.target] || 0) + weight;
    });
    
    // Thêm vào history
    const historyEntry = {
      marking: state.currentMarking,
      transition: transitionId,
      timestamp: Date.now(),
    };
    
    return {
      currentMarking: newMarking,
      simulationHistory: [...state.simulationHistory, historyEntry],
    };
  }),
  
  getEnabledTransitions: () => {
    const state = get();
    return state.transitions.filter(t => {
      const inputArcs = state.arcs.filter(a => a.target === t.id);
      return inputArcs.every(arc => {
        const weightKey = JSON.stringify([arc.source, arc.target]);
        const weight = state.weights[weightKey] || 1;
        return (state.currentMarking[arc.source] || 0) >= weight;
      });
    });
  },
  
  startAutoPlay: (interval = 1000) => set((state) => {
    if (state.autoPlayInterval) {
      clearInterval(state.autoPlayInterval);
    }
    
    const intervalId = setInterval(() => {
      const enabled = get().getEnabledTransitions();
      if (enabled.length > 0) {
        const randomTransition = enabled[Math.floor(Math.random() * enabled.length)];
        get().fireTransition(randomTransition.id);
      } else {
        get().stopAutoPlay();
      }
    }, interval);
    
    return { isSimulating: true, autoPlayInterval: intervalId };
  }),
  
  stopAutoPlay: () => set((state) => {
    if (state.autoPlayInterval) {
      clearInterval(state.autoPlayInterval);
    }
    return { isSimulating: false, autoPlayInterval: null };
  }),
  
  // ============ ACTIONS - Analysis ============
  
  setAnalysisResult: (analysisType, result) => set((state) => ({
    analysisResults: {
      ...state.analysisResults,
      [analysisType]: result,
    }
  })),
  
  setLoading: (key, value) => set((state) => ({
    loading: { ...state.loading, [key]: value }
  })),
  
  updateStatus: (updates) => set((state) => ({
    status: { ...state.status, ...updates }
  })),
  
  // ============ ACTIONS - History (Undo/Redo) ============
  
  saveToHistory: () => set((state) => {
    const snapshot = {
      places: state.places,
      transitions: state.transitions,
      arcs: state.arcs,
      weights: state.weights,
      initialMarking: state.initialMarking,
    };
    
    const newHistory = state.history.slice(0, state.historyIndex + 1);
    newHistory.push(snapshot);
    
    if (newHistory.length > state.maxHistory) {
      newHistory.shift();
    }
    
    return {
      history: newHistory,
      historyIndex: newHistory.length - 1,
    };
  }),
  
  undo: () => set((state) => {
    if (state.historyIndex <= 0) return state;
    
    const newIndex = state.historyIndex - 1;
    const snapshot = state.history[newIndex];
    
    return {
      ...snapshot,
      historyIndex: newIndex,
      currentMarking: { ...snapshot.initialMarking },
    };
  }),
  
  redo: () => set((state) => {
    if (state.historyIndex >= state.history.length - 1) return state;
    
    const newIndex = state.historyIndex + 1;
    const snapshot = state.history[newIndex];
    
    return {
      ...snapshot,
      historyIndex: newIndex,
      currentMarking: { ...snapshot.initialMarking },
    };
  }),
  
  canUndo: () => {
    const state = get();
    return state.historyIndex > 0;
  },
  
  canRedo: () => {
    const state = get();
    return state.historyIndex < state.history.length - 1;
  },
  
  // ============ ACTIONS - Import/Export ============
  
  loadPetriNet: (data) => set((state) => {
    get().saveToHistory();
    return {
      places: data.places || [],
      transitions: data.transitions || [],
      arcs: data.arcs || [],
      weights: data.weights || {},
      initialMarking: data.initial_marking || data.initialMarking || {},
      currentMarking: data.initial_marking || data.initialMarking || {},
      status: {
        ...state.status,
        elementCount: {
          places: (data.places || []).length,
          transitions: (data.transitions || []).length,
        }
      }
    };
  }),
  
  resetNet: () => set((state) => {
    get().saveToHistory();
    return {
      places: [],
      transitions: [],
      arcs: [],
      weights: {},
      initialMarking: {},
      currentMarking: {},
      selectedElement: null,
      simulationHistory: [],
      analysisResults: {
        reachability: null,
        deadlock: null,
        boundedness: null,
        liveness: null,
        siphonsTraps: null,
      },
      status: {
        isBounded: null,
        elementCount: { places: 0, transitions: 0 },
        stateCount: 0,
        hasWarning: false,
        warningMessage: '',
      },
    };
  }),
  
  // ============ HELPERS ============
  
  getPetriNetData: () => {
    const state = get();
    return {
      places: state.places.map(p => p.id),
      transitions: state.transitions.map(t => t.id),
      arcs: state.arcs.map(a => [a.source, a.target]),
      weights: state.weights,
      initial_marking: state.initialMarking,
    };
  },
//   getPetriNetData: () => {
//   const state = get();
//   return {
//     places: state.places.map(p => ({
//       id: p.id,
//       label: p.label,
//       position: p.position || { x: 0, y: 0 },
//     })),
//     transitions: state.transitions.map(t => ({
//       id: t.id,
//       label: t.label,
//       position: t.position || { x: 0, y: 0 },
//     })),
//     arcs: state.arcs.map(a => ({
//       source: a.source,
//       target: a.target //,
//       // weight: state.weights[JSON.stringify([a.source, a.target])] || 1,
//     })),
//     weights: state.weights,
//     initial_marking: state.initialMarking,
//   };
// }

  
}));

export default usePetriNetStore;


