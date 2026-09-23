export interface CandidateInfo {
  name: string;
  email?: string;
  phone?: string;
  location?: string;
  education: string[];
  work_experience: Array<{ description: string }>;
  estimated_years_experience: number;
  technical_skills: string[];
  soft_skills: string[];
  certifications: string[];
  projects: string[];
  programming_languages: string[];
  frameworks: string[];
  databases: string[];
  cloud_technologies: string[];
  tools: string[];
}

export interface JobInfo {
  title: string;
  company?: string;
  location?: string;
  required_skills: string[];
  preferred_skills: string[];
  required_experience_years: number;
  preferred_experience_years: number;
  education_requirements: string[];
  responsibilities: string[];
  technologies: string[];
  certifications: string[];
}

export interface SkillMatch {
  skill: string;
  canonical_skill: string;
  category: string;
  requirement_type: 'REQUIRED' | 'PREFERRED';
  match_type: 'EXACT MATCH' | 'SEMANTIC MATCH' | 'MISSING';
  similarity_score: number;
  candidate_evidence: string;
  job_requirement: string;
}

export interface MissingSkill {
  skill: string;
  canonical_skill: string;
  category: string;
  importance: 'CRITICAL' | 'NICE_TO_HAVE';
  reason: string;
  related_candidate_skills: string[];
}

export interface ScoreBreakdownItem {
  category: string;
  weight_percentage: number;
  earned_score: number;
  max_score: number;
  commentary: string;
}

export interface ScoreBreakdown {
  required_skills: ScoreBreakdownItem;
  preferred_skills: ScoreBreakdownItem;
  experience: ScoreBreakdownItem;
  education_certs: ScoreBreakdownItem;
  projects: ScoreBreakdownItem;
}

export interface ExplanationReport {
  overall_summary: string;
  strengths: string[];
  critical_missing: string[];
  nice_to_have_missing: string[];
  experience_summary: string;
  recommendations: string[];
}

export interface AnalysisResponse {
  id?: number;
  created_at: string;
  overall_score: number;
  rating_label: string;
  candidate_info: CandidateInfo;
  job_info: JobInfo;
  matched_skills: SkillMatch[];
  missing_skills: MissingSkill[];
  partial_matches: SkillMatch[];
  total_matched_count: number;
  total_missing_count: number;
  total_partial_count: number;
  score_breakdown: ScoreBreakdown;
  explanation: ExplanationReport;
}

export interface HistorySummary {
  id: number;
  created_at: string;
  candidate_name: string;
  job_title: string;
  overall_score: number;
  rating_label: string;
  total_matched: number;
  total_missing: number;
}

export interface SampleProfile {
  id: string;
  title: string;
  filename: string;
  content: string;
}
