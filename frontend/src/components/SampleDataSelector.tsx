import React from 'react';
import { Sparkles, Terminal, Code, Cpu } from 'lucide-react';
import { SampleProfile } from '../types';

interface SampleDataSelectorProps {
  samples: {
    resumes: SampleProfile[];
    job_descriptions: SampleProfile[];
  };
  onSelectSample: (resume: SampleProfile, jd: SampleProfile) => void;
  isLoading: boolean;
}

export const SampleDataSelector: React.FC<SampleDataSelectorProps> = ({
  samples,
  onSelectSample,
  isLoading,
}) => {
  if (!samples.resumes.length || !samples.job_descriptions.length) {
    return null;
  }

  // Pre-configured test scenarios
  const scenarios = [
    {
      title: 'Senior AI Backend Engineer',
      badge: 'High Match ~85%',
      icon: Terminal,
      color: 'from-sky-500/10 to-blue-500/10 border-sky-500/30 text-sky-400',
      resumeId: 'senior_python_engineer.txt',
      jdId: 'ai_backend_engineer.txt',
      desc: 'Python, FastAPI, PostgreSQL vs AI Backend JD (Semantic matching test)',
    },
    {
      title: 'Lead Frontend Engineer',
      badge: 'Strong Fit ~82%',
      icon: Code,
      color: 'from-indigo-500/10 to-purple-500/10 border-indigo-500/30 text-indigo-400',
      resumeId: 'frontend_react_dev.txt',
      jdId: 'frontend_lead.txt',
      desc: 'React, TypeScript, Recharts, Tailwind vs Lead Frontend role',
    },
    {
      title: 'ML / Data Scientist',
      badge: 'Targeted ~88%',
      icon: Cpu,
      color: 'from-emerald-500/10 to-teal-500/10 border-emerald-500/30 text-emerald-400',
      resumeId: 'data_scientist.txt',
      jdId: 'ml_engineer.txt',
      desc: 'PyTorch, Sentence Transformers, PhD vs Senior ML Engineer',
    },
  ];

  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-3.5 mb-6">
      <div className="flex items-center justify-between mb-2.5">
        <div className="flex items-center space-x-2">
          <Sparkles className="w-4 h-4 text-amber-400" />
          <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
            Quick Demo Scenarios (1-Click Load)
          </span>
        </div>
        <span className="text-xs text-slate-400">
          Click any preset to test genuine semantic matching instantly
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-2.5">
        {scenarios.map((sc, idx) => {
          const Icon = sc.icon;
          const resume = samples.resumes.find((r) => r.filename === sc.resumeId) || samples.resumes[0];
          const jd = samples.job_descriptions.find((j) => j.filename === sc.jdId) || samples.job_descriptions[0];

          return (
            <button
              key={idx}
              onClick={() => onSelectSample(resume, jd)}
              disabled={isLoading}
              className={`text-left p-3 rounded-lg border transition-all duration-200 bg-slate-950/60 hover:bg-slate-800/80 ${sc.color} flex flex-col justify-between`}
            >
              <div className="flex items-start justify-between w-full mb-1">
                <div className="flex items-center space-x-2">
                  <Icon className="w-4 h-4" />
                  <span className="text-sm font-semibold text-white">{sc.title}</span>
                </div>
                <span className="text-[10px] font-medium px-2 py-0.5 rounded-full bg-slate-800/90 border border-slate-700 text-slate-300">
                  {sc.badge}
                </span>
              </div>
              <p className="text-xs text-slate-400 line-clamp-2 mt-1">{sc.desc}</p>
            </button>
          );
        })}
      </div>
    </div>
  );
};
