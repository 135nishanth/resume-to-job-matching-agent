import React, { useEffect, useState } from 'react';
import { X, History, User, Briefcase, ChevronRight, Clock, Trash2 } from 'lucide-react';
import { HistorySummary, AnalysisResponse } from '../types';
import { fetchHistory, fetchHistoryDetail } from '../services/api';

interface HistoryDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectRecord: (record: AnalysisResponse) => void;
}

export const HistoryDrawer: React.FC<HistoryDrawerProps> = ({
  isOpen,
  onClose,
  onSelectRecord,
}) => {
  const [historyItems, setHistoryItems] = useState<HistorySummary[]>([]);
  const [loading, setLoading] = useState(false);
  const [loadingId, setLoadingId] = useState<number | null>(null);

  useEffect(() => {
    if (isOpen) {
      loadHistory();
    }
  }, [isOpen]);

  const loadHistory = async () => {
    setLoading(true);
    try {
      const data = await fetchHistory();
      setHistoryItems(data);
    } catch (err) {
      console.error('Error fetching history:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelect = async (id: number) => {
    setLoadingId(id);
    try {
      const detail = await fetchHistoryDetail(id);
      onSelectRecord(detail);
      onClose();
    } catch (err) {
      alert('Failed to load analysis details.');
    } finally {
      setLoadingId(null);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
      {/* Backdrop */}
      <div
        onClick={onClose}
        className="absolute inset-0 bg-slate-950/70 backdrop-blur-sm transition-opacity"
      />

      <div className="fixed inset-y-0 right-0 max-w-full flex pl-10">
        <div className="w-screen max-w-md bg-slate-900 border-l border-slate-800 text-slate-200 flex flex-col shadow-2xl">
          {/* Header */}
          <div className="p-4 border-b border-slate-800 flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <History className="w-5 h-5 text-sky-400" />
              <h2 className="text-sm font-bold text-white">Analysis History</h2>
            </div>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* List */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {loading ? (
              <div className="text-center py-12 text-slate-500 text-xs">
                Loading analysis history...
              </div>
            ) : historyItems.length === 0 ? (
              <div className="text-center py-12 text-slate-500 text-xs">
                No past analysis runs recorded yet.
              </div>
            ) : (
              historyItems.map((item) => (
                <div
                  key={item.id}
                  onClick={() => handleSelect(item.id)}
                  className="p-3.5 rounded-xl border border-slate-800 bg-slate-950/60 hover:bg-slate-800/60 hover:border-slate-700 cursor-pointer transition flex items-center justify-between group"
                >
                  <div className="flex-1 min-w-0 pr-3">
                    <div className="flex items-center space-x-2 mb-1">
                      <User className="w-3.5 h-3.5 text-sky-400" />
                      <span className="text-xs font-bold text-white truncate">
                        {item.candidate_name}
                      </span>
                    </div>

                    <div className="flex items-center space-x-2 text-slate-400 text-[11px] mb-2 truncate">
                      <Briefcase className="w-3 h-3 text-slate-500" />
                      <span className="truncate">{item.job_title}</span>
                    </div>

                    <div className="flex items-center space-x-2 text-[10px] text-slate-500">
                      <Clock className="w-3 h-3" />
                      <span>{item.created_at ? new Date(item.created_at).toLocaleDateString() : 'Recent'}</span>
                      <span>•</span>
                      <span>{item.total_matched} matched</span>
                      <span>•</span>
                      <span>{item.total_missing} missing</span>
                    </div>
                  </div>

                  <div className="flex flex-col items-end">
                    <span className="text-lg font-black text-sky-400 font-mono">
                      {Math.round(item.overall_score)}
                    </span>
                    <span className="text-[9px] text-slate-400 uppercase tracking-wider">
                      score
                    </span>
                    <ChevronRight className="w-4 h-4 text-slate-600 group-hover:text-sky-400 transition mt-1" />
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
