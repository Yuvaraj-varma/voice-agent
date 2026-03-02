export default function LoadingSpinner({ message = "Loading..." }) {
  return (
    <div className="flex flex-col items-center justify-center p-6">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mb-3"></div>
      <p className="text-gray-600 text-sm">{message}</p>
    </div>
  );
}

export function ButtonLoading({ children, loading, ...props }) {
  return (
    <button {...props} disabled={loading}>
      {loading ? (
        <div className="flex items-center justify-center gap-2">
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
          Processing...
        </div>
      ) : (
        children
      )}
    </button>
  );
}