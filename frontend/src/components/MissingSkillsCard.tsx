import React from 'react';
import { AlertTriangle, AlertOctagon, HelpCircle, ArrowRight } from 'lucide-react';
import { MissingSkill } from '../types';

interface MissingSkillsCardProps {
  missingSkills: MissingSkill[];
}

export const MissingSkillsCard: React.FC<MissingSkillsCardProps> = ({ missingSkills }) => {
  const critical = missingSkills.filter((m) => m.importance === 'CRITICAL');
  const niceToHave = missingSkills.filter((m) => m.importance === 'NICE_TO_HAVE');

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-lg">
      <div className="flex items-center space-x-2 mb-4">
        <AlertTriangle className="w-4 h-4 text-amber-400" />
        <h2 className="text-base font-semibold text-white">Missing Skill Detection</h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Critical Missing Skills (Required) */}
        <div className="bg-rose-950/20 border border-rose-500/20 rounded-xl p-4 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-2">
                <AlertOctagon className="w-4 h-4 text-rose-400" />
                <h3 className="text-xs font-bold text-rose-400 uppercase tracking-wider">
                  Critical Missing Skills ({critical.length})
                </h3>
              </div>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-rose-900/60 text-rose-300 font-semibold">
                High Impact
              </span>
            </div>

            {critical.length === 0 ? (
              <p className="text-xs text-emerald-400 bg-emerald-950/40 border border-emerald-500/20 rounded-lg p-3">
                ✓ Outstanding: Candidate satisfies all core required technical qualifications!
              </p>
            ) : (
              <div className="space-y-2.5">
                {critical.map((item, idx) => (
                  <div
                    key={idx}
                    className="bg-slate-900/90 border border-slate-800 rounded-lg p-3 text-xs"
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-bold text-white tracking-wide">{item.skill}</span>
                      <span className="text-[10px] text-slate-400">{item.category}</span>
                    </div>
                    <p className="text-slate-400 text-[11px] leading-relaxed mb-2">
                      {item.reason}
                    </p>
                    {item.related_candidate_skills && item.related_candidate_skills.length > 0 && (
                      <div className="flex items-center space-x-1.5 pt-2 border-t border-slate-800">
                        <span className="text-[10px] text-sky-400 font-medium">Candidate has related:</span>
                        <div className="flex flex-wrap gap-1">
                          {item.related_candidate_skills.map((rel, rIdx) => (
                            <span
                              key={rIdx}
                              className="text-[10px] px-1.5 py-0.5 rounded bg-sky-950/60 text-sky-300 border border-sky-800/50"
                            >
                              {rel}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Nice-to-Have Missing Skills (Preferred) */}
        <div className="bg-amber-950/20 border border-amber-500/20 rounded-xl p-4 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-2">
                <HelpCircle className="w-4 h-4 text-amber-400" />
                <h3 className="text-xs font-bold text-amber-400 uppercase tracking-wider">
                  Nice-to-Have Missing Skills ({niceToHave.length})
                </h3>
              </div>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-amber-900/60 text-amber-300 font-semibold">
                Low Impact
              </span>
            </div>

            {niceToHave.length === 0 ? (
              <p className="text-xs text-slate-400 bg-slate-900/60 rounded-lg p-3">
                No preferred skills missing from candidate background.
              </p>
            ) : (
              <div className="space-y-2.5">
                {niceToHave.map((item, idx) => (
                  <div
                    key={idx}
                    className="bg-slate-900/90 border border-slate-800 rounded-lg p-3 text-xs"
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-bold text-white tracking-wide">{item.skill}</span>
                      <span className="text-[10px] text-slate-400">{item.category}</span>
                    </div>
                    <p className="text-slate-400 text-[11px] leading-relaxed">
                      {item.reason}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
