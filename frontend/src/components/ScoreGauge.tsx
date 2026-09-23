import React from 'react';
import { Award, CheckCircle, AlertTriangle } from 'lucide-react';

interface ScoreGaugeProps {
  score: number;
  ratingLabel: string;
}

export const ScoreGauge: React.FC<ScoreGaugeProps> = ({ score, ratingLabel }) => {
  // SVG ring parameters
  const size = 180;
  const strokeWidth = 14;
  const center = size / 2;
  const radius = center - strokeWidth;
  const circumference = 2 * Math.PI * radius;
  // Calculate arc stroke offset
  const strokeDashoffset = circumference - (Math.min(100, Math.max(0, score)) / 100) * circumference;

  // Determine color scheme based on score
  const getColorClasses = (s: number) => {
    if (s >= 85) {
      return {
        text: 'text-emerald-400',
        stroke: '#10b981',
        glow: 'rgba(16, 185, 129, 0.25)',
        badgeBg: 'bg-emerald-950/50 text-emerald-400 border-emerald-500/30',
        icon: Award,
      };
    } else if (s >= 70) {
      return {
        text: 'text-sky-400',
        stroke: '#0284c7',
        glow: 'rgba(2, 132, 199, 0.25)',
        badgeBg: 'bg-sky-950/50 text-sky-400 border-sky-500/30',
        icon: CheckCircle,
      };
    } else if (s >= 50) {
      return {
        text: 'text-amber-400',
        stroke: '#f59e0b',
        glow: 'rgba(245, 158, 11, 0.25)',
        badgeBg: 'bg-amber-950/50 text-amber-400 border-amber-500/30',
        icon: AlertTriangle,
      };
    } else {
      return {
        text: 'text-rose-400',
        stroke: '#f43f5e',
        glow: 'rgba(244, 63, 94, 0.25)',
        badgeBg: 'bg-rose-950/50 text-rose-400 border-rose-500/30',
        icon: AlertTriangle,
      };
    }
  };

  const scheme = getColorClasses(score);
  const Icon = scheme.icon;

  return (
    <div className="flex flex-col items-center justify-center p-6 bg-slate-900/80 border border-slate-800 rounded-2xl relative overflow-hidden shadow-xl">
      {/* Background radial glow */}
      <div
        className="absolute w-44 h-44 rounded-full blur-3xl -top-10 -left-10 pointer-events-none"
        style={{ background: scheme.glow }}
      />

      <div className="relative flex items-center justify-center">
        <svg width={size} height={size} className="transform -rotate-90">
          {/* Background circle track */}
          <circle
            cx={center}
            cy={center}
            r={radius}
            fill="transparent"
            stroke="#1e293b"
            strokeWidth={strokeWidth}
          />
          {/* Animated score progress stroke */}
          <circle
            cx={center}
            cy={center}
            r={radius}
            fill="transparent"
            stroke={scheme.stroke}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className="transition-all duration-1000 ease-out"
          />
        </svg>

        {/* Center score readout */}
        <div className="absolute flex flex-col items-center justify-center text-center">
          <div className="flex items-baseline">
            <span className={`text-5xl font-black tracking-tight ${scheme.text}`}>
              {Math.round(score)}
            </span>
            <span className="text-sm font-semibold text-slate-400 ml-1">/100</span>
          </div>
          <span className="text-[11px] font-medium text-slate-400 uppercase tracking-widest mt-1">
            Compatibility
          </span>
        </div>
      </div>

      {/* Qualitative Label Badge */}
      <div className={`mt-5 px-3.5 py-1.5 rounded-full border text-xs font-semibold flex items-center space-x-1.5 shadow-sm ${scheme.badgeBg}`}>
        <Icon className="w-4 h-4" />
        <span>{ratingLabel}</span>
      </div>
    </div>
  );
};
