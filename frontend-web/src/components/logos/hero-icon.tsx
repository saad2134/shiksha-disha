export default function HeroIcon({ className }: { className?: string }) {
  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <div className="relative flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-violet-600 via-purple-500 to-indigo-600 shadow-lg shadow-purple-500/25">
        <svg 
          xmlns="http://www.w3.org/2000/svg" 
          viewBox="0 0 24 24" 
          fill="none" 
          stroke="currentColor" 
          strokeWidth="2" 
          strokeLinecap="round" 
          strokeLinejoin="round"
          className="h-5 w-5 text-white"
        >
          <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z" />
          <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z" />
        </svg>
        <div className="absolute -right-1 -top-1 h-3 w-3 rounded-full bg-green-400 ring-2 ring-white" />
      </div>
      <div className="flex flex-col">
        <span className="text-sm font-bold text-foreground">ShikshaDisha</span>
        <span className="text-xs text-muted-foreground">Learn & Grow</span>
      </div>
    </div>
  );
}
