import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';
import { BarChart3, Info } from 'lucide-react';
import { ScoreBreakdown } from '../types';

interface ScoreBreakdownChartProps {
  breakdown: ScoreBreakdown;
}

export const ScoreBreakdownChart: React.FC<ScoreBreakdownChartProps> = ({ breakdown }) => {
  const chartData = [
    {
      name: 'Required Skills',
      shortName: 'Required',
      weight: '50%',
      earned: breakdown.required_skills.earned_score,
      max: breakdown.required_skills.max_score,
      commentary: breakdown.required_skills.commentary,
      color: '#38bdf8', // sky
    },
    {
      name: 'Preferred Skills',
      shortName: 'Preferred',
      weight: '15%',
      earned: breakdown.preferred_skills.earned_score,
      max: breakdown.preferred_skills.max_score,
      commentary: breakdown.preferred_skills.commentary,
      color: '#818cf8', // indigo
    },
    {
      name: 'Experience Match',
      shortName: 'Experience',
      weight: '20%',
      earned: breakdown.experience.earned_score,
      max: breakdown.experience.max_score,
      commentary: breakdown.experience.commentary,
      color: '#34d399', // emerald
    },
    {
      name: 'Education & Certs',
      shortName: 'Education',
      weight: '5%',
      earned: breakdown.education_certs.earned_score,
      max: breakdown.education_certs.max_score,
      commentary: breakdown.education_certs.commentary,
      color: '#fbbf24', // amber
    },
    {
      name: 'Projects & Domain',
      shortName: 'Projects',
      weight: '10%',
      earned: breakdown.projects.earned_score,
      max: breakdown.projects.max_score,
      commentary: breakdown.projects.commentary,
      color: '#c084fc', // purple
    },
  ];

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-slate-900 border border-slate-700 p-3 rounded-lg shadow-xl text-xs max-w-xs">
          <p className="font-semibold text-white mb-1">
            {data.name} ({data.weight})
          </p>
          <div className="flex items-center space-x-2 text-slate-300 mb-1.5">
            <span>Score:</span>
            <span className="font-bold text-sky-400">
              {data.earned} / {data.max} pts
            </span>
            <span className="text-[10px] text-slate-400">
              ({Math.round((data.earned / data.max) * 100)}%)
            </span>
          </div>
          <p className="text-[11px] text-slate-400 leading-snug">{data.commentary}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-lg flex flex-col justify-between">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <BarChart3 className="w-4 h-4 text-sky-400" />
          <h2 className="text-sm font-semibold text-white">Transparent Score Breakdown</h2>
        </div>
        <span className="text-xs text-slate-400">Weighted evaluation across 5 dimensions</span>
      </div>

      {/* Chart visualization */}
      <div className="h-52 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={chartData}
            layout="vertical"
            margin={{ top: 5, right: 25, left: 10, bottom: 5 }}
          >
            <XAxis type="number" domain={[0, 50]} tick={{ fill: '#94a3b8', fontSize: 11 }} />
            <YAxis
              type="category"
              dataKey="shortName"
              tick={{ fill: '#cbd5e1', fontSize: 11, fontWeight: 500 }}
              width={75}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="earned" radius={[0, 4, 4, 0]} barSize={16}>
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Breakdown detail list */}
      <div className="mt-4 pt-3 border-t border-slate-800/80 space-y-2">
        {chartData.map((item, idx) => (
          <div key={idx} className="flex items-center justify-between text-xs">
            <div className="flex items-center space-x-2 truncate">
              <span className="w-2 h-2 rounded-full" style={{ backgroundColor: item.color }} />
              <span className="text-slate-300 font-medium">{item.name}</span>
              <span className="text-[10px] text-slate-400">({item.weight})</span>
            </div>
            <div className="flex items-center space-x-1 font-mono">
              <span className="font-semibold text-white">{item.earned}</span>
              <span className="text-slate-400">/{item.max}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
