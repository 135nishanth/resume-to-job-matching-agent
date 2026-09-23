import React, { useState, useEffect } from 'react';
import {
  Sparkles,
  ArrowRight,
  Loader2,
  AlertCircle,
  FileCheck2,
  RefreshCw,
} from 'lucide-react';
import { Header } from './components/Header';
import { SampleDataSelector } from './components/SampleDataSelector';
import { FileUpload } from './components/FileUpload';
import { JobDescriptionInput } from './components/JobDescriptionInput';
import { ScoreGauge } from './components/ScoreGauge';
import { StatCards } from './components/StatCards';
import { ScoreBreakdownChart } from './components/ScoreBreakdownChart';
import { SkillMatchTable } from './components/SkillMatchTable';
import { MissingSkillsCard } from './components/MissingSkillsCard';
import { ExplanationCard } from './components/ExplanationCard';
import { HistoryDrawer } from './components/HistoryDrawer';

import { checkBackendHealth, fetchSamples, analyzeMatch } from './services/api';
import { AnalysisResponse, SampleProfile } from './types';

export function App() {
  const [isBackendHealthy, setIsBackendHealthy] = useState(false);
  const [samples, setSamples] = useState<{
    resumes: SampleProfile[];
    job_descriptions: SampleProfile[];
  }>({ resumes: [], job_descriptions: [] });

  const [selectedResumeFile, setSelectedResumeFile] = useState<File | null>(null);
  const [jobText, setJobText] = useState<string>('');
  const [selectedJdFile, setSelectedJdFile] = useState<File | null>(null);

  const [isLoading, setIsLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState<string>('');
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResponse | null>(null);
  const [isHistoryOpen, setIsHistoryOpen] = useState(false);

  // Initial check & sample loader
  useEffect(() => {
    checkHealth();
    loadSampleData();
  }, []);

  const checkHealth = async () => {
    const health = await checkBackendHealth();
    setIsBackendHealthy(health.status === 'healthy');
  };

  const loadSampleData = async () => {
    try {
      const data = await fetchSamples();
      setSamples(data);
    } catch (err) {
      console.warn('Could not load samples:', err);
    }
  };

  const handleSelectSample = (resumeSample: SampleProfile, jdSample: SampleProfile) => {
    // Create a virtual File object for the resume sample
    const blob = new Blob([resumeSample.content], { type: 'text/plain' });
    const file = new File([blob], resumeSample.filename, { type: 'text/plain' });
    setSelectedResumeFile(file);
    setJobText(jdSample.content);
    setSelectedJdFile(null);
    setErrorMsg(null);
  };

  const handleAnalyze = async () => {
    if (!selectedResumeFile) {
      setErrorMsg('Please upload a candidate resume file (PDF, DOCX, or TXT).');
      return;
    }
    if (!jobText.trim() && !selectedJdFile) {
      setErrorMsg('Please paste a job description or upload a JD file.');
      return;
    }

    setIsLoading(true);
    setErrorMsg(null);
    setLoadingStep('Parsing resume and job documents...');

    try {
      // Step messages for smooth UI experience
      const stepTimer1 = setTimeout(() => {
        setLoadingStep('Extracting structured candidate & job entities...');
      }, 700);

      const stepTimer2 = setTimeout(() => {
        setLoadingStep('Running Sentence Transformers embeddings & semantic matching...');
      }, 1600);

      const result = await analyzeMatch(selectedResumeFile, jobText, selectedJdFile || undefined);

      clearTimeout(stepTimer1);
      clearTimeout(stepTimer2);
      setAnalysisResult(result);

      // Scroll smoothly to results
      setTimeout(() => {
        const el = document.getElementById('results-section');
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      }, 200);
    } catch (err: any) {
      setErrorMsg(err.message || 'An error occurred during analysis.');
    } finally {
      setIsLoading(false);
      setLoadingStep('');
    }
  };

  return (
    <div className="min-h-screen bg-[#0b0f19] text-slate-100 flex flex-col font-sans selection:bg-sky-500/30">
      {/* Header */}
      <Header
        isBackendHealthy={isBackendHealthy}
        onOpenHistory={() => setIsHistoryOpen(true)}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Sample preset selector */}
        <SampleDataSelector
          samples={samples}
          onSelectSample={handleSelectSample}
          isLoading={isLoading}
        />

        {/* Input Section (Upload Resume + Job Description) */}
        <section className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 shadow-xl relative backdrop-blur-md">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Left: Resume Upload */}
            <div className="bg-slate-950/40 p-4 rounded-xl border border-slate-800/80">
              <FileUpload
                selectedFile={selectedResumeFile}
                onFileSelect={setSelectedResumeFile}
                isLoading={isLoading}
              />
            </div>

            {/* Right: Job Description */}
            <div className="bg-slate-950/40 p-4 rounded-xl border border-slate-800/80">
              <JobDescriptionInput
                jobText={jobText}
                onJobTextChange={setJobText}
                selectedJdFile={selectedJdFile}
                onJdFileSelect={setSelectedJdFile}
                isLoading={isLoading}
              />
            </div>
          </div>

          {/* Error Message */}
          {errorMsg && (
            <div className="mt-4 p-3.5 rounded-xl bg-rose-950/40 border border-rose-500/30 text-rose-300 text-xs flex items-center space-x-2">
              <AlertCircle className="w-4 h-4 shrink-0 text-rose-400" />
              <span>{errorMsg}</span>
            </div>
          )}

          {/* Action Button */}
          <div className="mt-6 flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-slate-800">
            <div className="text-xs text-slate-400 flex items-center space-x-2">
              <Sparkles className="w-4 h-4 text-sky-400" />
              <span>
                Semantic embeddings powered by Sentence Transformers. No keyword-only shortcuts.
              </span>
            </div>

            <button
              onClick={handleAnalyze}
              disabled={isLoading || !selectedResumeFile || (!jobText.trim() && !selectedJdFile)}
              className={`w-full sm:w-auto px-7 py-3 rounded-xl font-bold text-sm tracking-wide flex items-center justify-center space-x-2 transition-all duration-200 shadow-lg ${
                isLoading || !selectedResumeFile || (!jobText.trim() && !selectedJdFile)
                  ? 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700/50'
                  : 'bg-gradient-to-r from-sky-500 via-indigo-600 to-purple-600 hover:from-sky-400 hover:to-purple-500 text-white shadow-sky-500/20 hover:scale-[1.02]'
              }`}
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>{loadingStep || 'Analyzing Semantic Fit...'}</span>
                </>
              ) : (
                <>
                  <span>Analyze Match</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </div>
        </section>

        {/* Results Section */}
        {analysisResult && (
          <section id="results-section" className="space-y-6 animate-in fade-in duration-500">
            {/* Top row: Score Gauge + Stat Cards + Candidate/Job Meta */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              {/* Score Gauge (Visual focal point) */}
              <div className="lg:col-span-4">
                <ScoreGauge
                  score={analysisResult.overall_score}
                  ratingLabel={analysisResult.rating_label}
                />
              </div>

              {/* Stats & Overview */}
              <div className="lg:col-span-8 flex flex-col justify-between space-y-4">
                {/* Candidate & Role banner */}
                <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/60 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div>
                    <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-widest block">
                      Target Role & Candidate
                    </span>
                    <h2 className="text-base font-bold text-white mt-0.5">
                      {analysisResult.candidate_info.name} → {analysisResult.job_info.title}
                    </h2>
                    <p className="text-xs text-slate-400 mt-0.5">
                      {analysisResult.candidate_info.email || 'Email not listed'} | {analysisResult.candidate_info.location || 'Location flexible'}
                    </p>
                  </div>
                  <div className="text-right">
                    <span className="text-[10px] text-slate-500 block">Analysis ID</span>
                    <span className="text-xs font-mono text-slate-300">
                      #{analysisResult.id || 'LIVE-RUN'}
                    </span>
                  </div>
                </div>

                {/* 4 Stat Cards */}
                <StatCards analysis={analysisResult} />
              </div>
            </div>

            {/* Score Breakdown Chart */}
            <ScoreBreakdownChart breakdown={analysisResult.score_breakdown} />

            {/* Skill Match Analysis (Table with tabs and citations) */}
            <SkillMatchTable
              matchedSkills={analysisResult.matched_skills}
              missingSkills={analysisResult.missing_skills}
              partialMatches={analysisResult.partial_matches}
            />

            {/* Missing Skills Section */}
            <MissingSkillsCard missingSkills={analysisResult.missing_skills} />

            {/* Grounded AI Explanations */}
            <ExplanationCard
              explanation={analysisResult.explanation}
              score={analysisResult.overall_score}
            />
          </section>
        )}
      </main>

      {/* History Drawer */}
      <HistoryDrawer
        isOpen={isHistoryOpen}
        onClose={() => setIsHistoryOpen(false)}
        onSelectRecord={(rec) => {
          setAnalysisResult(rec);
          setTimeout(() => {
            const el = document.getElementById('results-section');
            if (el) el.scrollIntoView({ behavior: 'smooth' });
          }, 200);
        }}
      />

      {/* Footer */}
      <footer className="border-t border-slate-800/80 bg-slate-950 py-5 text-center text-xs text-slate-500">
        <p>Intelligent Resume-to-Job Matching Agent • Built for the Codeathon</p>
      </footer>
    </div>
  );
}

export default App;
