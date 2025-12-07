import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://127.0.0.1:8000/api';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response.data;
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message);
    
    // Format error message
    const errorMessage = error.response?.data?.message || 
                        error.response?.data?.detail || 
                        error.message || 
                        'Unknown error occurred';
    
    return Promise.reject(new Error(errorMessage));
  }
);

// ============ FILE OPERATIONS ============

/**
 * Upload PNML or JSON file
 * file - File object to upload
 * returns Parsed Petri Net data
 */
export const uploadPetriNet = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  return await apiClient.post('/net/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

/**
 * Convert between PNML and JSON formats
 * string inputFormat - 'pnml' or 'json'
 * string outputFormat - 'pnml' or 'json'
 * string data - Data to convert
 * returns Converted data
 */
export const convertFormat = async (inputFormat, outputFormat, data) => {
  return await apiClient.post('/net/convert', {
    input_format: inputFormat,
    output_format: outputFormat,
    data,
  });
};

/**
 * Export Petri Net to specified format
 * object netData - Petri Net data
 * string format - 'pnml', 'json', 'png', 'svg'
 * returns Export result
 */
export const exportPetriNet = async (netData, format) => {
  return await apiClient.post('/net/export', {
    net_data: netData,
    format,
  }, {
    responseType: format === 'pnml' || format === 'png' || format === 'svg' ? 'blob' : 'json',
  });
};

// ============ ANALYSIS OPERATIONS ============

export const analyzeReachability = async (netData) => {
  return await apiClient.post('/analyze/reachability', netData);
};

export const analyzeDeadlock = async (netData) => {
  return await apiClient.post('/analyze/deadlock', netData);
};

export const analyzeBoundedness = async (netData) => {
  return await apiClient.post('/analyze/boundedness', netData);
};

export const analyzeLiveness = async (netData) => {
  return await apiClient.post('/analyze/liveness', netData);
};

export const analyzeSiphonsTraps = async (netData) => {
  return await apiClient.post('/analyze/siphons-traps', netData);
};

// ============ VISUALIZATION ============

/**
 * Get visualization of Reachability Graph
 * Object rgData - RG data (states, edges)
 * string format - 'png' or 'svg'
 * returns Image data
 */
export const getReachabilityGraphImage = async (rgData, format = 'svg') => {
  return await apiClient.post(`/visualize/reachability`, {
    data: rgData,
    format,
  }, {
    responseType: 'blob',
  });
};

/**
 * Get visualization of Coverability Tree
 * Object treeData - Coverability tree data
 * string format - 'png' or 'svg'
 * returns Image data
 */
export const getCoverabilityTreeImage = async (treeData, format = 'svg') => {
  return await apiClient.post(`/visualize/coverability`, {
    tree_data: treeData,
    format,
  }, {
    responseType: 'blob',
  });
};

export const getPetriNetImage = async (netData, format = 'svg') => {
  return await apiClient.post(`/visualize/petri-net`, {
    net_data: netData,
    format,
  }, {
    responseType: 'blob',
  });
};

// ============ SIMULATION ============

/**
 * Get enabled transitions at current marking
 * Object netData - Petri Net data
 * Object marking - Current marking
 * return List of enabled transition IDs
 */
export const getEnabledTransitions = async (netData, marking) => {
  return await apiClient.post('/sim/enabled', {
    net_data: netData,
    marking,
  });
};

/**
 * Fire a transition
 * Object netData - Petri Net data
 * Object marking - Current marking
 * string transitionId - Transition to fire
 * returns New marking after firing
 */
export const fireTransition = async (netData, marking, transitionId) => {
  return await apiClient.post('/sim/fire', {
    net_data: netData,
    marking,
    transition_id: transitionId,
  });
};

// ============ HEALTH CHECK ============
export const healthCheck = async () => {
  return await apiClient.get('/health');
};

export default {
  uploadPetriNet,
  convertFormat,
  exportPetriNet,
  analyzeReachability,
  analyzeDeadlock,
  analyzeBoundedness,
  analyzeLiveness,
  analyzeSiphonsTraps,
  getReachabilityGraphImage,
  getCoverabilityTreeImage,
  getPetriNetImage,
  getEnabledTransitions,
  fireTransition,
  healthCheck,
};


