import { AnalysisResponse, HistorySummary, SampleProfile } from '../types';

const API_BASE_URL = 'http://localhost:8000/api';

export async function checkBackendHealth() {
  try {
    const res = await fetch(`${API_BASE_URL}/health`);
    if (!res.ok) throw new Error('Health check failed');
    return await res.json();
  } catch (err) {
    return { status: 'offline', model_loaded: false };
  }
}

export async function fetchSamples(): Promise<{
  resumes: SampleProfile[];
  job_descriptions: SampleProfile[];
}> {
  const res = await fetch(`${API_BASE_URL}/samples`);
  if (!res.ok) {
    throw new Error('Failed to load sample data');
  }
  return await res.json();
}

export async function fetchHistory(): Promise<HistorySummary[]> {
  const res = await fetch(`${API_BASE_URL}/history`);
  if (!res.ok) {
    throw new Error('Failed to load history');
  }
  return await res.json();
}

export async function fetchHistoryDetail(id: number): Promise<AnalysisResponse> {
  const res = await fetch(`${API_BASE_URL}/history/${id}`);
  if (!res.ok) {
    throw new Error('Failed to load history details');
  }
  return await res.json();
}

export async function analyzeMatch(
  resumeFile: File,
  jobDescriptionText?: string,
  jobDescriptionFile?: File
): Promise<AnalysisResponse> {
  const formData = new FormData();
  formData.append('resume', resumeFile);

  if (jobDescriptionText && jobDescriptionText.trim()) {
    formData.append('job_description_text', jobDescriptionText.trim());
  } else if (jobDescriptionFile) {
    formData.append('job_description_file', jobDescriptionFile);
  } else {
    throw new Error('Please provide a job description.');
  }

  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    let errorMsg = 'Failed to analyze documents.';
    try {
      const errorData = await response.json();
      if (errorData.detail) {
        errorMsg = typeof errorData.detail === 'string' ? errorData.detail : JSON.stringify(errorData.detail);
      }
    } catch {
      // fallback
    }
    throw new Error(errorMsg);
  }

  return await response.json();
}
