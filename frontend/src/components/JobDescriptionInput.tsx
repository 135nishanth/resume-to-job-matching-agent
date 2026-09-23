import React, { useState, useRef } from 'react';
import { Briefcase, Upload, FileText, X, CheckCircle2 } from 'lucide-react';

interface JobDescriptionInputProps {
  jobText: string;
  onJobTextChange: (text: string) => void;
  selectedJdFile: File | null;
  onJdFileSelect: (file: File | null) => void;
  isLoading: boolean;
}

export const JobDescriptionInput: React.FC<JobDescriptionInputProps> = ({
  jobText,
  onJobTextChange,
  selectedJdFile,
  onJdFileSelect,
  isLoading,
}) => {
  const [activeTab, setActiveTab] = useState<'paste' | 'upload'>('paste');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      onJdFileSelect(file);
      onJobTextChange(''); // clear text if file selected
    }
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between mb-2">
        <label className="text-sm font-semibold text-slate-200 flex items-center gap-1.5">
          <Briefcase className="w-4 h-4 text-indigo-400" />
          <span>Job Description</span>
        </label>
        {/* Mode Switch Tabs */}
        <div className="flex rounded-lg bg-slate-900 border border-slate-800 p-0.5 text-xs">
          <button
            type="button"
            onClick={() => {
              setActiveTab('paste');
              onJdFileSelect(null);
            }}
            className={`px-2.5 py-1 rounded-md font-medium transition ${
              activeTab === 'paste'
                ? 'bg-indigo-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Paste Text
          </button>
          <button
            type="button"
            onClick={() => {
              setActiveTab('upload');
            }}
            className={`px-2.5 py-1 rounded-md font-medium transition ${
              activeTab === 'upload'
                ? 'bg-indigo-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Upload File
          </button>
        </div>
      </div>

      {activeTab === 'paste' ? (
        <div className="flex-1 flex flex-col min-h-[220px]">
          <div className="relative flex-1">
            <textarea
              value={jobText}
              onChange={(e) => onJobTextChange(e.target.value)}
              disabled={isLoading}
              placeholder="Paste the target job description here... (Include Required Skills, Responsibilities, Years of Experience, and Preferred Qualifications)"
              className="w-full h-full min-h-[220px] p-4 text-xs font-mono leading-relaxed rounded-xl border border-slate-700/80 bg-slate-900/60 text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition resize-none"
            />
            {jobText && (
              <button
                type="button"
                onClick={() => onJobTextChange('')}
                disabled={isLoading}
                className="absolute top-3 right-3 p-1 rounded-md bg-slate-800/80 hover:bg-slate-700 text-slate-400 hover:text-white transition"
                title="Clear text"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            )}
          </div>
          <div className="flex items-center justify-between text-[11px] text-slate-500 mt-2 px-1">
            <span>Minimum 30 characters recommended for accurate extraction</span>
            <span>{jobText.length} characters</span>
          </div>
        </div>
      ) : (
        <div className="flex-1 min-h-[220px] flex flex-col justify-center">
          {!selectedJdFile ? (
            <div
              onClick={() => fileInputRef.current?.click()}
              className="flex-1 min-h-[220px] rounded-xl border-2 border-dashed border-slate-700/80 bg-slate-900/40 hover:bg-slate-900/70 hover:border-slate-600 transition flex flex-col items-center justify-center p-6 text-center cursor-pointer"
            >
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileChange}
                accept=".txt,.pdf,.docx"
                className="hidden"
                disabled={isLoading}
              />
              <div className="w-12 h-12 rounded-full bg-slate-800 flex items-center justify-center mb-3 text-indigo-400 border border-slate-700">
                <Upload className="w-6 h-6" />
              </div>
              <p className="text-sm font-medium text-slate-200">
                Click to upload Job Description file
              </p>
              <p className="text-xs text-slate-500 mt-1">Supports TXT, PDF, or DOCX formats</p>
            </div>
          ) : (
            <div className="flex-1 min-h-[220px] rounded-xl border border-indigo-500/30 bg-indigo-950/20 p-5 flex flex-col justify-between">
              <div className="flex items-start justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 rounded-lg bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400">
                    <FileText className="w-5 h-5" />
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-white break-all">{selectedJdFile.name}</p>
                    <p className="text-xs text-slate-400 mt-0.5">
                      {(selectedJdFile.size / 1024).toFixed(1)} KB
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => onJdFileSelect(null)}
                  disabled={isLoading}
                  className="p-1 rounded-md text-slate-400 hover:text-white hover:bg-slate-800 transition"
                  title="Remove file"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>

              <div className="flex items-center space-x-2 text-xs text-emerald-400 bg-emerald-950/30 border border-emerald-500/20 rounded-lg px-3 py-2 mt-4">
                <CheckCircle2 className="w-4 h-4 shrink-0" />
                <span>Job Description loaded and ready for analysis</span>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
