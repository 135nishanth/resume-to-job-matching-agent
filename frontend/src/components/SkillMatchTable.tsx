import React, { useState } from 'react';
import {
  CheckCircle2,
  Shuffle,
  AlertOctagon,
  HelpCircle,
  Search,
  Filter,
} from 'lucide-react';
import { SkillMatch, MissingSkill } from '../types';

interface SkillMatchTableProps {
  matchedSkills: SkillMatch[];
  missingSkills: MissingSkill[];
  partialMatches: SkillMatch[];
}

export const SkillMatchTable: React.FC<SkillMatchTableProps> = ({
  matchedSkills,
  missingSkills,
  partialMatches,
}) => {
  const [filterTab, setFilterTab] = useState<'ALL' | 'EXACT' | 'SEMANTIC' | 'MISSING_REQ' | 'MISSING_PREF'>('ALL');
  const [searchQuery, setSearchQuery] = useState('');

  const exactMatches = matchedSkills.filter((m) => m.match_type === 'EXACT MATCH');
  const semanticMatches = partialMatches;
  const missingRequired = missingSkills.filter((m) => m.importance === 'CRITICAL');
  const missingPreferred = missingSkills.filter((m) => m.importance === 'NICE_TO_HAVE');

  // Unified items for filtering
  interface DisplayItem {
    id: string;
    skill: string;
    category: string;
    requirementType: 'REQUIRED' | 'PREFERRED';
    matchType: 'EXACT MATCH' | 'SEMANTIC MATCH' | 'MISSING';
    similarity: number;
    evidence: string;
    requirement: string;
    relatedSkills?: string[];
  }

  const allItems: DisplayItem[] = [
    ...matchedSkills.map((m, idx) => ({
      id: `match-${idx}`,
      skill: m.skill,
      category: m.category,
      requirementType: m.requirement_type,
      matchType: m.match_type,
      similarity: m.similarity_score,
      evidence: m.candidate_evidence,
      requirement: m.job_requirement,
    })),
    ...missingSkills.map((ms, idx) => ({
      id: `missing-${idx}`,
      skill: ms.skill,
      category: ms.category,
      requirementType: (ms.importance === 'CRITICAL' ? 'REQUIRED' : 'PREFERRED') as 'REQUIRED' | 'PREFERRED',
      matchType: 'MISSING' as const,
      similarity: 0,
      evidence: ms.reason,
      requirement: `Specified in job description under ${ms.importance === 'CRITICAL' ? 'Required' : 'Preferred'} qualifications.`,
      relatedSkills: ms.related_candidate_skills,
    })),
  ];

  // Apply Tab filter
  let filtered = allItems;
  if (filterTab === 'EXACT') {
    filtered = allItems.filter((i) => i.matchType === 'EXACT MATCH');
  } else if (filterTab === 'SEMANTIC') {
    filtered = allItems.filter((i) => i.matchType === 'SEMANTIC MATCH');
  } else if (filterTab === 'MISSING_REQ') {
    filtered = allItems.filter((i) => i.matchType === 'MISSING' && i.requirementType === 'REQUIRED');
  } else if (filterTab === 'MISSING_PREF') {
    filtered = allItems.filter((i) => i.matchType === 'MISSING' && i.requirementType === 'PREFERRED');
  }

  // Apply search query
  if (searchQuery.trim()) {
    const q = searchQuery.toLowerCase();
    filtered = filtered.filter(
      (i) =>
        i.skill.toLowerCase().includes(q) ||
        i.category.toLowerCase().includes(q) ||
        i.evidence.toLowerCase().includes(q) ||
        i.requirement.toLowerCase().includes(q)
    );
  }

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-lg">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-5">
        <div>
          <h2 className="text-base font-semibold text-white">Skill Match Analysis</h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Transparent comparison of candidate evidence vs job requirements
          </p>
        </div>

        {/* Search bar */}
        <div className="relative w-full sm:w-64">
          <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search skills or keywords..."
            className="w-full pl-8 pr-3 py-1.5 text-xs rounded-lg bg-slate-950/80 border border-slate-700 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-sky-500"
          />
        </div>
      </div>

      {/* Tabs */}
      <div className="flex flex-wrap gap-1.5 mb-4 border-b border-slate-800 pb-3">
        <button
          onClick={() => setFilterTab('ALL')}
          className={`px-3 py-1 rounded-lg text-xs font-medium transition ${
            filterTab === 'ALL'
              ? 'bg-sky-600 text-white shadow-sm'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
          }`}
        >
          All Skills ({allItems.length})
        </button>
        <button
          onClick={() => setFilterTab('EXACT')}
          className={`px-3 py-1 rounded-lg text-xs font-medium flex items-center space-x-1.5 transition ${
            filterTab === 'EXACT'
              ? 'bg-emerald-600 text-white shadow-sm'
              : 'text-slate-400 hover:text-emerald-400 hover:bg-slate-800'
          }`}
        >
          <CheckCircle2 className="w-3.5 h-3.5" />
          <span>Exact Matches ({exactMatches.length})</span>
        </button>
        <button
          onClick={() => setFilterTab('SEMANTIC')}
          className={`px-3 py-1 rounded-lg text-xs font-medium flex items-center space-x-1.5 transition ${
            filterTab === 'SEMANTIC'
              ? 'bg-sky-600 text-white shadow-sm'
              : 'text-slate-400 hover:text-sky-400 hover:bg-slate-800'
          }`}
        >
          <Shuffle className="w-3.5 h-3.5" />
          <span>Semantic Matches ({semanticMatches.length})</span>
        </button>
        <button
          onClick={() => setFilterTab('MISSING_REQ')}
          className={`px-3 py-1 rounded-lg text-xs font-medium flex items-center space-x-1.5 transition ${
            filterTab === 'MISSING_REQ'
              ? 'bg-rose-600 text-white shadow-sm'
              : 'text-slate-400 hover:text-rose-400 hover:bg-slate-800'
          }`}
        >
          <AlertOctagon className="w-3.5 h-3.5" />
          <span>Missing Required ({missingRequired.length})</span>
        </button>
        <button
          onClick={() => setFilterTab('MISSING_PREF')}
          className={`px-3 py-1 rounded-lg text-xs font-medium flex items-center space-x-1.5 transition ${
            filterTab === 'MISSING_PREF'
              ? 'bg-amber-600 text-white shadow-sm'
              : 'text-slate-400 hover:text-amber-400 hover:bg-slate-800'
          }`}
        >
          <HelpCircle className="w-3.5 h-3.5" />
          <span>Missing Preferred ({missingPreferred.length})</span>
        </button>
      </div>

      {/* Cards / Rows */}
      {filtered.length === 0 ? (
        <div className="text-center py-10 text-slate-500 text-xs">
          No skills found matching the current filter.
        </div>
      ) : (
        <div className="space-y-3">
          {filtered.map((item) => {
            const isExact = item.matchType === 'EXACT MATCH';
            const isSemantic = item.matchType === 'SEMANTIC MATCH';
            const isMissing = item.matchType === 'MISSING';

            return (
              <div
                key={item.id}
                className="p-4 rounded-xl border border-slate-800/90 bg-slate-950/50 hover:bg-slate-900/60 transition flex flex-col md:flex-row md:items-start justify-between gap-4"
              >
                {/* Left: Skill name, category & badges */}
                <div className="md:w-1/4">
                  <div className="flex items-center space-x-2">
                    <span className="text-sm font-bold text-white tracking-wide">
                      {item.skill}
                    </span>
                    <span className="text-[10px] font-medium px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
                      {item.category}
                    </span>
                  </div>

                  <div className="flex items-center space-x-2 mt-2">
                    {/* Requirement Type Badge */}
                    <span
                      className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border ${
                        item.requirementType === 'REQUIRED'
                          ? 'bg-purple-950/60 text-purple-300 border-purple-800/50'
                          : 'bg-slate-800/80 text-slate-400 border-slate-700'
                      }`}
                    >
                      {item.requirementType}
                    </span>

                    {/* Match Type Badge */}
                    {isExact && (
                      <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-emerald-950/50 text-emerald-400 border border-emerald-500/30 flex items-center gap-1">
                        <CheckCircle2 className="w-3 h-3" /> Exact Match
                      </span>
                    )}
                    {isSemantic && (
                      <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-sky-950/50 text-sky-400 border border-sky-500/30 flex items-center gap-1">
                        <Shuffle className="w-3 h-3" /> Semantic Match
                      </span>
                    )}
                    {isMissing && (
                      <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-rose-950/50 text-rose-400 border border-rose-500/30 flex items-center gap-1">
                        <AlertOctagon className="w-3 h-3" /> Missing
                      </span>
                    )}
                  </div>

                  {/* Similarity Progress Bar */}
                  {!isMissing && (
                    <div className="mt-2.5">
                      <div className="flex items-center justify-between text-[10px] text-slate-400 mb-1">
                        <span>Similarity</span>
                        <span className="font-mono font-medium text-slate-300">
                          {Math.round(item.similarity * 100)}%
                        </span>
                      </div>
                      <div className="w-full h-1.5 rounded-full bg-slate-800 overflow-hidden">
                        <div
                          className={`h-full rounded-full ${
                            isExact ? 'bg-emerald-500' : 'bg-sky-500'
                          }`}
                          style={{ width: `${Math.round(item.similarity * 100)}%` }}
                        />
                      </div>
                    </div>
                  )}

                  {/* Related skills if missing */}
                  {isMissing && item.relatedSkills && item.relatedSkills.length > 0 && (
                    <div className="mt-2.5">
                      <span className="text-[10px] text-slate-500 block mb-1">Related Candidate Skills:</span>
                      <div className="flex flex-wrap gap-1">
                        {item.relatedSkills.map((rs, rIdx) => (
                          <span
                            key={rIdx}
                            className="text-[10px] px-1.5 py-0.5 rounded bg-sky-950/40 text-sky-300 border border-sky-800/40"
                          >
                            {rs}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {/* Right: Evidence vs Job Requirement comparison */}
                <div className="md:w-3/4 grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                  {/* Candidate Evidence */}
                  <div className="bg-slate-900/90 rounded-lg p-3 border border-slate-800 flex flex-col justify-between">
                    <div>
                      <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider block mb-1">
                        Candidate Evidence
                      </span>
                      <p className="text-slate-200 leading-relaxed italic">
                        "{item.evidence}"
                      </p>
                    </div>
                  </div>

                  {/* Job Requirement */}
                  <div className="bg-slate-900/90 rounded-lg p-3 border border-slate-800 flex flex-col justify-between">
                    <div>
                      <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider block mb-1">
                        Job Requirement
                      </span>
                      <p className="text-slate-300 leading-relaxed">
                        "{item.requirement}"
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
