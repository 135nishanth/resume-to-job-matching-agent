import React, { useRef, useState } from 'react';
import { UploadCloud, FileText, CheckCircle2, X } from 'lucide-react';

interface FileUploadProps {
  selectedFile: File | null;
  onFileSelect: (file: File | null) => void;
  isLoading: boolean;
}

export const FileUpload: React.FC<FileUploadProps> = ({
  selectedFile,
  onFileSelect,
  isLoading,
}) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    if (isLoading) return;

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      validateAndSet(file);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      validateAndSet(e.target.files[0]);
    }
  };

  const validateAndSet = (file: File) => {
    const validExtensions = ['.pdf', '.docx', '.txt', '.md'];
    const hasValidExt = validExtensions.some((ext) => file.name.toLowerCase().endsWith(ext));
    if (!hasValidExt) {
      alert('Please upload a PDF (.pdf), Word document (.docx), or text file (.txt).');
      return;
    }
    onFileSelect(file);
  };

  const formatSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between mb-2">
        <label className="text-sm font-semibold text-slate-200 flex items-center gap-1.5">
          <FileText className="w-4 h-4 text-sky-400" />
          <span>Candidate Resume</span>
        </label>
        <span className="text-xs text-slate-400">PDF, DOCX, or TXT</span>
      </div>

      {!selectedFile ? (
        <div
          onDragOver={(e) => {
            e.preventDefault();
            setIsDragOver(true);
          }}
          onDragLeave={() => setIsDragOver(false)}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          className={`flex-1 min-h-[220px] rounded-xl border-2 border-dashed transition-all flex flex-col items-center justify-center p-6 text-center cursor-pointer ${
            isDragOver
              ? 'border-sky-500 bg-sky-500/10'
              : 'border-slate-700/80 bg-slate-900/40 hover:bg-slate-900/70 hover:border-slate-600'
          }`}
        >
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleChange}
            accept=".pdf,.docx,.txt,.md"
            className="hidden"
            disabled={isLoading}
          />
          <div className="w-12 h-12 rounded-full bg-slate-800 flex items-center justify-center mb-3 text-sky-400 border border-slate-700">
            <UploadCloud className="w-6 h-6" />
          </div>
          <p className="text-sm font-medium text-slate-200">
            Drag & drop resume here, or <span className="text-sky-400 hover:underline">browse</span>
          </p>
          <p className="text-xs text-slate-500 mt-1">Supports PDF, Word (.docx), or plain text (.txt)</p>
        </div>
      ) : (
        <div className="flex-1 min-h-[220px] rounded-xl border border-sky-500/30 bg-sky-950/20 p-5 flex flex-col justify-between">
          <div className="flex items-start justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-lg bg-sky-500/10 border border-sky-500/20 flex items-center justify-center text-sky-400">
                <FileText className="w-5 h-5" />
              </div>
              <div>
                <p className="text-sm font-semibold text-white break-all">{selectedFile.name}</p>
                <p className="text-xs text-slate-400 mt-0.5">{formatSize(selectedFile.size)}</p>
              </div>
            </div>
            <button
              onClick={() => onFileSelect(null)}
              disabled={isLoading}
              className="p-1 rounded-md text-slate-400 hover:text-white hover:bg-slate-800 transition"
              title="Remove file"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          <div className="flex items-center space-x-2 text-xs text-emerald-400 bg-emerald-950/30 border border-emerald-500/20 rounded-lg px-3 py-2 mt-4">
            <CheckCircle2 className="w-4 h-4 shrink-0" />
            <span>Document ready for semantic extraction and parsing</span>
          </div>
        </div>
      )}
    </div>
  );
};
