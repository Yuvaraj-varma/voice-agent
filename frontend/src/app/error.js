"use client";

export default function Error({ error }) {
  return (
    <div className="p-6 text-center">
      <h2 className="text-xl font-bold text-red-600">
        Something went wrong
      </h2>
      <p className="text-gray-600 mt-2">
        {error?.message}
      </p>
    </div>
  );
}
