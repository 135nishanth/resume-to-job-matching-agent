import React from 'react';
import { CheckCircle2, XCircle, Shuffle, Briefcase, GraduationCap } from 'lucide-react';
import { AnalysisResponse } from '../types';

interface StatCardsProps {
  analysis: AnalysisResponse;
}

export const StatCards: React.FC<StatCardsProps> = ({ analysis }) => {
  const cards = [
    {
      label: 'Matched Skills',
      value: analysis.total_matched_count,
      sub: `${analysis.matched_skills.filter((m) => m.match_type === 'EXACT MATCH').length} exact matches`,
      icon: CheckCircle2,
      color: 'text-emerald-400',
      bg: 'bg-emerald-950/20 border-emerald-500/20',
      iconBg: 'bg-emerald-500/10 text-emerald-400',
    },
    {
      label: 'Missing Skills',
      value: analysis.total_missing_count,
      sub: `${analysis.missing_skills.filter((m) => m.importance === 'CRITICAL').length} critical required`,
      icon: XCircle,
      color: 'text-rose-400',
      bg: 'bg-rose-950/20 border-rose-500/20',
      iconBg: 'bg-rose-500/10 text-rose-400',
    },
    {
      label: 'Semantic / Partial',
      value: analysis.total_partial_count,
      sub: 'Related domain skills',
      icon: Shuffle,
      color: 'text-sky-400',
      bg: 'bg-sky-950/20 border-sky-500/20',
      iconBg: 'bg-sky-500/10 text-sky-400',
    },
    {
      label: 'Experience Fit',
      value: `${analysis.candidate_info.estimated_years_experience.toFixed(1)}y`,
      sub: `Target: ${analysis.job_info.required_experience_years.toFixed(1)}y req.`,
      icon: Briefcase,
      color: 'text-indigo-400',
      bg: 'bg-indigo-950/20 border-indigo-500/20',
      iconBg: 'bg-indigo-500/10 text-indigo-400',
    },
  ];

  return (
    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3.5">
      {cards.map((card, idx) => {
        const Icon = card.icon;
        return (
          <div
            key={idx}
            className={`p-4 rounded-xl border ${card.bg} flex flex-col justify-between transition hover:scale-[1.01]`}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-medium text-slate-400">{card.label}</span>
              <div className={`p-1.5 rounded-lg ${card.iconBg}`}>
                <Icon className="w-4 h-4" />
              </div>
            </div>
            <div>
              <div className={`text-2xl font-bold tracking-tight ${card.color}`}>
                {card.value}
              </div>
              <div className="text-[11px] text-slate-400 mt-1 truncate">{card.sub}</div>
            </div>
          </div>
        );
      })}
    </div>
  );
};
