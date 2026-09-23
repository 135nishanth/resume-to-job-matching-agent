import React from 'react';
import { FileCheck, Sparkles, Check, HelpCircle, Briefcase, Lightbulb } from 'lucide-react';
import { ExplanationReport } from '../types';

interface ExplanationCardProps {
  explanation: ExplanationReport;
  score: number;
}

export const ExplanationCard: React.FC<ExplanationCardProps> = ({ explanation, score }) => {
  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-lg">
      <div className="flex items-center space-x-2 mb-4">
        <Sparkles className="w-5 h-5 text-indigo-400" />
        <h2 className="text-base font-semibold text-white">Explainable AI Reasoning Report</h2>
      </div>

      {/* Overall Summary Banner */}
      <div className="bg-gradient-to-r from-indigo-950/40 via-slate-900/60 to-purple-950/40 border border-indigo-500/20 rounded-xl p-4 mb-5">
        <p className="text-sm text-slate-200 leading-relaxed font-medium">
          {explanation.overall_summary}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Left Column: Strengths & Experience */}
        <div className="space-y-5">
          {/* Key Strengths */}
          <div>
            <h3 className="text-xs font-bold text-emerald-400 uppercase tracking-wider mb-2.5 flex items-center gap-1.5">
              <Check className="w-4 h-4 text-emerald-400" />
              <span>Key Strengths & Evidence</span>
            </h3>
            <div className="space-y-2">
              {explanation.strengths.length === 0 ? (
                <p className="text-xs text-slate-400">No primary strengths detected.</p>
              ) : (
                explanation.strengths.map((str, idx) => (
                  <div
                    key={idx}
                    className="text-xs text-slate-300 bg-slate-950/60 border border-slate-800/80 rounded-lg p-3 leading-relaxed flex items-start space-x-2"
                  >
                    <span className="text-emerald-400 font-bold shrink-0 mt-0.5">•</span>
                    <span>{str}</span>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Experience Evaluation */}
          <div>
            <h3 className="text-xs font-bold text-sky-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
              <Briefcase className="w-4 h-4 text-sky-400" />
              <span>Experience & Seniority Evaluation</span>
            </h3>
            <div className="text-xs text-slate-300 bg-slate-950/60 border border-slate-800/80 rounded-lg p-3 leading-relaxed">
              {explanation.experience_summary}
            </div>
          </div>
        </div>

        {/* Right Column: Missing Qualifications & Recommendations */}
        <div className="space-y-5">
          {/* Missing Qualifications Summary */}
          <div>
            <h3 className="text-xs font-bold text-rose-400 uppercase tracking-wider mb-2.5 flex items-center gap-1.5">
              <HelpCircle className="w-4 h-4 text-rose-400" />
              <span>Detected Qualification Gaps</span>
            </h3>
            <div className="bg-slate-950/60 border border-slate-800/80 rounded-lg p-3 text-xs space-y-2">
              <div>
                <span className="text-[11px] font-semibold text-rose-300 block mb-1">
                  Missing Required Skills:
                </span>
                {explanation.critical_missing.length === 0 ? (
                  <span className="text-emerald-400 text-[11px]">None (All required skills present)</span>
                ) : (
                  <div className="flex flex-wrap gap-1">
                    {explanation.critical_missing.map((sk, idx) => (
                      <span
                        key={idx}
                        className="px-2 py-0.5 rounded bg-rose-950/60 text-rose-300 border border-rose-800/50 text-[10px]"
                      >
                        {sk}
                      </span>
                    ))}
                  </div>
                )}
              </div>

              <div className="pt-2 border-t border-slate-800">
                <span className="text-[11px] font-semibold text-amber-300 block mb-1">
                  Missing Preferred Skills:
                </span>
                {explanation.nice_to_have_missing.length === 0 ? (
                  <span className="text-slate-400 text-[11px]">None</span>
                ) : (
                  <div className="flex flex-wrap gap-1">
                    {explanation.nice_to_have_missing.map((sk, idx) => (
                      <span
                        key={idx}
                        className="px-2 py-0.5 rounded bg-amber-950/60 text-amber-300 border border-amber-800/50 text-[10px]"
                      >
                        {sk}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Actionable Recommendations */}
          <div>
            <h3 className="text-xs font-bold text-indigo-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
              <Lightbulb className="w-4 h-4 text-indigo-400" />
              <span>Recruiter Next Steps & Interview Focus</span>
            </h3>
            <div className="space-y-2">
              {explanation.recommendations.map((rec, idx) => (
                <div
                  key={idx}
                  className="text-xs text-slate-300 bg-slate-950/60 border border-indigo-900/30 rounded-lg p-3 leading-relaxed flex items-start space-x-2"
                >
                  <span className="text-indigo-400 font-bold shrink-0 mt-0.5">→</span>
                  <span>{rec}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
